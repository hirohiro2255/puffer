import unittest

from app import Chess, board_from_fen
from movegen import knight_moves, pawn_moves, king_moves, rook_moves, bishop_moves, queen_moves, get_moves, is_check
from defs import WHITE, KNIGHT, PAWN, BLACK, KING, ROOK, BISHOP, QUEEN, BOARD_START, BOARD_END, is_white


class TestMoveGen(unittest.TestCase):

    def test_queen_checks(self):
        b = board_from_fen("8/8/8/8/3k1Q2/8/8/8 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("8/8/2k5/8/8/8/6Q1/8 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("8/8/2K5/8/3q4/8/8/8 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

        b = board_from_fen("8/8/1K6/2Q5/3q4/8/8/8 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

        b = board_from_fen("8/5Q2/1K6/8/3q4/8/8/8 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

        b = board_from_fen("8/5Q2/1K6/1P6/8/8/1q6/8 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

        b = board_from_fen("8/2P2Q2/1K6/8/8/8/1q6/8 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

    def test_bishop_checks(self):
        b = board_from_fen("8/8/8/1B6/8/8/8/5k2 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("8/8/2B1B3/1B3B2/1B1k1B2/8/8/8 w - - 0 1")
        self.assertTrue(not is_check(b, BLACK))

        b = board_from_fen("8/8/8/8/5k2/8/8/2B5 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("8/8/8/8/5k2/4n3/8/2B5 w - - 0 1")
        self.assertTrue(not is_check(b, BLACK))

        b = board_from_fen("8/8/8/8/3K4/8/8/6b1 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

        b = board_from_fen("8/8/8/8/3K4/4r3/8/6b1 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

        b = board_from_fen("8/8/8/8/3K4/4r3/8/b5b1 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

        b = board_from_fen("8/8/8/8/3K4/2P1r3/8/b5b1 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

    # Rook checks
    def test_rook_checks(self):
        b = board_from_fen("8/8/8/R3k3/8/8/8/8 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("8/8/8/R1r1k3/8/8/8/8 w - - 0 1")
        self.assertTrue(not is_check(b, BLACK))

        b = board_from_fen("8/8/8/R1r1k3/8/8/8/4R3 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("4R3/8/8/R1r5/8/8/8/4k3 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("8/8/8/R1r5/8/8/7R/4k3 w - - 0 1")
        self.assertTrue(not is_check(b, BLACK))

        b = board_from_fen("4R3/8/8/8/8/3r4/R3K2R/2r1Rr2 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

        b = board_from_fen("4R3/8/8/8/4K3/3r4/R6R/2r1rr2 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

        b = board_from_fen("4R3/8/8/8/4K2r/3r4/R6R/2r2r2 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

        b = board_from_fen("4r3/8/8/4B3/r2QKP1r/3rR3/R6R/2r1rr2 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

    def test_check_sanity_test(self):
        b = board_from_fen("8/8/8/8/3K4/8/8/8 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

    def test_knight_checks(self):
        b = board_from_fen("8/8/4n3/8/3K4/8/8/8 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

        b = board_from_fen("8/8/8/8/8/8/1RK5/nRB5 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

        b = board_from_fen("8/8/8/8/3k4/5N2/8/8 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("8/8/8/8/3k4/5n2/8/7N w - - 0 1")
        self.assertTrue(not is_check(b, BLACK))

        b = board_from_fen("8/8/2N5/8/3k4/5n2/8/7N w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

    def test_pawn_checks(self):
        b = board_from_fen("8/8/8/4k3/3P4/8/8/8 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("8/8/8/4k3/5P2/8/8/8 w - - 0 1")
        self.assertTrue(is_check(b, BLACK))

        b = board_from_fen("8/8/8/4k3/4P3/8/8/8 w - - 0 1")
        self.assertTrue(not is_check(b, BLACK))

        b = board_from_fen("8/8/3PPP2/4k3/8/8/8/8 w - - 0 1")
        self.assertTrue(not is_check(b, BLACK))

        b = board_from_fen("8/8/8/8/8/5p2/6K1/8 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

        b = board_from_fen("8/8/8/8/8/7p/6K1/8 w - - 0 1")
        self.assertTrue(is_check(b, WHITE))

        b = board_from_fen("8/8/8/8/8/6p1/6K1/8 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

        b = board_from_fen("8/8/8/8/8/6K1/5ppp/8 w - - 0 1")
        self.assertTrue(not is_check(b, WHITE))

    def teste_perft_test_depth_one(self):
        moves = []
        b = board_from_fen(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        for i in range(BOARD_START, BOARD_END):
            for j in range(BOARD_START, BOARD_END):
                if is_white(b.state[i][j]):
                    get_moves(i, j, b.state[i][j], b, moves)

        self.assertEqual(len(moves), 20)

    # queen tests
    def test_white_queen_empty_board(self):
        b = board_from_fen("8/8/8/8/3Q4/8/8/8 w - - 0 1")
        ret = []
        row = 6
        col = 5
        queen_moves(row, col, WHITE | QUEEN, b, ret)
        self.assertEqual(len(ret), 27)

    def test_white_queen_cant_move(self):
        b = board_from_fen("8/8/8/2NBR3/2PQR3/2RRR3/8/8 w - - 0 1")
        ret = []
        row = 6
        col = 5
        queen_moves(row, col, WHITE | QUEEN, b, ret)
        self.assertEqual(len(ret), 0)

    def test_white_queen_hits_other_pieces(self):
        b = board_from_fen("8/6r1/8/8/3Q4/5N2/8/6P1 w - - 0 1")
        ret = []
        row = 6
        col = 5
        queen_moves(row, col, WHITE | QUEEN, b, ret)
        self.assertEqual(len(ret), 25)

    # bishop tests
    def test_black_bishop_center_empty_board(self):
        b = board_from_fen("8/8/8/3b4/8/8/8/8 w - - 0 1")
        ret = []
        row = 5
        col = 5
        bishop_moves(row, col, BLACK | BISHOP, b, ret)
        self.assertEqual(len(ret), 13)

    def test_black_bishop_center_with_captures(self):
        b = board_from_fen("6P1/8/8/3b4/8/1R6/8/3Q4 w - - 0 1")
        ret = []
        row = 5
        col = 5
        bishop_moves(row, col, BLACK | BISHOP, b, ret)
        self.assertEqual(len(ret), 12)

    def test_black_bishop_center_with_captures_and_black_pieces(self):
        b = board_from_fen("6P1/8/2Q5/3b4/2k1n3/1R6/8/b2Q4 w - - 0 1")
        ret = []
        row = 5
        col = 5
        bishop_moves(row, col, BLACK | BISHOP, b, ret)
        self.assertEqual(len(ret), 4)

    def test_white_bishop_center_with_captures_and_white_pieces(self):
        b = board_from_fen("8/8/8/4r3/5B2/8/3Q4/8 w - - 0 1")
        ret = []
        row = 6
        col = 7
        bishop_moves(row, col, WHITE | BISHOP, b, ret)
        self.assertEqual(len(ret), 6)

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
        rook_moves(row, col, BLACK | ROOK, b, ret)
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
