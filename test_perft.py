import unittest
from app import board_from_fen
from movegen import generate_moves_test


class TestPerft(unittest.TestCase):
    def test_perft_position_6(self):
        move_states = [0] * 5
        b = board_from_fen(
            "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
        generate_moves_test(b, 0, 2, move_states)
        self.assertEqual(move_states[0], 46)
        self.assertEqual(move_states[1], 2079)
        # self.assertEqual(move_states[2], 89890) == SLOW

    def test_peft_position_5(self):
        move_states = [0] * 5
        b = board_from_fen(
            "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
        generate_moves_test(b, 0, 2, move_states)
        self.assertEqual(move_states[0], 44)
        self.assertEqual(move_states[1], 1486)

    def test_perft_position_4_mirrored(self):
        move_states = [0] * 5
        b = board_from_fen(
            "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1")
        generate_moves_test(b, 0, 2, move_states)
        self.assertTrue(move_states[0], 6)
        self.assertTrue(move_states[1], 264)

    def test_perft_position_4(self):
        move_states = [0] * 5
        b = board_from_fen(
            "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
        generate_moves_test(b, 0, 2, move_states)
        self.assertTrue(move_states[0], 6)
        self.assertTrue(move_states[1], 264)

    def test_perft_position_3(self):
        move_states = [0] * 5
        b = board_from_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1")
        generate_moves_test(b, 0, 3, move_states)
        self.assertEqual(move_states[0], 14)
        self.assertEqual(move_states[1], 191)
        self.assertEqual(move_states[2], 2812)

    def test_perft_position_2(self):
        move_states = [0] * 5
        b = board_from_fen(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")
        generate_moves_test(b, 0, 3, move_states)
        self.assertEqual(move_states[0], 48)

    def test_perft_position_1(self):
        move_states = [0] * 5
        b = board_from_fen(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        generate_moves_test(b, 0, 3, move_states)
        self.assertEqual(move_states[0], 20)
        self.assertEqual(move_states[1], 400)
        self.assertEqual(move_states[2], 8902)
        # self.assertEqual(move_states[3], 197281)
