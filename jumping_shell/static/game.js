
class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;

        this.score = 0;
        this.lives = 3;
        this.currentLevel = 1;
        this.maxLevels = 100;

        this.player = null;
        this.platforms = [];
        this.items = [];
        this.obstacles = [];
        this.exit = null;

        this.keys = {};
        this.state = 'start'; // start, playing, level_complete, game_over, victory

        this.cameraX = 0;

        this.setupInput();
        this.startLevel(this.currentLevel);

        this.lastTime = 0;
        requestAnimationFrame(this.loop.bind(this));
    }

    setupInput() {
        window.addEventListener('keydown', (e) => {
            this.keys[e.code] = true;
            if (this.state === 'start' || this.state === 'level_complete' || this.state === 'game_over' || this.state === 'victory') {
                if (e.code === 'Space') {
                    this.handleStateTransition();
                }
            }
        });
        window.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
    }

    handleStateTransition() {
        if (this.state === 'start') {
            this.state = 'playing';
            this.hideMessage();
        } else if (this.state === 'level_complete') {
            this.currentLevel++;
            if (this.currentLevel > this.maxLevels) {
                this.state = 'victory';
                this.showMessage("Victory!", "You completed all levels! Press Space to restart.");
            } else {
                this.startLevel(this.currentLevel);
                this.state = 'playing';
                this.hideMessage();
            }
        } else if (this.state === 'game_over' || this.state === 'victory') {
            this.resetGame();
        }
    }

    resetGame() {
        this.score = 0;
        this.lives = 3;
        this.currentLevel = 1;
        this.startLevel(1);
        this.state = 'playing';
        this.hideMessage();
        this.updateUI();
    }

    startLevel(levelNum) {
        // Reset entities
        this.platforms = [];
        this.items = [];
        this.obstacles = [];
        this.exit = null;
        this.cameraX = 0;

        // Generate Level
        const levelData = LevelGenerator.generate(levelNum);
        this.parseLevel(levelData);

        // Update UI
        document.getElementById('level').innerText = `Level: ${levelNum}`;
        this.updateUI();
    }

    parseLevel(data) {
        const tileSize = 40;
        for (let r = 0; r < data.length; r++) {
            for (let c = 0; c < data[r].length; c++) {
                const char = data[r][c];
                const x = c * tileSize;
                const y = r * tileSize;

                if (char === '#') {
                    this.platforms.push(new Platform(x, y, tileSize, tileSize));
                } else if (char === '@') {
                    this.player = new Player(x, y);
                } else if (char === 'o') {
                    this.items.push(new Item(x + 10, y + 10, 20, 'coin'));
                } else if (char === '*') {
                    this.obstacles.push(new Obstacle(x, y + 20, tileSize, 20, 'spike'));
                } else if (char === '!') {
                    this.exit = new Exit(x, y, tileSize, tileSize);
                }
            }
        }
    }

    update(dt) {
        if (this.state !== 'playing') return;

        this.player.update(dt, this.keys, this.platforms);

        // Camera follow
        this.cameraX = this.player.x - this.width / 3;
        if (this.cameraX < 0) this.cameraX = 0;

        // Check Collisions with Items
        for (let i = this.items.length - 1; i >= 0; i--) {
            if (this.checkCollision(this.player, this.items[i])) {
                this.score += 10;
                this.items.splice(i, 1);
                this.updateUI();
            }
        }

        // Check Collisions with Obstacles
        for (const obs of this.obstacles) {
            if (this.checkCollision(this.player, obs)) {
                this.handleDeath();
                return;
            }
        }

        // Check Fall off world
        if (this.player.y > this.height) {
            this.handleDeath();
            return;
        }

        // Check Exit
        if (this.exit && this.checkCollision(this.player, this.exit)) {
            this.state = 'level_complete';
            this.showMessage("Level Complete!", "Press Space to continue");
        }
    }

    handleDeath() {
        this.lives--;
        this.updateUI();
        if (this.lives <= 0) {
            this.state = 'game_over';
            this.showMessage("Game Over", `Final Score: ${this.score}. Press Space to restart.`);
        } else {
            // Respawn at start of level (simplified: reload level)
            this.startLevel(this.currentLevel);
        }
    }

    checkCollision(rect1, rect2) {
        return (rect1.x < rect2.x + rect2.width &&
                rect1.x + rect1.width > rect2.x &&
                rect1.y < rect2.y + rect2.height &&
                rect1.y + rect1.height > rect2.y);
    }

    draw() {
        // Clear background
        this.ctx.fillStyle = '#87CEEB';
        this.ctx.fillRect(0, 0, this.width, this.height);

        this.ctx.save();
        this.ctx.translate(-this.cameraX, 0);

        // Draw entities
        this.platforms.forEach(p => p.draw(this.ctx));
        this.items.forEach(i => i.draw(this.ctx));
        this.obstacles.forEach(o => o.draw(this.ctx));
        if (this.exit) this.exit.draw(this.ctx);
        if (this.player) this.player.draw(this.ctx);

        this.ctx.restore();
    }

    loop(timestamp) {
        const dt = (timestamp - this.lastTime) / 1000;
        this.lastTime = timestamp;

        this.update(dt);
        this.draw();

        requestAnimationFrame(this.loop.bind(this));
    }

    showMessage(title, text) {
        const overlay = document.getElementById('message-overlay');
        document.getElementById('message-title').innerText = title;
        document.getElementById('message-text').innerText = text;
        overlay.classList.remove('hidden');
    }

    hideMessage() {
        document.getElementById('message-overlay').classList.add('hidden');
    }

    updateUI() {
        document.getElementById('score').innerText = `Score: ${this.score}`;
        document.getElementById('lives').innerText = `Lives: ${this.lives}`;
    }
}

class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 30;
        this.height = 30;
        this.vx = 0;
        this.vy = 0;
        this.speed = 300;
        this.jumpForce = -600; // Increased jump force to clear 2 block high
        this.gravity = 1500;
        this.grounded = false;
        this.color = '#FF6347'; // Tomato
    }

    update(dt, keys, platforms) {
        // Horizontal Movement
        if (keys['ArrowRight']) this.vx = this.speed;
        else if (keys['ArrowLeft']) this.vx = -this.speed;
        else this.vx = 0;

        this.x += this.vx * dt;

        // Horizontal Collision
        this.handleCollision(platforms, true);

        // Jumping
        if (keys['Space'] && this.grounded) {
            this.vy = this.jumpForce;
            this.grounded = false;
        }

        // Gravity
        this.vy += this.gravity * dt;
        this.y += this.vy * dt;

        // Vertical Collision
        this.grounded = false;
        this.handleCollision(platforms, false);
    }

    handleCollision(platforms, horizontal) {
        for (const p of platforms) {
            if (this.checkCollision(p)) {
                if (horizontal) {
                    if (this.vx > 0) this.x = p.x - this.width;
                    else if (this.vx < 0) this.x = p.x + p.width;
                    this.vx = 0;
                } else {
                    if (this.vy > 0) {
                        this.y = p.y - this.height;
                        this.grounded = true;
                        this.vy = 0;
                    } else if (this.vy < 0) {
                        this.y = p.y + p.height;
                        this.vy = 0;
                    }
                }
            }
        }
    }

    checkCollision(rect2) {
        return (this.x < rect2.x + rect2.width &&
                this.x + this.width > rect2.x &&
                this.y < rect2.y + rect2.height &&
                this.y + this.height > rect2.y);
    }

    draw(ctx) {
        ctx.fillStyle = this.color;
        // Draw a shell shape (semi-circle on top of rectangle)
        ctx.beginPath();
        ctx.arc(this.x + this.width/2, this.y + this.height/2, this.width/2, Math.PI, 0);
        ctx.rect(this.x, this.y + this.height/2, this.width, this.height/2);
        ctx.fill();
        ctx.closePath();
    }
}

class Platform {
    constructor(x, y, w, h) {
        this.x = x;
        this.y = y;
        this.width = w;
        this.height = h;
    }

    draw(ctx) {
        ctx.fillStyle = '#654321'; // Brown
        ctx.fillRect(this.x, this.y, this.width, this.height);
        // Grass top
        ctx.fillStyle = '#228B22'; // Forest Green
        ctx.fillRect(this.x, this.y, this.width, 10);
    }
}

class Item {
    constructor(x, y, size, type) {
        this.x = x;
        this.y = y;
        this.width = size;
        this.height = size;
        this.type = type;
        this.wobble = 0;
    }

    draw(ctx) {
        ctx.fillStyle = '#FFD700'; // Gold
        ctx.beginPath();
        ctx.arc(this.x + this.width/2, this.y + this.height/2, this.width/2, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#DAA520';
        ctx.lineWidth = 2;
        ctx.stroke();
    }
}

class Obstacle {
    constructor(x, y, w, h, type) {
        this.x = x;
        this.y = y;
        this.width = w;
        this.height = h;
        this.type = type;
    }

    draw(ctx) {
        ctx.fillStyle = '#808080';
        if (this.type === 'spike') {
            // Draw triangles
            const numSpikes = Math.floor(this.width / 10);
            ctx.beginPath();
            for (let i = 0; i < numSpikes; i++) {
                ctx.moveTo(this.x + i*10, this.y + this.height);
                ctx.lineTo(this.x + i*10 + 5, this.y);
                ctx.lineTo(this.x + i*10 + 10, this.y + this.height);
            }
            ctx.fill();
        } else {
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }
}

class Exit {
    constructor(x, y, w, h) {
        this.x = x;
        this.y = y;
        this.width = w;
        this.height = h;
    }

    draw(ctx) {
        ctx.fillStyle = '#000000';
        ctx.fillRect(this.x + this.width/4, this.y, this.width/2, this.height);
        ctx.fillStyle = '#FF0000'; // Flag
        ctx.beginPath();
        ctx.moveTo(this.x + this.width/4, this.y);
        ctx.lineTo(this.x + this.width, this.y + 10);
        ctx.lineTo(this.x + this.width/4, this.y + 20);
        ctx.fill();
    }
}

class LevelGenerator {
    static generate(levelNum) {
        const rows = 15; // 600px height / 40
        const minCols = 20; // 800px width / 40
        const cols = minCols + levelNum * 2; // Level gets longer

        let map = [];
        for (let r = 0; r < rows; r++) {
            let row = "";
            for (let c = 0; c < cols; c++) {
                row += ".";
            }
            map.push(row.split(''));
        }

        // Floor
        for (let c = 0; c < cols; c++) {
            map[rows-1][c] = '#';
        }

        // Start
        map[rows-2][2] = '@';

        // Generate Terrain
        let currentHeight = rows - 1;
        let lastGap = -10;

        for (let c = 5; c < cols - 2; c++) {
            // Chance to create a gap
            // Difficulty increases gap frequency
            const gapChance = 0.05 + (levelNum * 0.002);
            if (Math.random() < gapChance && c - lastGap > 3) {
                map[rows-1][c] = '.';
                // Maybe double gap for higher levels
                if (levelNum > 10 && Math.random() < 0.5) {
                   map[rows-1][c+1] = '.';
                   c++;
                }
                lastGap = c;
            } else {
                // Platform height change
                // (Simplified: mostly flat or simple steps)
                if (Math.random() < 0.1) {
                     // Create a raised platform
                     const h = Math.floor(Math.random() * 3) + 2; // Height from bottom
                     const w = Math.floor(Math.random() * 3) + 2;
                     const py = rows - 1 - h;

                     // Ensure jumpable
                     for(let i=0; i<w; i++) {
                         if (c+i < cols-2) {
                             map[py][c+i] = '#';

                             // Add coin on top?
                             if (Math.random() < 0.5) map[py-1][c+i] = 'o';
                         }
                     }
                }
            }

            // Spikes
            if (levelNum > 5 && Math.random() < (0.05 + levelNum * 0.005)) {
                if (map[rows-1][c] === '#') { // If ground exists
                    map[rows-2][c] = '*';
                }
            }
        }

        // Exit
        map[rows-2][cols-2] = '!';

        return map;
    }
}

window.onload = () => {
    new Game();
};
