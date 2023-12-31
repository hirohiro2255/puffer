import unittest
from app import Chess, board_from_fen
from defs import is_white, is_black, WHITE, BLACK, KNIGHT, BISHOP, ROOK, QUEEN, KING, PAWN, is_pawn, is_knight, is_bishop, is_rook, is_queen, is_king, is_empty, is_outside_board, EMPTY, SENTINEL, has_moved, MOVED_MASK, pawn_did_double_move, EN_PASSANT, algebraic_pairs_to_board_position, BOARD_START, BOARD_END, board_position_to_algebraic_pair


class TestChessClass(unittest.TestCase):

    def test_points_to_long_algebraic_position(self):
        res = board_position_to_algebraic_pair((2,2))
        self.assertEqual(res, "a8")

        res = board_position_to_algebraic_pair((4,6))
        self.assertEqual(res, "e6")

    def test_correct_en_passant_privileges(self):
        b = board_from_fen(
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e4 0 1")
        self.assertEqual(b.pawn_double_move[0], BOARD_START+4)
        self.assertEqual(b.pawn_double_move[1], BOARD_START+4)

    def test_correct_en_passant_privileges_black(self):
        b = board_from_fen(
            "rnbqkbnr/ppppppp1/8/7p/8/8/PPPPPPPP/RNBQKBNR w KQkq h5 0 1")
        self.assertEqual(b.pawn_double_move[0], BOARD_START+3)
        self.assertEqual(b.pawn_double_move[1], BOARD_START+7)

    def test_algebraic_translation_correct(self):
        res = algebraic_pairs_to_board_position("a8")
        self.assertEqual(res[0], BOARD_START)
        self.assertEqual(res[1], BOARD_START)

        res = algebraic_pairs_to_board_position("h1")
        self.assertEqual(res[0], BOARD_END-1)
        self.assertEqual(res[1], BOARD_END-1)

        res = algebraic_pairs_to_board_position("a6")
        self.assertEqual(res[0], BOARD_START+2)
        self.assertEqual(res[1], BOARD_START)

        res = algebraic_pairs_to_board_position("c5")
        self.assertEqual(res[0], BOARD_START+3)
        self.assertEqual(res[1], BOARD_START+2)

    def test_algebraic_translation_value_error(self):
        res = algebraic_pairs_to_board_position("z1")
        self.assertIsNone(res)

    def test_algebraic_translation_value_too_long(self):
        res = algebraic_pairs_to_board_position("a11")
        self.assertIsNone(res)

    def test_correct_castling_privileges(self):
        b = board_from_fen(
            "6rk/1b4np/5pp1/1p6/8/1P3NP1/1B3P1P/5RK1 w KQkq - 0 1")
        self.assertTrue(b.white_king_side_castle)
        self.assertTrue(b.white_queen_side_castle)
        self.assertTrue(b.black_king_side_castle)
        self.assertTrue(b.black_queen_side_castle)

        b = board_from_fen("6rk/1b4np/5pp1/1p6/8/1P3NP1/1B3P1P/5RK1 w - - 0 1")
        self.assertTrue(not b.white_king_side_castle)
        self.assertTrue(not b.white_queen_side_castle)
        self.assertTrue(not b.black_king_side_castle)
        self.assertTrue(not b.black_queen_side_castle)

        b = board_from_fen(
            "6rk/1b4np/5pp1/1p6/8/1P3NP1/1B3P1P/5RK1 w Kq - 0 1")
        self.assertTrue(not b.black_king_side_castle)
        self.assertTrue(b.black_queen_side_castle)
        self.assertTrue(b.white_king_side_castle)
        self.assertTrue(not b.white_queen_side_castle)

    def test_correct_king_location(self):
        b = board_from_fen(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(b.black_king_location, (2, 6))
        self.assertEqual(b.white_king_location, (9, 6))

    def test_correct_king_location_two(self):
        b = board_from_fen(
            "6rk/1b4np/5pp1/1p6/8/1P3NP1/1B3P1P/5RK1 w KQkq - 0 1")
        self.assertEqual(b.black_king_location, (2, 9))
        self.assertEqual(b.white_king_location, (9, 8))

    def test_empty_board(self):
        b = board_from_fen("8/8/8/8/8/8/8/8 w KQkq - 0 1")
        for i in range(2, 10):
            for j in range(2, 10):
                self.assertEqual(b.state[i][j], EMPTY)

    def test_start_pos(self):
        b = board_from_fen()
        self.assertEqual(b.state[2][2], BLACK | ROOK)
        self.assertEqual(b.state[2][3], BLACK | KNIGHT)
        self.assertEqual(b.state[2][4], BLACK | BISHOP)
        self.assertEqual(b.state[2][5], BLACK | QUEEN)
        self.assertEqual(b.state[2][6], BLACK | KING)
        self.assertEqual(b.state[2][7], BLACK | BISHOP)
        self.assertEqual(b.state[2][8], BLACK | KNIGHT)
        self.assertEqual(b.state[2][9], BLACK | ROOK)

        for i in range(2, 10):
            self.assertEqual(b.state[3][i], BLACK | PAWN)

        for i in range(4, 8):
            for j in range(2, 10):
                self.assertEqual(b.state[i][j], EMPTY)

        self.assertEqual(b.state[9][2], WHITE | ROOK)
        self.assertEqual(b.state[9][3], WHITE | KNIGHT)
        self.assertEqual(b.state[9][4], WHITE | BISHOP)
        self.assertEqual(b.state[9][5], WHITE | QUEEN)
        self.assertEqual(b.state[9][6], WHITE | KING)
        self.assertEqual(b.state[9][7], WHITE | BISHOP)
        self.assertEqual(b.state[9][8], WHITE | KNIGHT)
        self.assertEqual(b.state[9][9], WHITE | ROOK)

        for i in range(2, 10):
            self.assertEqual(b.state[8][i], WHITE | PAWN)

    def test_correct_starting_player(self):
        b = board_from_fen(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(b.to_move, WHITE)
        b = board_from_fen(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqual(b.to_move, BLACK)

    def test_random_pos(self):
        b = board_from_fen(
            "4R1B1/1kp5/1B1Q4/1P5p/1p2p1pK/8/3pP3/4N1b1 w - - 0 1")
        self.assertEqual(b.state[2][6], WHITE | ROOK)
        self.assertEqual(b.state[2][8], WHITE | BISHOP)
        self.assertEqual(b.state[3][3], BLACK | KING)
        self.assertEqual(b.state[3][4], BLACK | PAWN)
        self.assertEqual(b.state[4][3], WHITE | BISHOP)
        self.assertEqual(b.state[4][5], WHITE | QUEEN)
        self.assertEqual(b.state[5][3], WHITE | PAWN)
        self.assertEqual(b.state[5][9], BLACK | PAWN)
        self.assertEqual(b.state[6][3], BLACK | PAWN)
        self.assertEqual(b.state[6][6], BLACK | PAWN)
        self.assertEqual(b.state[6][8], BLACK | PAWN)
        self.assertEqual(b.state[6][9], WHITE | KING)
        self.assertEqual(b.state[8][5], BLACK | PAWN)
        self.assertEqual(b.state[8][6], WHITE | PAWN)
        self.assertEqual(b.state[9][6], WHITE | KNIGHT)
        self.assertEqual(b.state[9][8], BLACK | BISHOP)

    def test_bad_fen_string(self):
        with self.assertRaises(ValueError):
            b = board_from_fen('this is bad string')

    def test_bad_fen_string_bad_char(self):
        with self.assertRaises(ValueError):
            b = board_from_fen(
                "rnbqkbnH/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def test_bad_fen_string_too_many_chars(self):
        with self.assertRaises(IndexError):
            b = board_from_fen(
                "rnbqkbnrrrrr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

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

        self.assertTrue(pawn_did_double_move(WHITE | PAWN | EN_PASSANT))
        self.assertTrue(pawn_did_double_move(BLACK | PAWN | EN_PASSANT))
        self.assertTrue(not pawn_did_double_move(WHITE | PAWN))
        self.assertTrue(not pawn_did_double_move(BLACK | PAWN))

        self.assertTrue(has_moved(WHITE | PAWN | MOVED_MASK))
        self.assertTrue(not has_moved(WHITE | PAWN))


if __name__ == '__main__':
    unittest.main()
