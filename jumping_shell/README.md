# Jumping Shell - 2D Platformer

A 2D platformer game built with Python (Flask) and JavaScript (HTML5 Canvas). The game features a shell character that jumps, collects items, avoids obstacles, and progresses through 50-100 procedural levels.

## Features
- **Procedural Level Generation**: Levels get longer and harder as you progress (1-100).
- **Physics Engine**: Custom AABB collision detection, gravity, and jumping mechanics.
- **Entities**: Platforms, Coins (Score), Spikes (Obstacles), and Exits.
- **Responsive UI**: Score, Lives, and Level indicators.

## Prerequisites
- Python 3.x
- Flask

## Installation & Running
1.  **Navigate to the directory**:
    ```bash
    cd jumping_shell
    ```

2.  **Run the Flask application**:
    ```bash
    python app.py
    ```

3.  **Play**:
    Open your web browser and go to `http://127.0.0.1:5001`.

## How It Was Built (Step-by-Step Guide)

### 1. Project Structure
We started by setting up a standard Flask project structure:
- `app.py`: The backend server.
- `templates/index.html`: The frontend HTML.
- `static/`: Contains `style.css` and `game.js`.

### 2. The Backend (Flask)
We created a minimal Flask app in `app.py` that serves the `index.html` file. This allows us to easily expand the game with backend features (like high scores) later.

### 3. The Frontend (HTML/CSS)
- **HTML**: Created a container with a `<canvas>` element for rendering the game.
- **CSS**: Styled the canvas to be centered and added an overlay for UI elements (Score, Lives).

### 4. Game Engine (JavaScript)
The core logic resides in `static/game.js`.
- **Game Loop**: Uses `requestAnimationFrame` for smooth rendering.
- **Classes**:
    - `Game`: Manages state (Start, Playing, GameOver), score, and levels.
    - `Player`: Handles physics (velocity, gravity, collision resolution).
    - `LevelGenerator`: The magic behind the "infinite" content. It generates a 2D map array based on the current level number, adding more gaps and spikes as the level increases.

### 5. Collision Detection
We implemented Axis-Aligned Bounding Box (AABB) collision detection. The player checks for overlaps with platforms (to stand on), items (to collect), and obstacles (to die).

### 6. Level Progression
Upon reaching the "Exit" flag, the game increments the level counter and regenerates a new, slightly harder level using the `LevelGenerator`.

## Controls
- **Space**: Jump / Start Game / Next Level
- **Arrow Left/Right**: Move
