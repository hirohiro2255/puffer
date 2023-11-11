import unittest

from app import Chess, board_from_fen
from movegen import knight_moves, pawn_moves
from defs import WHITE, KNIGHT, PAWN, BLACK


class TestMoveGen(unittest.TestCase):
    # knight tests
    def test_knight_moves_empty_board(self):
        b = board_from_fen("8/8/8/8/3N4/8/8/8 w - - 0 1")
        ret = []
        row = 6
        col = 5
        knight_moves(row, col, WHITE | KNIGHT, b, ret)
        self.assertEqual(len(ret), 8)

    def test_moves_corner(self):
        b = board_from_fen("N7/8/8/8/8/8/8/8 w - - 0 1")
        ret = []
        row = 2
        col = 2
        knight_moves(row, col, WHITE | KNIGHT, b, ret)
        self.assertEqual(len(ret), 2)

    def test_knight_moves_with_other_pieces_with_capture(self):
        b = board_from_fen("8/8/5n2/3NQ3/2K2P2/8/8/8 w - - 0 1")
        ret = []
        row = 5
        col = 5
        knight_moves(row, col, WHITE | KNIGHT, b, ret)
        self.assertEqual(len(ret), 7)

    # pawn tests -- white pawn
    def test_white_pawn_start(self):
        b = board_from_fen("8/8/8/8/8/8/P7/8 w - - 0 1")
        ret = []
        row = 8
        col = 2
        pawn_moves(row, col, WHITE | PAWN, b, ret)
        self.assertEqual(len(ret), 2)

    def test_white_pawn_has_moved(self):
        b = board_from_fen("8/8/8/8/8/3P4/8/8 w - - 0 1")
        ret = []
        row = 7
        col = 5
        pawn_moves(row, col, WHITE | PAWN, b, ret)
        self.assertEqual(len(ret), 1)

    def test_white_pawn_cant_move_black_piece_block(self):
        b = board_from_fen("8/8/8/8/3r4/3P4/8/8 w - - 0 1")
        ret = []
        row = 7
        col = 5
        pawn_moves(row, col, WHITE | PAWN, b, ret)
        self.assertEqual(len(ret), 0)

    def test_white_pawn_cant_move_white_piece_block(self):
        b = board_from_fen("8/8/8/8/3K4/3P4/8/8 w - - 0 1")
        ret = []
        row = 7
        col = 5
        pawn_moves(row, col, WHITE | PAWN, b, ret)
        self.assertEqual(len(ret), 0)

    def test_white_pawn_with_two_captures_and_start(self):
        b = board_from_fen("8/8/8/8/8/n1q5/1P6/8 w - - 0 1")
        ret = []
        row = 8
        col = 3
        pawn_moves(row, col, WHITE | PAWN, b, ret)
        self.assertEqual(len(ret), 4)

    def test_white_pawn_with_one_capture(self):
        b = board_from_fen("8/8/Q1b5/1P6/8/8/8/8 w - - 0 1")
        ret = []
        row = 5
        col = 3
        pawn_moves(row, col, WHITE | PAWN, b, ret)
        self.assertEqual(len(ret), 2)

    def test_white_pawn_double_push_piece_in_front(self):
        b = board_from_fen("8/8/8/8/8/b7/P7/8 w - - 0 1")
        ret = []
        row = 8
        col = 2
        pawn_moves(row, col, WHITE | PAWN, b, ret)
        self.assertEqual(len(ret), 0)

    # pawn tests -- black pawn
    def test_black_pawn_double_push(self):
        b = board_from_fen("8/p7/8/8/8/8/8/8 w - - 0 1")
        ret = []
        row = 3
        col = 2
        pawn_moves(row, col, BLACK | PAWN, b, ret)
        self.assertEqual(len(ret), 2)

    def test_black_pawn_has_moved(self):
        b = board_from_fen("8/8/8/3p4/8/8/8/8 w - - 0 1")
        ret = []
        row = 5
        col = 5
        pawn_moves(row, col, BLACK | PAWN, b, ret)
        self.assertEqual(len(ret), 1)

    def test_black_pawn_cant_move_white_piece_block(self):
        b = board_from_fen("8/3p4/3R4/8/8/8/8/8 w - - 0 1")
        ret = []
        row = 3
        col = 5
        pawn_moves(row, col, BLACK | PAWN, b, ret)
        self.assertEqual(len(ret), 0)

    def test_black_pawn_with_two_captures_and_start(self):
        b = board_from_fen("8/3p4/2R1R3/8/8/8/8/8 w - - 0 1")
        ret = []
        row = 3
        col = 5
        pawn_moves(row, col, BLACK | PAWN, b, ret)
        self.assertEqual(len(ret), 4)

    def test_black_pawn_with_one_capture(self):
        b = board_from_fen("8/3p4/3qR3/8/8/8/8/8 w - - 0 1")
        ret = []
        row = 3
        col = 5
        pawn_moves(row, col, BLACK | PAWN, b, ret)
        self.assertEqual(len(ret), 1)


if __name__ == '__main__':
    unittest.main()
