import pytest
from playwright.sync_api import Page, expect
import threading
import time
from jumping_shell.app import app

# We need to run the app in a separate thread for the test
def run_app():
    app.run(port=5003, debug=False, use_reloader=False)

@pytest.fixture(scope="module", autouse=True)
def server():
    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()
    time.sleep(1) # Give it a second to start
    yield

def test_game_loads(page: Page):
    page.goto("http://127.0.0.1:5003")
    expect(page).to_have_title("Jumping Shell")
    expect(page.locator("#gameCanvas")).to_be_visible()
    expect(page.locator("#score")).to_contain_text("Score: 0")
