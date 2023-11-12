from enum import Enum
from typing import Tuple
"""
    Example Piece: 0b11000101
    1st bit: Color 1 = White, 0 = Black
    2nd bit: Whether this piece has moved yet, 0=has not moved, 1=has moved
    3-5 bit: Unused
    6-8 bit: Piece identifier
"""

MOVED_MASK = 0b01000000


COLOR_MASK = 0b10000000
WHITE = 0b10000000
BLACK = 0b00000000

PIECE_MASK = 0b00000111
EN_PASSANT = 0b01000000
PAWN = 0b00000001
KNIGHT = 0b00000010
BISHOP = 0b00000011
ROOK = 0b00000100
QUEEN = 0b00000110
KING = 0b00000111

EMPTY = 0
SENTINEL = 0b11111111


def is_white(square: int) -> bool:
    return not is_empty(square) and square & COLOR_MASK == WHITE


def is_black(square: int) -> bool:
    return not is_empty(square) and square & COLOR_MASK == BLACK


def is_pawn(square: int) -> bool:
    return square & PIECE_MASK == PAWN


def is_knight(square: int) -> bool:
    return square & PIECE_MASK == KNIGHT


def is_bishop(square: int) -> bool:
    return square & PIECE_MASK == BISHOP


def is_rook(square: int) -> bool:
    return square & PIECE_MASK == ROOK


def is_queen(square: int) -> bool:
    return square & PIECE_MASK == QUEEN


def is_king(square: int) -> bool:
    return square & PIECE_MASK == KING


def is_empty(square: int) -> bool:
    return square == EMPTY


def is_outside_board(square: int) -> bool:
    return square == SENTINEL


DEFAULT_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
KIWI_PETE = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1'
POSITION_3 = '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1'

BOARD_START = 2
BOARD_END = 10


def has_moved(square: int) -> bool:
    return square & MOVED_MASK != 0


def pawn_did_double_move(pawn: int) -> bool:
    return pawn & EN_PASSANT != 0


class CastlingType(Enum):
    WHITE_KING_SIDE = 1
    WHITE_QUEEN_SIDE = 2
    BLACK_KING_SIDE = 4
    BLACK_QUEEN_SIDE = 8


def algebraic_pairs_to_board_position(pair: str) -> Tuple[int, int]:

    if len(pair) != 2:
        raise ValueError('Algebraic position str length is wrong')

    c = pair[0]
    r = pair[1]
    col = None
    if c == "a":
        col = 0
    elif c == "b":
        col = 1
    elif c == "c":
        col = 2
    elif c == "d":
        col = 3
    elif c == "e":
        col = 4
    elif c == "f":
        col = 5
    elif c == "g":
        col = 6
    elif c == "h":
        col = 7
    else:
        raise ValueError("Could not parse column of algebraic position")

    row = BOARD_END - int(r)
    if row < BOARD_START or row >= BOARD_END:
        raise ValueError('Could not parse row of algebraic position')

    return (row, col+BOARD_START)
