import copy
from typing import List, Tuple
from defs import EMPTY, WHITE, is_empty, COLOR_MASK, is_white, is_outside_board, is_black, PIECE_MASK, PAWN, ROOK, BISHOP, KNIGHT, QUEEN, KING, BLACK, CastlingType, BOARD_END, BOARD_START, EN_PASSANT, get_color, is_pawn, is_king
import sys
import json
from defs import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY, SENTINEL, DEFAULT_POSITION, KIWI_PETE, POSITION_3, BOARD_START, BOARD_END, is_empty, COLOR_MASK, is_king, is_white, is_black, algebraic_pairs_to_board_position, EN_PASSANT, Point, DEFAULT_POSITION
from utils import get_piece_character, get_piece_from_fen_string_char


class Chess:
    def __init__(self, filename):
        with open(filename) as f:
            self.__dict__ = json.loads(f.read())
            self.board = list('         \n' * 2 + ' ' + ''.join([
                '.' * int(c) if c.isdigit() else c
                for c in self.fen.split()[0].replace('/', '\n ')
            ]) + '\n' + '         \n' * 2)
            self.side = 0 if self.fen.split()[1] == 'w' else 1
            self.state = [[0] * 12 for i in range(12)]
            self.to_move = WHITE
            self.white_king_location: Point = (0, 0)
            self.black_king_location: Point = (0, 0)
            self.white_king_side_castle = True
            self.white_queen_side_castle = True
            self.black_king_side_castle = True
            self.black_queen_side_castle = True
            self.pawn_double_move: Point | None = None
            # The number of the full moves. It starts at 1, and is incremented after Black's move
            self.full_move_clock = 1
            # The number of half moves since the last capture or pawn advance, used for the fifty-move rule
            self.half_move_clock = 0
            self.white_total_piece_value = 0
            self.black_total_piece_value = 0

    def swap_color(self):
        self.to_move = WHITE if self.to_move == BLACK else BLACK

    def do_move(self, move: str):
        move_str = move.strip()
        if len(move_str) < 4:
            raise ValueError("Invalid move string")

        from_cords = algebraic_pairs_to_board_position(move_str[:2])
        to_cords = algebraic_pairs_to_board_position(move_str[2:])
        print(f"piece on from square: {self.state[from_cords[0]][from_cords[1]]}")
        print(f"piece on to square: {self.state[to_cords[0]][to_cords[1]]}")
        from_piece_type = self.state[from_cords[0]][from_cords[1]]
        to_piece_type = self.state[to_cords[0]][to_cords[1]]

        if is_empty(from_piece_type):
            print("no piece to move on square you picked")
        elif is_outside_board(to_piece_type):
            print("you are about to move a piece to outside the board")





    def generate_moves(self):
        move_list = []
        for square in range(len(self.board)):
            piece = self.board[square]
            if piece not in ' .\n' and self.colors[piece] == self.side:
                for offset in self.directions[piece]:
                    target_square = square
                    while True:
                        target_square += offset
                        captured_piece = self.board[target_square]
                        if captured_piece in ' \n':
                            break
                        if self.colors[captured_piece] == self.side:
                            break
                        if piece in 'Pp' and offset in [9, 11, -9, -11] and captured_piece == '.':
                            break
                        if piece in 'Pp' and offset in [10, 20, -10, -20] and captured_piece != '.':
                            break
                        if piece == 'P' and offset == -20:
                            if square not in self.rank_2:
                                break
                            if self.board[square - 10] != '.':
                                break
                        if piece == 'p' and offset == 20:
                            if square not in self.rank_7:
                                break
                            if self.board[square + 10] != '.':
                                break
                        if captured_piece in 'Kk':
                            return []
                        move_list.append({
                            'source': square, 'target': target_square,
                            'piece': piece, 'captured': captured_piece
                        })
                        if self.colors[captured_piece] == (self.side ^ 1):
                            break
                        if piece in 'PpNnKk':
                            break
        return move_list

    def make_move(self, move):
        self.board[move['target']] = move['piece']
        self.board[move['source']] = '.'
        if move['piece'] == 'P' and move['source'] in self.rank_7:
            self.board[move['target']] = 'Q'
        if move['piece'] == 'p' and move['source'] in self.rank_2:
            self.board[move['target']] = 'q'
        self.side ^= 1

    def take_back(self, move):
        self.board[move['target']] = move['captured']
        self.board[move['source']] = move['piece']
        self.side ^= 1

    def search(self, depth):
        if depth == 0:
            return self.evaluate()
        best_score = -10000
        best_source, best_target = -1, -1
        move_list = self.generate_moves()
        if not len(move_list):
            return 10000
        for move in move_list:
            self.make_move(move)
            score = -self.search(depth - 1)
            self.take_back(move)
            if score > best_score:
                best_score = score
                best_source = move['source']
                best_target = move['target']
        self.best_source = best_source
        self.best_target = best_target
        return best_score

    def evaluate(self):
        score = 0
        for square in range(len(self.board)):
            piece = self.board[square]
            if piece not in ' .\n':
                score += self.weights[piece]
                if piece.islower():
                    score -= self.pst[square]
                if piece.isupper():
                    score += self.pst[square]
        return -score if self.side else score

    def play(self):
        print(''.join([' ' + self.pieces[p] for p in self.board]))
        while True:
            raw = input('   Your move: ')
            if len(raw) < 4:
                continue
            user_source = self.coordinates.index(raw[0] + raw[1])
            user_target = self.coordinates.index(raw[2] + raw[3])
            self.make_move({
                'source': user_source, 'target': user_target,
                'piece': self.board[user_source], 'captured': self.board[user_target]
            })
            print(''.join([' ' + self.pieces[p] for p in self.board]))
            score = self.search(3)
            self.make_move({
                'source': self.best_source, 'target': self.best_target,
                'piece': self.board[self.best_source], 'captured': self.board[self.best_target]
            })
            print(''.join([' ' + self.pieces[p] for p in self.board]))
            if abs(score) == 10000:
                print('   Checkmate!')
                break

    def print_board(self):
        print("\n   a b c d e f g h")
        for i in range(BOARD_START, BOARD_END):
            print(f'{10-i}  ', end='')
            for j in range(BOARD_START, BOARD_END):
                piece = "{} ".format(get_piece_character(self.state[i][j]))

                print(f'{piece}', end='')
            print(f' {10-i}')

        print("   a b c d e f g h")


def board_from_fen(fen: str = DEFAULT_POSITION) -> Chess:
    b = [[SENTINEL] * 12 for _ in range(12)]
    fen_config = fen.split(' ')
    if len(fen_config) != 6:
        raise ValueError('Could not parse fen string: Invalid fen string')

    to_move = WHITE if fen_config[1] == 'w' else BLACK
    castling_privileges = fen_config[2]
    en_passant = fen_config[3]

    half_move_clock = 0
    try:
        half_move_clock = int(fen_config[4])
    except:
        raise ValueError("Could not parse fen string: Invalid half move value")

    full_move_clock = 1
    try:
        full_move_clock = int(fen_config[5])
    except:
        raise ValueError("Could not parse fen string: Invalid full move value")

    white_king_location = (0, 0)
    black_king_location = (0, 0)

    fen_rows = fen_config[0].split('/')
    if len(fen_rows) != 8:
        raise ValueError(
            "Could not parse fen string: Invalid number of rows provided, 8 expected")

    row = BOARD_START
    col = BOARD_START
    white_piece_value = 0
    black_piece_value = 0

    for fen_row in fen_rows:
        for square in fen_row:
            if square.isdigit():
                square_skip_count = int(square)
                if square_skip_count + col > BOARD_END:
                    raise IndexError(
                        'Could not parse fen string: Index out of bounds')

                while square_skip_count > 0:
                    b[row][col] = EMPTY
                    col += 1
                    square_skip_count -= 1
            else:
                piece = get_piece_from_fen_string_char(square)
                if piece is None:
                    raise ValueError(
                        'Could not parse fen string: Invalid character found')
                else:
                    b[row][col] = piece

                if is_white(b[row][col]):
                    white_piece_value += PIECE_VALUES[b[row][col] & PIECE_MASK]
                else:
                    black_piece_value += PIECE_VALUES[b[row][col] & PIECE_MASK]

                if is_king(b[row][col]):
                    if is_white(b[row][col]):
                        white_king_location = (row, col)
                    else:
                        black_king_location = (row, col)

                col += 1
        if col != BOARD_END:
            raise ValueError(
                'Could not parse fen string: Complete row was not specified')
        row += 1
        col = BOARD_START

    # Deal with en passant
    en_passant_pos: Tuple[int, int] | None = None
    if len(en_passant) != 2:
        if en_passant != "-":
            raise ValueError(
                "Could not parse fen string: En passant string not valid")
    else:
        en_passant_pos = algebraic_pairs_to_board_position(en_passant)

    board = Chess('settings.json')
    board.state = b
    board.to_move = to_move
    board.white_king_location = white_king_location
    board.black_king_location = black_king_location
    board.white_king_side_castle = "K" in castling_privileges
    board.white_queen_side_castle = "Q" in castling_privileges
    board.black_king_side_castle = "k" in castling_privileges
    board.black_queen_side_castle = "q" in castling_privileges
    board.pawn_double_move = en_passant_pos
    board.half_move_clock = half_move_clock
    board.full_move_clock = full_move_clock
    board.black_total_piece_value = black_piece_value
    board.white_total_piece_value = white_piece_value
    return board


def new_board() -> Chess:
    b = [[SENTINEL] * 12 for i in range(12)]

    # white pieces
    b[2][2] = WHITE | ROOK
    b[2][3] = WHITE | KNIGHT
    b[2][4] = WHITE | BISHOP
    b[2][5] = WHITE | KING
    b[2][6] = WHITE | QUEEN
    b[2][7] = WHITE | BISHOP
    b[2][8] = WHITE | KNIGHT
    b[2][9] = WHITE | ROOK
    for i in range(2, 10):
        b[3][i] = WHITE | PAWN

    for i in range(4, 8):
        for j in range(2, 10):
            b[i][j] = EMPTY

    b[9][2] = BLACK | ROOK
    b[9][3] = BLACK | KNIGHT
    b[9][4] = BLACK | BISHOP
    b[9][5] = BLACK | KING
    b[9][6] = BLACK | QUEEN
    b[9][7] = BLACK | BISHOP
    b[9][8] = BLACK | KNIGHT
    b[9][9] = BLACK | ROOK

    for i in range(2, 10):
        b[8][i] = BLACK | PAWN

    chess = Chess('settings.json')
    chess.state = copy.deepcopy(b)
    chess.to_move = WHITE
    return chess




"""
1. The castling must be kingside or queen side.
    2. Neither the king nor the chosen rook has previously moved.
    3. There are no pieces between the king and the chosen rook.
    4. The king is not currently in check.
    5. The king does not pass through a square that is attacked by an enemy piece.
    6. The king does not end up in check. (True of any legal move.)
    This method will check all but rule 2
    This method will check the board state to determine if is should go ahead with the castling check
    If the associated castling privilege variable is set to true, the following will be assumed by this function
    1. The king and associated rook have not moved yet this game
    2. The king and associated rook are in the correct castling positions
    Thus its the responsibility of other functions to update the castling privilege variables when the king or associated rook moves (including castling)
"""


def can_castle(board: Chess, castling_type: CastlingType) -> bool:
    if castling_type == CastlingType.WHITE_KING_SIDE:
        if not board.white_king_side_castle:
            return False

        # check that squares required for castling are empty
        if not is_empty(board.state[9][7]) or not is_empty(board.state[9][8]):
            return False

        # check that the king currently is'nt in check
        if is_check(board, WHITE):
            return False

        # check that the square required for castling are not threatened
        if is_check_cords(board, WHITE, (9, 7)) or is_check_cords(board, WHITE, (9, 8)):
            return False

        return True

    if castling_type == CastlingType.WHITE_QUEEN_SIDE:
        if not board.white_queen_side_castle:
            return False

        # check that squares required for castling are empty
        if not is_empty(board.state[9][3]) or not is_empty(board.state[9][4]) or not is_empty(board.state[9][5]):
            return False

        # check that the king currently is'nt in check
        if is_check(board, WHITE):
            return False

        # check that the square required for castling are not threatened
        if is_check_cords(board, WHITE, (9, 5)) or is_check_cords(board, WHITE, (9, 4)):
            return False

        return True

    if castling_type == CastlingType.BLACK_KING_SIDE:
        if not board.black_king_side_castle:
            return False

        # check that squares required for castling are empty
        if not is_empty(board.state[2][7]) or not is_empty(board.state[2][8]):
            return False

        if is_check(board, BLACK):
            return False

        # check that the square required for castling are not threatened
        if is_check_cords(board, BLACK, (2, 7)) or is_check_cords(board, BLACK, (2, 8)):
            return False

        return True

    if castling_type == CastlingType.BLACK_QUEEN_SIDE:
        if not board.black_queen_side_castle:
            return False

        # check that squares required for castling are empty
        if not is_empty(board.state[2][3]) or not is_empty(board.state[2][4]) or not is_empty(board.state[2][5]):
            return False

        if is_check(board, BLACK):
            return False

        if is_check_cords(board, BLACK, (2, 4)) or is_check_cords(board, BLACK, (2, 5)):
            return False

        return True

    raise ValueError("Should'nt be here")


def is_check(board: Chess, color: int) -> bool:
    if color == WHITE:
        return is_check_cords(board, color, board.white_king_location)
    else:
        return is_check_cords(board, color, board.black_king_location)


def is_check_cords(board: Chess, color: int, square_cords: Tuple[int, int]) -> bool:
    attacking_color = None
    if color == WHITE:
        attacking_color = BLACK
    else:
        attacking_color = WHITE

    # Check from knight
    for mods in KNIGHT_CORDS:
        _row = square_cords[0] + mods[0]
        _col = square_cords[1] + mods[1]
        square = board.state[_row][_col]

        if square == (KNIGHT | attacking_color):
            return True

    # Check from pawn
    _row = None
    if color == WHITE:
        _row = square_cords[0] - 1
    else:
        _row = square_cords[0] + 1

    if board.state[_row][square_cords[1]-1] == (attacking_color | PAWN) or board.state[_row][square_cords[1]+1] == (attacking_color | PAWN):
        return True

    mods = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for m in mods:
        multiplier = 1
        _row = square_cords[0] + m[0]
        _col = square_cords[1] + m[1]
        square = board.state[_row][_col]
        while is_empty(square):
            multiplier += 1
            _row = square_cords[0] + m[0] * multiplier
            _col = square_cords[1] + m[1] * multiplier
            square = board.state[_row][_col]

        if square == (attacking_color | ROOK) or square == (attacking_color | QUEEN):
            return True

    # Check from bishop or queen
    mods = [1, -1]
    for i in mods:
        for j in mods:
            multiplier = 1
            _row = square_cords[0] + i
            _col = square_cords[1] + j
            square = board.state[_row][_col]
            while is_empty(square):
                multiplier += 1
                _row = square_cords[0] + i * multiplier
                _col = square_cords[1] + j * multiplier
                square = board.state[_row][_col]

            if square == (attacking_color | BISHOP) or square == (attacking_color | QUEEN):
                return True

    # Check from king
    for i in range(-1, 2):
        for j in range(-1, 2):
            _row = square_cords[0] + i
            _col = square_cords[1] + j
            square = board.state[_row][_col]
            if is_outside_board(square):
                continue

            if is_king(square) and (square & COLOR_MASK) == attacking_color:
                return True
    return False


def get_moves(row: int, col: int, board: Chess, moves: List[Tuple[int, int]]):
    piece = board.state[row][col]
    piece_type = piece & PIECE_MASK
    if piece_type == PAWN:
        pawn_moves(row, col, board, moves)
    elif piece_type == ROOK:
        rook_moves(row, col, board, moves)
    elif piece_type == BISHOP:
        bishop_moves(row, col, board, moves)
    elif piece_type == KNIGHT:
        knight_moves(row, col, board, moves)
    elif piece_type == KING:
        king_moves(row, col, board, moves)
    elif piece_type == QUEEN:
        queen_moves(row, col, board, moves)
    else:
        raise ValueError('Unrecognized piece')


def queen_moves(row: int, col: int, board: Chess, moves: List[Tuple[int, int]]):
    rook_moves(row, col, board, moves)
    bishop_moves(row, col, board, moves)


def bishop_moves(row: int, col: int, board: Chess, moves: List[Tuple[int, int]]):
    mods = [1, -1]
    piece = board.state[row][col]
    for i in mods:
        for j in mods:
            multiplier = 1
            _row = row + i
            _col = col + j
            square = board.state[_row][_col]
            while is_empty(square):
                moves.append((_row, _col))
                multiplier += 1
                _row = row + (i * multiplier)
                _col = col + (j * multiplier)
                square = board.state[_row][_col]

            if not is_outside_board(square) and (piece & COLOR_MASK) != (square & COLOR_MASK):
                moves.append((_row, _col))


def rook_moves(row: int, col: int, board: Chess, moves: List[Tuple[int, int]]):
    mods = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    piece = board.state[row][col]
    for m in mods:
        mutiplier = 1
        _row = row + m[0]
        _col = col + m[1]
        square = board.state[_row][_col]
        while is_empty(square):
            moves.append((_row, _col))
            mutiplier += 1
            _row = row + (m[0] * mutiplier)
            _col = col + (m[1] * mutiplier)
            square = board.state[_row][_col]

        if not is_outside_board(square) and (piece & COLOR_MASK) != (square & COLOR_MASK):
            moves.append((_row, _col))


def king_moves(row: int, col: int, board: Chess, moves: List[Tuple[int, int]]):
    piece = board.state[row][col]
    for i in range(-1, 2):
        for j in range(-1, 2):
            _row = row+i
            _col = col+j

            if is_outside_board(board.state[_row][_col]):
                continue

            if is_empty(board.state[_row][_col]) or (board.state[_row][_col] & COLOR_MASK) != (piece & COLOR_MASK):
                moves.append((_row, _col))


def pawn_moves(row: int, col: int, board: Chess, moves: List[Tuple[int, int]]):
    piece = board.state[row][col]
    # white pawns move up board
    if is_white(piece):
        # check capture
        left_cap = board.state[row-1][col-1]
        right_cap = board.state[row-1][col+1]
        if not is_outside_board(left_cap) and is_black(left_cap):
            moves.append((row-1, col-1))

        if not is_outside_board(right_cap) and is_black(right_cap):
            moves.append((row-1, col+1))

        # check a normal push
        if is_empty(board.state[row-1][col]):
            moves.append((row-1, col))
            # check double push
            if row == 8 and is_empty(board.state[row-2][col]):
                moves.append((row-2, col))

    else:
        # check capture
        left_cap = board.state[row+1][col+1]
        right_cap = board.state[row+1][col-1]
        if not is_outside_board(left_cap) and is_white(left_cap):
            moves.append((row+1, col+1))

        if not is_outside_board(right_cap) and is_white(right_cap):
            moves.append((row+1, col-1))

        # check a normal push
        if is_empty(board.state[row+1][col]):
            moves.append((row+1, col))
            # check double push
            if row == 3 and is_empty(board.state[row+2][col]):
                moves.append((row+2, col))


def pawn_moves_en_passant(row: int, col: int,  board: Chess) -> Tuple[int, int] | None:
    piece = board.state[row][col]
    if board.pawn_double_move is None:
        return None

    if is_white(piece) and row == BOARD_START+3:
        left_cap = (row-1, col-1)
        right_cap = (row-1, col+1)
        if left_cap == board.pawn_double_move:
            return left_cap
        elif right_cap == board.pawn_double_move:
            return right_cap

    elif is_black(piece) and row == BOARD_START+4:
        left_cap = (row+1, col+1)
        right_cap = (row+1, col-1)
        if left_cap == board.pawn_double_move:
            return left_cap
        elif right_cap == board.pawn_double_move:
            return right_cap

    return None


KNIGHT_CORDS = [(1, 2),
                (1, -2),
                (2, 1),
                (2, -1),
                (-1, 2),
                (-1, -2),
                (-2, -1),
                (-2, 1)]


def knight_moves(row: int, col: int, board: Chess, moves: List[Tuple[int, int]]):
    piece = board.state[row][col]
    for mods in KNIGHT_CORDS:
        _row = row + mods[0]
        _col = col + mods[1]
        square = board.state[_row][_col]

        if is_outside_board(board.state[_row][_col]):
            continue

        if is_empty(square) or (square & COLOR_MASK) != piece & COLOR_MASK:
            moves.append((_row, _col))


def generate_moves(board: Chess) -> List[Chess]:
    new_moves: List[Chess] = []

    for i in range(BOARD_START, BOARD_END):
        for j in range(BOARD_START, BOARD_END):
            color = get_color(board.state[i][j])
            if color is not None and color == board.to_move:
                moves: List[int] = []
                piece = board.state[i][j]
                get_moves(i, j, board, moves)
                # make all the valid moes of this piece
                for _move in moves:
                    new_board = copy.deepcopy(board)
                    new_board.swap_color()
                    if color == BLACK:
                        new_board.full_move_clock += 1

                    # update king location if we are moving the king
                    if piece == WHITE | KING:
                        new_board.white_king_location = (_move[0], _move[1])
                    elif piece == BLACK | KING:
                        new_board.black_king_location = (_move[0], _move[1])

                    target_square = new_board.state[_move[0]][_move[1]]
                    if not is_empty(target_square):
                        piece_value = PIECE_VALUES[target_square & PIECE_MASK]

                        if board.to_move == WHITE:
                            new_board.black_total_piece_value -= piece_value
                        else:
                            new_board.white_total_piece_value -= piece_value

                    # this will take care of any captures, except for en passant captures
                    new_board.state[_move[0]][_move[1]] = piece
                    new_board.state[i][j] = EMPTY

                    # if you make your move, and you are in check, this move is not valid
                    if is_check(new_board, color):
                        continue

                    # this is a valid board state, update the variables

                    # deal with setting castling privileges and updating king location
                    if piece == WHITE | KING:
                        new_board.white_king_side_castle = False
                        new_board.white_queen_side_castle = False
                    elif piece == BLACK | KING:
                        new_board.black_king_side_castle = False
                        new_board.black_queen_side_castle = False
                    elif i == BOARD_END-1 and j == BOARD_END-1:
                        new_board.white_king_side_castle = False
                    elif i == BOARD_END-1 and j == BOARD_START:
                        new_board.white_queen_side_castle = False
                    elif i == BOARD_START and j == BOARD_START:
                        new_board.black_queen_side_castle = False
                    elif i == BOARD_START and j == BOARD_END-1:
                        new_board.black_king_side_castle = False

                    # if the rook is captured, take away castling privileges
                    if _move[0] == BOARD_END-1 and _move[1] == BOARD_END-1:
                        new_board.white_king_side_castle = False
                    elif _move[0] == BOARD_END-1 and _move[1] == BOARD_START:
                        new_board.white_queen_side_castle = False
                    elif _move[0] == BOARD_START and _move[1] == BOARD_START:
                        new_board.black_queen_side_castle = False
                    elif _move[0] == BOARD_START and _move[1] == BOARD_END-1:
                        new_board.black_king_side_castle = False

                    # checks if the pawn has moved two spaces, if it has it can be captured en passant, record the space behind the pawn
                    if is_pawn(piece) and abs(i-_move[0]) == 2:
                        if is_white(piece):
                            new_board.pawn_double_move = (_move[0]+1, _move[1])
                        else:
                            new_board.pawn_double_move = (_move[0]-1, _move[1])
                    else:
                        # the most recent move was not a double pawn move, unset any possibly existing pawn double move
                        new_board.pawn_double_move = None


                    # deal with pawn promotions
                    if _move[0] == BOARD_START and piece == (WHITE | PAWN):
                        for promotion_piece in [QUEEN, KNIGHT, BISHOP, ROOK]:
                            _new_board = copy.deepcopy(new_board)
                            _new_board.pawn_double_move = None
                            _new_board.state[_move[0]][_move[1]] = (
                                WHITE | promotion_piece)
                            _new_board.white_total_piece_value += (PIECE_VALUES[promotion_piece] - PIECE_VALUES[PAWN])
                            new_moves.append(_new_board)
                    elif piece == (BLACK | PAWN) and _move[0] == BOARD_END-1:
                        for promotion_piece in [QUEEN, KNIGHT, BISHOP, ROOK]:
                            _new_board = copy.deepcopy(new_board)
                            _new_board.state[_move[0]][_move[1]] = (
                                BLACK | promotion_piece)
                            _new_board.black_total_piece_value += (PIECE_VALUES[promotion_piece] - PIECE_VALUES[PAWN])
                            new_moves.append(_new_board)
                    else:
                        new_moves.append(new_board)

                # take care of en passant captures
                if is_pawn(piece):
                    en_passant = pawn_moves_en_passant(i, j, board)
                    if en_passant is not None:
                        _move = copy.deepcopy(en_passant)
                        new_board = copy.deepcopy(board)
                        new_board.swap_color()
                        new_board.pawn_double_move = None

                        new_board.state[_move[0]][_move[1]] = piece
                        new_board.state[i][j] = EMPTY
                        if is_white(piece):
                            new_board.state[_move[0]+1][_move[1]] = EMPTY
                            new_board.black_total_piece_value -= PIECE_VALUES[PAWN]
                        else:
                            new_board.state[_move[0]-1][_move[1]] = EMPTY
                            new_board.white_total_piece_value -= PIECE_VALUES[PAWN]

                        # if you make your move, and you do not end up in check, this this move is valid
                        if not is_check(new_board, board.to_move):
                            new_moves.append(new_board)

    # take care of castling
    if board.to_move == WHITE and can_castle(board, CastlingType.WHITE_KING_SIDE):
        new_board = copy.deepcopy(board)
        new_board.swap_color()
        new_board.pawn_double_move = None
        new_board.white_king_side_castle = False
        new_board.white_queen_side_castle = False
        new_board.white_king_location = (BOARD_END - 1, BOARD_END - 2)
        new_board.state[BOARD_END - 1][BOARD_START + 4] = EMPTY
        new_board.state[BOARD_END - 1][BOARD_END - 1] = EMPTY
        new_board.state[BOARD_END - 1][BOARD_END - 2] = WHITE | KING
        new_board.state[BOARD_END - 1][BOARD_END - 3] = WHITE | ROOK
        new_moves.append(new_board)

    if board.to_move == WHITE and can_castle(board, CastlingType.WHITE_QUEEN_SIDE):
        new_board = copy.deepcopy(board)
        new_board.swap_color()
        new_board.pawn_double_move = None
        new_board.white_king_side_castle = False
        new_board.white_queen_side_castle = False
        new_board.white_king_location = (BOARD_END - 1, BOARD_START + 2)
        new_board.state[BOARD_END - 1][BOARD_START + 4] = EMPTY
        new_board.state[BOARD_END - 1][BOARD_START] = EMPTY
        new_board.state[BOARD_END - 1][BOARD_START + 2] = WHITE | KING
        new_board.state[BOARD_END - 1][BOARD_START + 3] = WHITE | ROOK
        new_moves.append(new_board)

    if board.to_move == BLACK and can_castle(board, CastlingType.BLACK_KING_SIDE):
        new_board = copy.deepcopy(board)
        new_board.swap_color()
        new_board.pawn_double_move = None
        new_board.black_king_side_castle = False
        new_board.black_queen_side_castle = False
        new_board.black_king_location = (BOARD_START, BOARD_END - 2)
        new_board.state[BOARD_START][BOARD_START + 4] = EMPTY
        new_board.state[BOARD_START][BOARD_END - 1] = EMPTY
        new_board.state[BOARD_START][BOARD_END - 2] = BLACK | KING
        new_board.state[BOARD_START][BOARD_END - 3] = BLACK | ROOK
        new_moves.append(new_board)

    if board.to_move == BLACK and can_castle(board, CastlingType.BLACK_QUEEN_SIDE):
        new_board = copy.deepcopy(board)
        new_board.swap_color()
        new_board.pawn_double_move = None
        new_board.black_king_side_castle = False
        new_board.black_queen_side_castle = False
        new_board.black_king_location = (BOARD_START, BOARD_START + 2)
        new_board.state[BOARD_START][BOARD_START + 4] = EMPTY
        new_board.state[BOARD_START][BOARD_START] = EMPTY
        new_board.state[BOARD_START][BOARD_START + 2] = BLACK | KING
        new_board.state[BOARD_START][BOARD_START + 3] = BLACK | ROOK
        new_moves.append(new_board)

    return new_moves


def generate_moves_test(board: Chess, cur_depth: int, depth: int, move_counts: List[int]):
    if cur_depth == depth:
        return
    moves = generate_moves(board)
    move_counts[cur_depth] += len(moves)
    for mov in moves:
        generate_moves_test(mov, cur_depth+1, depth, move_counts)



PIECE_VALUES = [0, 100, 320, 330, 500, 900, 20000]

PAWN_WEIGHTS = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

KNIGHT_WEIGHTS = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50],
]

BISHOP_WEIGHTS = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20],
]

ROOK_WEIGHTS = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0],
]

QUEEN_WEIGHTS = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20],
]

KING_WEIGHTS = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20],
]

KING_LATE_GAME = [
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50],
]


def get_pos_evaluation(row: int, col: int, board: Chess, color: int) -> int:
    piece = board.state[row][col] & PIECE_MASK
    _row = row - BOARD_START
    _col = col - BOARD_START
    if color == BLACK:
        _row = 7 - _row

    if piece == PAWN:
        return PAWN_WEIGHTS[_row][_col]
    elif piece == ROOK:
        return ROOK_WEIGHTS[_row][_col]
    elif piece == BISHOP:
        return BISHOP_WEIGHTS[_row][_col]
    elif piece == KNIGHT:
        return KNIGHT_WEIGHTS[_row][_col]
    elif piece == KING:
        if board.full_move_clock > 30:
            return KING_LATE_GAME[_row][_col]
        else:
            return KING_WEIGHTS[_row][_col]
    elif piece == QUEEN:
        return QUEEN_WEIGHTS[_row][_col]
    else:
        raise ValueError("Could not recognize piece")


def get_evaluation(board: Chess) -> int:
    evaluation = board.white_total_piece_value
    evaluation -= board.black_total_piece_value
    for row in range(BOARD_START, BOARD_END):
        for col in range(BOARD_START, BOARD_END):
            square = board.state[row][col]
            if is_empty(square):
                continue

            if get_color(square) == WHITE:
                evaluation += get_pos_evaluation(row, col, board, WHITE)
            else:
                evaluation -= get_pos_evaluation(row, col, board, BLACK)

             
            

    return evaluation





def alpha_beta_search(board: Chess, depth: int, alpha: int, beta: int, maximizing_player: int) -> int:
    if depth == 0:
        return get_evaluation(board)

    states = generate_moves(board)
    if len(states) == 0:
        return get_evaluation(board)

    if maximizing_player == WHITE:
        val = -sys.maxsize - 1
        for board in states:
            val = max([val, alpha_beta_search(board,depth-1,alpha,beta,BLACK)])
            if val >= beta:
                break
            alpha = max([alpha, val])

        return val
    else:
        val = sys.maxsize
        for board in states:
            val = min([val, alpha_beta_search(board, depth-1, alpha, beta, WHITE)])
            if val <= alpha:
                break
            beta = min([beta, val])
        return val




if __name__ == '__main__':
    # chess = Chess('settings.json')
    board = board_from_fen(DEFAULT_POSITION)

    best_move = None
    next_board = board
    while board.full_move_clock < 200:
        if board.to_move == WHITE:
            best_move = -sys.maxsize - 1
        else:
            best_move = sys.maxsize

        moves = generate_moves(board)
        if len(moves) == 0:
            break

        for mov in moves:
            maximizer = BLACK if board.to_move == WHITE else WHITE
            res = alpha_beta_search(mov, 2, -sys.maxsize-1,sys.maxsize, maximizer)
            if board.to_move == WHITE and best_move < res:
                best_move = res
                next_board = mov
            elif board.to_move == BLACK and res < best_move:
                best_move = res
                next_board = mov
        next_board.print_board()
        board = next_board

    board.print_board()

    """
    * Get from-square and to-square in Point type.
    * Check if to-square is empty or not.
    * if empty just move to destination 
    * else if an opponent piece is where your piece is going , then get it
    * else if your own piece is where your  piece is  going then not allowed to move
    * update your state property
    """
    # chess.play()
    # print(chess.state)
    # b = new_board()
    # board = board_from_fen()
    # board.print_board()
    #
