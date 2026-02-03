from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import chess
from game_logic import ChessAI
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game states: { room_id: { 'board': chess.Board(), 'white': session_id, 'black': session_id } }
games = {}
ai = ChessAI()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('join_game')
def on_join(data):
    room = data.get('room')
    mode = data.get('mode') # 'single', 'multi', 'local'

    join_room(room)

    if room not in games:
        games[room] = {
            'board': chess.Board(),
            'mode': mode,
            'white': None,
            'black': None
        }

    game = games[room]

    # Assign colors for multiplayer
    if mode == 'multi':
        if game['white'] is None:
            game['white'] = request.sid
            emit('color_assignment', {'color': 'white'}, room=request.sid)
        elif game['black'] is None:
            game['black'] = request.sid
            emit('color_assignment', {'color': 'black'}, room=request.sid)
        else:
            emit('spectator', {}, room=request.sid)
    else:
        # Local or Single player: User controls both or just White (handled by client logic mostly)
        emit('color_assignment', {'color': 'white'}, room=request.sid)

    emit('board_state', {'fen': game['board'].fen()}, room=room)

@socketio.on('make_move')
def on_move(data):
    room = data.get('room')
    move_uci = data.get('move')

    if room in games:
        board = games[room]['board']
        try:
            move = chess.Move.from_uci(move_uci)
            if move in board.legal_moves:
                board.push(move)

                game_over = board.is_game_over()
                result = board.result() if game_over else None

                emit('board_state', {
                    'fen': board.fen(),
                    'last_move': move_uci,
                    'game_over': game_over,
                    'result': result
                }, room=room)

                # Check for AI move trigger if Single Player
                if games[room]['mode'] == 'single' and not game_over and board.turn == chess.BLACK:
                     # This logic assumes User is White.
                     pass

            else:
                emit('invalid_move', {'move': move_uci}, room=request.sid)
        except ValueError:
             emit('error', {'message': 'Invalid move format'}, room=request.sid)

@socketio.on('request_ai_move')
def on_ai_move(data):
    room = data.get('room')
    difficulty = int(data.get('difficulty', 2))

    if room in games:
        board = games[room]['board']
        if not board.is_game_over():
            best_move = ai.get_best_move(board, depth=difficulty)
            if best_move:
                board.push(best_move)
                game_over = board.is_game_over()
                result = board.result() if game_over else None

                emit('board_state', {
                    'fen': board.fen(),
                    'last_move': best_move.uci(),
                    'game_over': game_over,
                    'result': result
                }, room=room)

@socketio.on('get_analysis')
def on_analysis(data):
    room = data.get('room')
    if room in games:
        board = games[room]['board']
        score = ai.evaluate_board(board)
        emit('analysis_result', {'score': score}, room=request.sid)

@socketio.on('get_hint')
def on_hint(data):
    room = data.get('room')
    if room in games:
        board = games[room]['board']
        if not board.is_game_over():
            best_move = ai.get_best_move(board, depth=3)
            if best_move:
                emit('hint_result', {'move': best_move.uci()}, room=request.sid)

@socketio.on('reset_game')
def on_reset(data):
    room = data.get('room')
    if room in games:
        games[room]['board'].reset()
        emit('board_state', {'fen': games[room]['board'].fen()}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=False, port=5000)
