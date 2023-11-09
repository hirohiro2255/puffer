import json
import copy
from defs import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY, SENTINEL


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
        for i in range(2, 10):
            for j in range(2, 10):
                piece = '.'
                if self.state[i][j] == WHITE | PAWN:
                    piece = '♙'
                elif self.state[i][j] == WHITE | KNIGHT:
                    piece = '♘'
                elif self.state[i][j] == WHITE | BISHOP:
                    piece = '♗'
                elif self.state[i][j] == WHITE | ROOK:
                    piece = '♖'
                elif self.state[i][j] == WHITE | QUEEN:
                    piece = '♕'
                elif self.state[i][j] == WHITE | KING:
                    piece = '♔'
                elif self.state[i][j] == BLACK | PAWN:
                    piece = '♟︎'
                elif self.state[i][j] == BLACK | KNIGHT:
                    piece = '♞'
                elif self.state[i][j] == BLACK | BISHOP:
                    piece = '♝'
                elif self.state[i][j] == BLACK | ROOK:
                    piece = '♜'
                elif self.state[i][j] == BLACK | QUEEN:
                    piece = '♛'
                elif self.state[i][j] == BLACK | KING:
                    piece = '♚'

                print(f'{piece} ', end='')
            print()


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
    b.print_board()
