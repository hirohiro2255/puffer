from typing import List, Tuple
from defs import is_empty, COLOR_MASK, is_white, is_outside_board, is_black
from app import Chess


def king_moves(row: int, col: int, piece: int, board: Chess, moves: List[Tuple[int, int]]):
    for i in range(-1, 2):
        for j in range(-1, 2):
            r = row+i
            c = col+j

            if is_outside_board(board.state[r][c]):
                continue

            if is_empty(board.state[r][c]) or (board.state[r][c] & COLOR_MASK) != (piece & COLOR_MASK):
                moves.append((r, c))


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
        space = board.state[_row][_col]

        if is_outside_board(board.state[_row][_col]):
            continue

        if is_empty(space) or (space & COLOR_MASK) != piece & COLOR_MASK:
            moves.append((_row, _col))
