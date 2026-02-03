import subprocess
import sys
import os
import time
import atexit

class ChessModule:
    def __init__(self):
        self.process = None
        atexit.register(self.stop_server)

    def stop_server(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def start_game(self):
        if self.process and self.process.poll() is None:
            return "Chess server is already running. You can play at http://127.0.0.1:5000"

        # Path to app.py
        # Assuming we are running from root
        app_path = os.path.join(os.getcwd(), 'chess_game', 'app.py')

        if not os.path.exists(app_path):
            return f"Error: Could not find chess game at {app_path}"

        try:
            # Start the flask app
            self.process = subprocess.Popen(
                [sys.executable, app_path],
                cwd=os.getcwd(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(2) # Wait for startup

            if self.process.poll() is None:
                return "I've started the 3D Chess Game for you. Go to http://127.0.0.1:5000 to play!"
            else:
                return "Something went wrong while starting the chess server."
        except Exception as e:
            return f"Error starting chess module: {str(e)}"
