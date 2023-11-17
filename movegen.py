import copy
from typing import List, Tuple
from defs import EMPTY, WHITE, is_empty, COLOR_MASK, is_white, is_outside_board, is_black, PIECE_MASK, PAWN, ROOK, BISHOP, KNIGHT, QUEEN, KING, BLACK, CastlingType, BOARD_END, BOARD_START, EN_PASSANT, get_color, is_pawn, is_king
from app import Chess

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

                    # update king location if we are moving the king
                    if piece == WHITE | KING:
                        new_board.white_king_location = (_move[0], _move[1])
                    elif piece == BLACK | KING:
                        new_board.black_king_location = (_move[0], _move[1])

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

                    new_board.swap_color()

                    # deal with pawn promotions
                    if piece == (WHITE | PAWN) and _move[0] == BOARD_START:
                        for promotion_piece in [QUEEN, KNIGHT, BISHOP, ROOK]:
                            _new_board = copy.deepcopy(new_board)
                            _new_board.pawn_double_move = None
                            _new_board.state[_move[0]][_move[1]] = (
                                WHITE | promotion_piece)
                            new_moves.append(_new_board)
                    elif piece == (BLACK | PAWN) and _move[0] == BOARD_END-1:
                        for promotion_piece in [QUEEN, KNIGHT, BISHOP, ROOK]:
                            _new_board = copy.deepcopy(new_board)
                            _new_board.state[_move[0]][_move[1]] = (
                                BLACK | promotion_piece)
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
                        else:
                            new_board.state[_move[0]-1][_move[1]] = EMPTY

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
