from defs import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING


def get_piece_from_fen_string_char(piece: str) -> int | None:
    match piece:
        case 'r':
            return BLACK | ROOK
        case 'n':
            return BLACK | KNIGHT
        case 'b':
            return BLACK | BISHOP
        case 'q':
            return BLACK | QUEEN
        case 'k':
            return BLACK | KING
        case 'p':
            return BLACK | PAWN
        case 'R':
            return WHITE | ROOK
        case 'N':
            return WHITE | KNIGHT
        case 'B':
            return WHITE | BISHOP
        case 'Q':
            return WHITE | QUEEN
        case 'K':
            return WHITE | KING
        case 'P':
            return WHITE | PAWN
        case _:
            return None


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
