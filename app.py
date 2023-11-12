from typing import List, Tuple
import json
import copy
from defs import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY, SENTINEL, DEFAULT_POSITION, KIWI_PETE, POSITION_3, BOARD_START, BOARD_END, is_empty, COLOR_MASK, is_king, is_white, is_black
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
            self.white_king_location = (0, 0)
            self.black_king_location = (0, 0)

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
    halfmove_clock = fen_config[4]
    fullmove_clock = fen_config[5]

    white_king_location = (0, 0)
    black_king_location = (0, 0)

    fen_rows = fen_config[0].split('/')
    if len(fen_rows) != 8:
        raise ValueError(
            "Could not parse fen string: Invalid number of rows provided, 8 expected")

    row = BOARD_START
    col = BOARD_START
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

    board = Chess('settings.json')
    board.state = b
    board.to_move = to_move
    board.white_king_location = white_king_location
    board.black_king_location = black_king_location
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


if __name__ == '__main__':
    chess = Chess('settings.json')
# chess.play()
    # print(chess.state)
    b = new_board()
    board = board_from_fen()
    board.print_board()
    print(board.state)
