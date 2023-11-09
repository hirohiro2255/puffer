import unittest
from app import Chess
from defs import is_white, is_black, WHITE, BLACK, KNIGHT, BISHOP, ROOK, QUEEN, KING, PAWN, is_pawn, is_knight, is_bishop, is_rook, is_queen, is_king, is_empty, is_outside_board, EMPTY, SENTINEL


class TestChessClass(unittest.TestCase):
    def test_piece_recognized(self):
        self.assertTrue(is_white(WHITE | BISHOP))
        self.assertTrue(is_white(WHITE | ROOK))
        self.assertTrue(is_white(WHITE | KING))
        self.assertTrue(is_white(WHITE | PAWN))

        self.assertTrue(is_black(BLACK | BISHOP))
        self.assertTrue(is_black(BLACK | ROOK))
        self.assertTrue(is_black(BLACK | KING))
        self.assertTrue(is_black(BLACK | PAWN))

        self.assertTrue(is_pawn(WHITE | PAWN))
        self.assertTrue(is_pawn(BLACK | PAWN))
        self.assertTrue(not is_pawn(WHITE | ROOK))

        self.assertTrue(is_knight(WHITE | KNIGHT))
        self.assertTrue(is_knight(BLACK | KNIGHT))
        self.assertTrue(not is_knight(BLACK | QUEEN))

        self.assertTrue(is_bishop(WHITE | BISHOP))
        self.assertTrue(is_bishop(BLACK | BISHOP))
        self.assertTrue(not is_bishop(WHITE | ROOK))

        self.assertTrue(is_queen(WHITE | QUEEN))
        self.assertTrue(is_queen(BLACK | QUEEN))
        self.assertTrue(not is_queen(WHITE | PAWN))

        self.assertTrue(is_king(WHITE | KING))
        self.assertTrue(is_king(BLACK | KING))
        self.assertTrue(not is_king(WHITE | QUEEN))

        self.assertTrue(is_empty(EMPTY))
        self.assertTrue(not is_empty(WHITE | KING))

        self.assertTrue(is_outside_board(SENTINEL))
        self.assertTrue(not is_outside_board(EMPTY))
        self.assertTrue(not is_outside_board(WHITE | KING))


if __name__ == '__main__':
    unittest.main()
