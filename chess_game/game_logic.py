import chess
import random

class ChessAI:
    def __init__(self):
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

    def evaluate_board(self, board):
        if board.is_checkmate():
            if board.turn:
                return -99999  # Black wins (White to move and checkmated)
            else:
                return 99999   # White wins

        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    evaluation += value
                else:
                    evaluation -= value

        # Simple positional heuristic: Central control (bonus for pieces in center)
        # Center squares: e4, d4, e5, d5 (28, 27, 36, 35)
        # Just a tiny bonus to encourage developing to center
        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        for square in center_squares:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    evaluation += 10
                else:
                    evaluation -= 10

        return evaluation

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        moves = list(board.legal_moves)

        # Move ordering: Check captures first for efficiency (simple heuristic)
        # Not strictly necessary for low depth but good practice.

        if maximizing_player:
            max_eval = -float('inf')
            for move in moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, board, depth=2):
        best_move = None
        moves = list(board.legal_moves)
        random.shuffle(moves) # Add randomness if evals are equal

        if board.turn == chess.WHITE: # Maximizing
            max_eval = -float('inf')
            for move in moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, -float('inf'), float('inf'), False)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
        else: # Minimizing
            min_eval = float('inf')
            for move in moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, -float('inf'), float('inf'), True)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

        return best_move

if __name__ == "__main__":
    # Test
    board = chess.Board()
    ai = ChessAI()
    move = ai.get_best_move(board, depth=1)
    print(f"Best move (depth 1): {move}")
