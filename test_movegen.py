import unittest

from app import Chess, board_from_fen
from movegen import knight_moves, pawn_moves, king_moves, rook_moves, bishop_moves
from defs import WHITE, KNIGHT, PAWN, BLACK, KING, ROOK, BISHOP


class TestMoveGen(unittest.TestCase):

    # bishop tests
    def test_black_bishop_center_empty_board(self):
        b = board_from_fen("8/8/8/3b4/8/8/8/8 w - - 0 1")
        ret = []
        row = 5
        col = 5
        bishop_moves(row,col,BLACK|BISHOP,b,ret)
        self.assertEqual(len(ret), 13)

    # rook tests
    def test_rook_center_of_empty_board(self):
        b = board_from_fen("8/8/8/8/3R4/8/8/8 w - - 0 1")
        ret = []
        row = 6
        col = 5
        rook_moves(row, col, WHITE | ROOK, b, ret)
        self.assertEqual(len(ret), 14)

    def test_rook_center_of_board(self):
        b = board_from_fen("8/8/8/3q4/2kRp3/3b4/8/8 w - - 0 1")
        ret = []
        row = 6
        col = 5
        rook_moves(row, col, WHITE | ROOK, b, ret)
        self.assertEqual(len(ret), 4)

    def test_rook_center_of_board_with_white_pieces(self):
        b = board_from_fen("7p/3N4/8/4n3/2kR4/3b4/8/8 w - - 0 1")
        ret = []
        row = 6
        col = 5
        rook_moves(row, col, WHITE | ROOK, b, ret)
        self.assertEqual(len(ret), 8)

    def test_rook_corner(self):
        b = board_from_fen("7p/3N4/8/4n3/2kR4/3b4/8/8 w - - 0 1")
        ret = []
        row = 9
        col = 9
        rook_moves(row, col, WHITE | ROOK, b, ret)
        self.assertEqual(len(ret), 14)

    def test_black_rook_center_of_board_with_white_pieces(self):
        b = board_from_fen("7p/3N4/8/4n3/2kR4/3b4/8/8 w - - 0 1")
        ret = []
        row = 6
        col = 5
        rook_moves(row,col,BLACK|ROOK,b,ret)
        self.assertEqual(len(ret), 7)


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

    # piece test -- king
    def test_king_empty_board_center(self):
        b = board_from_fen("8/8/8/8/3K4/8/8/8 w - - 0 1")
        ret = []
        row = 5
        col = 6
        king_moves(row, col, WHITE | KING, b, ret)
        self.assertEqual(len(ret), 8)

    def test_king_start_pos(self):
        b = board_from_fen("8/8/8/8/8/8/8/4K3 w - - 0 1")
        ret = []
        row = 9
        col = 6
        king_moves(row, col, WHITE | KING, b, ret)
        self.assertEqual(len(ret), 5)

    def test_king_start_pos_other_pieces(self):
        b = board_from_fen("8/8/8/8/8/8/3Pn3/3QKB2 w - - 0 1")
        ret = []
        row = 9
        col = 6
        king_moves(row, col, WHITE | KING, b, ret)
        self.assertEqual(len(ret), 2)

    def test_king_black_other_pieces(self):
        b = board_from_fen("8/8/8/8/8/3Pn3/3QkB2/3R1q2 w - - 0 1")
        ret = []
        row = 8
        col = 6
        king_moves(row, col, BLACK | KING, b, ret)
        self.assertEqual(len(ret), 6)


if __name__ == '__main__':
    unittest.main()
