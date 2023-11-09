from defs import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING


def get_piece_character(piece: int) -> str:
    if piece == WHITE | PAWN:
        return '♙'
    elif piece == WHITE | KNIGHT:
        return '♘'
    elif piece == WHITE | BISHOP:
        return '♗'
    elif piece == WHITE | ROOK:
        return '♖'
    elif piece == WHITE | QUEEN:
        return '♕'
    elif piece == WHITE | KING:
        return '♔'
    elif piece == BLACK | PAWN:
        return '♟︎'
    elif piece == BLACK | KNIGHT:
        return '♞'
    elif piece == BLACK | BISHOP:
        return '♝'
    elif piece == BLACK | ROOK:
        return '♜'
    elif piece == BLACK | QUEEN:
        return '♛'
    elif piece == BLACK | KING:
        return '♚'

    return '.'
