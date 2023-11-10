COLOR_MASK = 0b10000000
WHITE = 0b10000000
BLACK = 0b00000000

PIECE_MASK = 0b00000111
PAWN = 0b00000001
KNIGHT = 0b00000010
BISHOP = 0b00000011
ROOK = 0b00000100
QUEEN = 0b00000110
KING = 0b00000111

EMPTY = 0
SENTINEL = 0b11111111


def is_white(square: int) -> bool:
    return square & COLOR_MASK == WHITE


def is_black(square: int) -> bool:
    return not is_white(square)


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
