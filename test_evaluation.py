import unittest
from evaluation import PIECE_VALUES
from defs import PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING


class TestEvaluation(unittest.TestCase):
    def test_correct_values(self):
        self.assertEqual(PIECE_VALUES[PAWN], 100)
        self.assertEqual(PIECE_VALUES[KNIGHT], 320)
        self.assertEqual(PIECE_VALUES[BISHOP], 330)
        self.assertEqual(PIECE_VALUES[ROOK], 500)
        self.assertEqual(PIECE_VALUES[QUEEN], 900)
        self.assertEqual(PIECE_VALUES[KING], 20000)


if __name__ == '__main__':
    unittest.main()
