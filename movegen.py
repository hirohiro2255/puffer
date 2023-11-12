from typing import List, Tuple
from defs import is_empty, COLOR_MASK, is_white, is_outside_board, is_black, PIECE_MASK, PAWN, ROOK, BISHOP, KNIGHT, QUEEN, KING
from app import Chess


def is_check(board: Chess, color: int) -> bool:
    return True


def get_moves(row: int, col: int, piece: int, board: Chess, moves: List[Tuple[int, int]]):
    piece_type = piece & PIECE_MASK
    if piece_type == PAWN:
        pawn_moves(row, col, piece, board, moves)
    elif piece_type == ROOK:
        rook_moves(row, col, piece, board, moves)
    elif piece_type == BISHOP:
        bishop_moves(row, col, piece, board, moves)
    elif piece_type == KNIGHT:
        knight_moves(row, col, piece, board, moves)
    elif piece_type == KING:
        king_moves(row, col, piece, board, moves)
    elif piece_type == QUEEN:
        queen_moves(row, col, piece, board, moves)
    else:
        raise ValueError('Unrecognized piece')


def queen_moves(row: int, col: int, piece: int, board: Chess, moves: List[Tuple[int, int]]):
    rook_moves(row, col, piece, board, moves)
    bishop_moves(row, col, piece, board, moves)


def bishop_moves(row: int, col: int, piece: int, board: Chess, moves: List[Tuple[int, int]]):
    mods = [1, -1]
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


def rook_moves(row: int, col: int, piece: int, board: Chess, moves: List[Tuple[int, int]]):
    mods = [(1, 0), (-1, 0), (0, 1), (0, -1)]
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


def king_moves(row: int, col: int, piece: int, board: Chess, moves: List[Tuple[int, int]]):
    for i in range(-1, 2):
        for j in range(-1, 2):
            _row = row+i
            _col = col+j

            if is_outside_board(board.state[_row][_col]):
                continue

            if is_empty(board.state[_row][_col]) or (board.state[_row][_col] & COLOR_MASK) != (piece & COLOR_MASK):
                moves.append((_row, _col))


def pawn_moves(row: int, col: int, piece: int, board: Chess, moves: List[Tuple[int, int]]):
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


def knight_moves(row: int, col: int, piece: int, board: Chess, moves: List[Tuple[int, int]]):
    cords = [(1, 2),
             (1, -2),
             (2, 1),
             (2, -1),
             (-1, 2),
             (-1, -2),
             (-2, -1),
             (-2, 1)]

    for mods in cords:
        _row = row + mods[0]
        _col = col + mods[1]
        square = board.state[_row][_col]

        if is_outside_board(board.state[_row][_col]):
            continue

        if is_empty(square) or (square & COLOR_MASK) != piece & COLOR_MASK:
            moves.append((_row, _col))
