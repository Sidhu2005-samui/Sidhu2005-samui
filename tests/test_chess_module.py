import unittest
import time
import urllib.request
from ava.modules.chess import ChessModule

class TestChessModule(unittest.TestCase):
    def setUp(self):
        self.chess = ChessModule()

    def tearDown(self):
        # Stop the server explicitly
        self.chess.stop_server()
        # Ensure process is killed
        if self.chess.process and self.chess.process.poll() is None:
            self.chess.process.kill()

        # Wait for port to be released
        time.sleep(1)

    def test_start_game(self):
        # Start the game
        result = self.chess.start_game()

        # Check output message
        self.assertIn("started the 3D Chess Game", result)
        self.assertIn("http://127.0.0.1:5000", result)

        # Verify server is actually running and responding
        try:
            with urllib.request.urlopen("http://127.0.0.1:5000/", timeout=2) as response:
                self.assertEqual(response.status, 200)
        except Exception as e:
            self.fail(f"Server is not responding: {e}")

        # Test that calling start_game again returns "already running"
        result2 = self.chess.start_game()
        self.assertIn("already running", result2)

if __name__ == "__main__":
    unittest.main()
