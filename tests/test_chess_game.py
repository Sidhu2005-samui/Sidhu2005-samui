import unittest
import chess
from chess_game.game_logic import ChessAI

class TestChessAI(unittest.TestCase):
    def setUp(self):
        self.ai = ChessAI()

    def test_evaluate_checkmate(self):
        # Fool's mate
        board = chess.Board()
        board.push(chess.Move.from_uci("f2f3"))
        board.push(chess.Move.from_uci("e7e5"))
        board.push(chess.Move.from_uci("g2g4"))
        board.push(chess.Move.from_uci("d8h4"))
        self.assertTrue(board.is_checkmate())

        # White turn? No, it's White to move and checkmated.
        self.assertTrue(board.turn == chess.WHITE)

        score = self.ai.evaluate_board(board)
        self.assertEqual(score, -99999)

    def test_evaluate_stalemate(self):
        board = chess.Board("4k3/4P3/4K3/8/8/8/8/8 b - - 0 1")
        self.assertTrue(board.is_stalemate())

        score = self.ai.evaluate_board(board)
        self.assertEqual(score, 0)

    def test_evaluate_insufficient_material(self):
        board = chess.Board("8/8/8/8/8/3k4/3K4/8 w - - 0 1")
        self.assertTrue(board.is_insufficient_material())

        score = self.ai.evaluate_board(board)
        self.assertEqual(score, 0)

    def test_evaluate_75_moves(self):
        # Simulate 75 moves without pawn move or capture
        board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # Add a piece for White so eval is positive
        board.set_piece_at(chess.E3, chess.Piece(chess.PAWN, chess.WHITE))

        # Set 75-move rule condition
        board.halfmove_clock = 150

        # Optimized code should detect game over and return 0
        score = self.ai.evaluate_board(board)
        self.assertEqual(score, 0)

    def test_evaluate_normal(self):
        board = chess.Board()
        score = self.ai.evaluate_board(board)
        # Start position score is 0
        self.assertEqual(score, 0)

if __name__ == "__main__":
    unittest.main()
