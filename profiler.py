import cProfile
from app import board_from_fen, generate_moves_test

if __name__ == "__main__":
    move_states = [0] * 5
    b = board_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    cProfile.run("generate_moves_test(b, 0, 3, move_states)")

