import chess
from chess_game.game_logic import ChessAI

def test_evaluate_board_start_pos():
    ai = ChessAI()
    board = chess.Board()
    # Initial position should evaluate to 0
    assert ai.evaluate_board(board) == 0

def test_evaluate_board_material_advantage():
    ai = ChessAI()
    board = chess.Board()
    # Remove black queen
    board.remove_piece_at(chess.D8)

    score = ai.evaluate_board(board)
    # White should be winning significantly. Queen is 900.
    assert score == 900

def test_evaluate_board_center_control():
    ai = ChessAI()
    board = chess.Board()
    # Place white pawn on e4
    board.clear()
    board.set_piece_at(chess.E4, chess.Piece(chess.PAWN, chess.WHITE))

    # Material: 100
    # Center bonus: 10
    # Total: 110
    assert ai.evaluate_board(board) == 110

def test_evaluate_board_mixed():
    ai = ChessAI()
    board = chess.Board()
    # White pawn on e4, Black pawn on d5
    board.clear()
    board.set_piece_at(chess.E4, chess.Piece(chess.PAWN, chess.WHITE))
    board.set_piece_at(chess.D5, chess.Piece(chess.PAWN, chess.BLACK))

    # White: 100 + 10 = 110
    # Black: 100 + 10 = 110
    # Total: 0
    assert ai.evaluate_board(board) == 0

if __name__ == "__main__":
    test_evaluate_board_start_pos()
    test_evaluate_board_material_advantage()
    test_evaluate_board_center_control()
    test_evaluate_board_mixed()
    print("All tests passed!")
