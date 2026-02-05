class Game {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;

        this.level = 1;
        this.score = 0;
        this.balls = [];
        this.bricks = [];
        this.items = [];

        // Game State
        this.state = 'AIMING'; // AIMING, SHOOTING, MOVING, END_TURN
        this.ballsToShoot = 0;
        this.shootTimer = 0;

        // Paddle/Launcher pos
        this.launcherX = this.width / 2;
        this.launcherY = this.height - 30;

        this.levelGenerator = new LevelGenerator(7); // 7 Columns
        this.colWidth = this.width / 7;
        this.rowHeight = this.colWidth * 0.6;

        this.input = { x: 0, y: 0, isDown: false, aimAngle: -Math.PI / 2 };

        this.ballCount = 1; // Starting balls
        this.ballsReturned = 0;
        this.nextLauncherX = null;

        // Bind events
        this.bindEvents();

        // Load first level
        this.loadLevel(this.level);
    }

    bindEvents() {
        const start = (e) => {
            if (this.state !== 'AIMING') return;
            const pos = this.getPos(e);
            this.input.isDown = true;
            this.input.x = pos.x;
            this.input.y = pos.y;
        };

        const move = (e) => {
            if (!this.input.isDown || this.state !== 'AIMING') return;
            const pos = this.getPos(e);
            const dx = pos.x - this.launcherX;
            const dy = pos.y - this.launcherY;
            // Angle should be upwards
            if (dy < 0) {
                this.input.aimAngle = Math.atan2(dy, dx);
            }
        };

        const end = (e) => {
            if (this.input.isDown && this.state === 'AIMING') {
                this.shoot();
            }
            this.input.isDown = false;
        };

        this.canvas.addEventListener('mousedown', start);
        this.canvas.addEventListener('mousemove', move);
        this.canvas.addEventListener('mouseup', end);

        this.canvas.addEventListener('touchstart', (e) => { e.preventDefault(); start(e.touches[0]); }, {passive: false});
        this.canvas.addEventListener('touchmove', (e) => { e.preventDefault(); move(e.touches[0]); }, {passive: false});
        this.canvas.addEventListener('touchend', (e) => { e.preventDefault(); end(e.changedTouches[0]); }, {passive: false});
    }

    getPos(e) {
        const rect = this.canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }

    loadLevel(n) {
        this.level = n;
        const data = this.levelGenerator.generateLevel(n);

        this.bricks = [];
        this.items = [];

        data.bricks.forEach(b => {
            this.bricks.push(new Brick(
                b.c * this.colWidth,
                b.r * this.rowHeight + 50, // Top margin
                this.colWidth - 2,
                this.rowHeight - 2,
                b.hp,
                b.type
            ));
        });

        data.items.forEach(i => {
            this.items.push(new Item(
                i.c * this.colWidth + this.colWidth/2,
                i.r * this.rowHeight + 50 + this.rowHeight/2,
                10,
                i.type
            ));
        });

        // Reset launcher
        this.launcherX = this.width / 2;
        this.state = 'AIMING';
        this.balls = [];
    }

    shoot() {
        this.state = 'SHOOTING';
        this.ballsToShoot = this.ballCount;
        this.shootTimer = 0;
        this.ballsReturned = 0;
        this.nextLauncherX = null;
    }

    update(dt) {
        if (this.state === 'SHOOTING') {
            this.shootTimer += dt;
            if (this.shootTimer > 0.1) { // Fire every 100ms
                this.shootTimer = 0;

                // 20% chance for a heavy ball
                const type = (Math.random() < 0.2) ? 'HEAVY' : 'NORMAL';

                const ball = new Ball(this.launcherX, this.launcherY, 8, type);
                ball.vx = Math.cos(this.input.aimAngle) * 500; // Speed
                ball.vy = Math.sin(this.input.aimAngle) * 500;
                ball.active = true;
                this.balls.push(ball);
                this.ballsToShoot--;
                if (this.ballsToShoot <= 0) {
                    this.state = 'MOVING';
                }
            }
        }

        if (this.state === 'MOVING' || this.state === 'SHOOTING') {
            let allStopped = (this.state === 'MOVING');

            this.balls.forEach(ball => {
                if (ball.active) {
                    allStopped = false;
                    // Move
                    // Sub-stepping for collision precision
                    const steps = 5;
                    const stepDt = dt / steps;
                    for (let s = 0; s < steps; s++) {
                        ball.update(stepDt);
                        this.checkCollisions(ball);
                        if (!ball.active) break;
                    }
                }
            });

            if (allStopped && this.balls.length === this.ballCount) {
                 this.endTurn();
            }
        }
    }

    checkCollisions(ball) {
        // Walls
        if (ball.x - ball.radius < 0) {
            ball.x = ball.radius;
            ball.vx *= -1;
        }
        if (ball.x + ball.radius > this.width) {
            ball.x = this.width - ball.radius;
            ball.vx *= -1;
        }
        if (ball.y - ball.radius < 0) {
            ball.y = ball.radius;
            ball.vy *= -1;
        }
        // Floor
        if (ball.y + ball.radius > this.height) {
            ball.active = false;
            ball.y = this.height - ball.radius;
            this.ballsReturned++;
            if (this.nextLauncherX === null) {
                this.nextLauncherX = ball.x;
            }
        }

        // Bricks
        for (let i = 0; i < this.bricks.length; i++) {
            const brick = this.bricks[i];
            if (brick.markedForDeletion) continue;

            // Simple AABB vs Circle
            // Find closest point on rect to circle center
            const closestX = Math.max(brick.x, Math.min(ball.x, brick.x + brick.width));
            const closestY = Math.max(brick.y, Math.min(ball.y, brick.y + brick.height));

            const dx = ball.x - closestX;
            const dy = ball.y - closestY;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < ball.radius) {
                // Collision
                // Determine normal
                // (Very simplified reflection)
                if (Math.abs(dx) > Math.abs(dy)) {
                    ball.vx *= -1;
                } else {
                    ball.vy *= -1;
                }

                // Damage Brick
                if (brick.hit(ball.damage)) {
                   this.score += 10;
                   if (brick.type === 'EXPLOSIVE') {
                       this.explode(brick);
                   } else if (brick.type === 'HEALER') {
                       this.healNeighbors(brick);
                   }
                }

                return; // Only one collision per step
            }
        }

        // Items
        for (let i = 0; i < this.items.length; i++) {
            const item = this.items[i];
            if (item.markedForDeletion) continue;

            const dx = ball.x - item.x;
            const dy = ball.y - item.y;
            const dist = Math.sqrt(dx*dx + dy*dy);

            if (dist < ball.radius + item.radius) {
                item.markedForDeletion = true;
                if (item.type === 'ADD_BALL') {
                    this.ballCount++;
                }
            }
        }
    }

    getNeighbors(brick) {
        // Find bricks adjacent to this one (ignoring itself)
        const neighbors = [];
        const cx = brick.x + brick.width/2;
        const cy = brick.y + brick.height/2;

        this.bricks.forEach(b => {
            if (b === brick || b.markedForDeletion) return;
            const bcx = b.x + b.width/2;
            const bcy = b.y + b.height/2;

            // Check distance (approx grid size * 1.5)
            const dist = Math.sqrt((cx-bcx)**2 + (cy-bcy)**2);
            if (dist < this.colWidth * 1.5) {
                neighbors.push(b);
            }
        });
        return neighbors;
    }

    explode(brick) {
        // Deal massive damage to neighbors
        const neighbors = this.getNeighbors(brick);
        neighbors.forEach(n => {
            n.hit(5); // 5 Damage
        });
    }

    healNeighbors(brick) {
        const neighbors = this.getNeighbors(brick);
        neighbors.forEach(n => {
            n.hp += 5;
            if (n.hp > n.maxHp * 2) n.hp = n.maxHp * 2; // Cap over-heal
        });
    }

    endTurn() {
        // Cleanup
        this.bricks = this.bricks.filter(b => !b.markedForDeletion);
        this.items = this.items.filter(i => !i.markedForDeletion);
        this.balls = [];

        // Check Win
        if (this.bricks.length === 0) {
            alert('Level Complete!');
            this.loadLevel(this.level + 1);
            return;
        }

        // Move Bricks Down
        this.bricks.forEach(b => b.y += this.rowHeight);
        this.items.forEach(i => i.y += this.rowHeight);

        // Check Loss
        let gameOver = false;
        this.bricks.forEach(b => {
            if (b.y + b.height > this.launcherY) gameOver = true;
        });

        if (gameOver) {
            alert('Game Over! Restarting Level.');
            this.ballCount = 1;
            this.score = 0;
            this.loadLevel(this.level);
        } else {
            this.state = 'AIMING';
            if (this.nextLauncherX !== null) {
                this.launcherX = this.nextLauncherX;
            }
        }
    }

    draw() {
        // Clear
        this.ctx.fillStyle = '#111';
        this.ctx.fillRect(0, 0, this.width, this.height);

        // Draw Bricks
        this.bricks.forEach(b => b.draw(this.ctx));

        // Draw Items
        this.items.forEach(i => i.draw(this.ctx));

        // Draw Balls
        this.balls.forEach(b => {
            if (b.active) {
                this.ctx.beginPath();
                this.ctx.arc(b.x, b.y, b.radius, 0, Math.PI*2);
                this.ctx.fillStyle = '#fff';
                this.ctx.fill();
            }
        });

        // Draw Launcher/Aim
        if (this.state === 'AIMING') {
            this.ctx.beginPath();
            this.ctx.arc(this.launcherX, this.launcherY, 10, 0, Math.PI*2);
            this.ctx.fillStyle = '#0ff';
            this.ctx.fill();

            if (this.input.isDown) {
                this.ctx.beginPath();
                this.ctx.moveTo(this.launcherX, this.launcherY);
                this.ctx.lineTo(
                    this.launcherX + Math.cos(this.input.aimAngle) * 100,
                    this.launcherY + Math.sin(this.input.aimAngle) * 100
                );
                this.ctx.strokeStyle = '#fff';
                this.ctx.setLineDash([5, 5]);
                this.ctx.stroke();
                this.ctx.setLineDash([]);
            }
        }

        // Draw UI
        this.ctx.fillStyle = 'white';
        this.ctx.font = '20px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(`Level: ${this.level}`, 10, 30);
        this.ctx.textAlign = 'right';
        this.ctx.fillText(`Balls: ${this.ballCount}`, this.width - 10, 30);
    }
}
