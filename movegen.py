from typing import List, Tuple
from defs import WHITE, is_empty, COLOR_MASK, is_white, is_outside_board, is_black, PIECE_MASK, PAWN, ROOK, BISHOP, KNIGHT, QUEEN, KING, BLACK, CastlingType, BOARD_END, BOARD_START, EN_PASSANT
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
    return False


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

        # check en passant
        if row == BOARD_START+3:
            if board.state[row][col-1] == (BLACK | PAWN | EN_PASSANT) and is_empty(board.state[row-1][col-1]):
                moves.append((row-1, col-1))
            if board.state[row][col+1] == (BLACK | PAWN | EN_PASSANT) and is_empty(board.state[row-1][col+1]):
                moves.append((row-1, col+1))
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

        # check en passant
        if row == BOARD_START+4:
            if board.state[row][col-1] == (WHITE | PAWN | EN_PASSANT) and is_empty(board.state[row+1][col-1]):
                moves.append((row+1, col-1))
            if board.state[row][col+1] == (WHITE | PAWN | EN_PASSANT) and is_empty(board.state[row+1][col+1]):
                moves.append((row+1, col+1))


KNIGHT_CORDS = [(1, 2),
                (1, -2),
                (2, 1),
                (2, -1),
                (-1, 2),
                (-1, -2),
                (-2, -1),
                (-2, 1)]


def knight_moves(row: int, col: int, piece: int, board: Chess, moves: List[Tuple[int, int]]):

    for mods in KNIGHT_CORDS:
        _row = row + mods[0]
        _col = col + mods[1]
        square = board.state[_row][_col]

        if is_outside_board(board.state[_row][_col]):
            continue

        if is_empty(square) or (square & COLOR_MASK) != piece & COLOR_MASK:
            moves.append((_row, _col))
