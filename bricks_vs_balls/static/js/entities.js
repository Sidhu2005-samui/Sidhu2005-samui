class Ball {
    constructor(x, y, radius, type = 'NORMAL') {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.vx = 0;
        this.vy = 0;
        this.active = false; // Balls start inactive until shot
        this.type = type;
        this.damage = 1;

        if (this.type === 'HEAVY') {
            this.damage = 2;
            this.radius *= 1.2;
        }
    }

    update(dt) {
        if (!this.active) return;
        this.x += this.vx * dt;
        this.y += this.vy * dt;
    }

    reset(x, y) {
        this.x = x;
        this.y = y;
        this.vx = 0;
        this.vy = 0;
        this.active = false;
    }
}

class Brick {
    constructor(x, y, width, height, hp, type = 'NORMAL') {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.hp = hp;
        this.maxHp = hp;
        this.type = type;
        this.markedForDeletion = false;
    }

    draw(ctx) {
        if (this.markedForDeletion) return;

        ctx.fillStyle = this.getColor();
        ctx.fillRect(this.x, this.y, this.width, this.height);

        // Draw HP
        ctx.fillStyle = 'white';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.hp, this.x + this.width / 2, this.y + this.height / 2);

        // Draw Border
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        ctx.strokeRect(this.x, this.y, this.width, this.height);
    }

    getColor() {
        if (this.type === 'EXPLOSIVE') return '#ff4444';
        if (this.type === 'HEALER') return '#44ff44';

        // Gradient color based on HP relative to maxHP?
        // Or just fixed colors for readability. Let's do heat map style.
        const ratio = Math.min(this.hp / 50, 1); // Cap at 50 for color scaling
        // Simple interpolation: Green to Red
        const r = Math.floor(255 * ratio);
        const g = Math.floor(255 * (1 - ratio));
        return `rgb(${r}, ${g}, 100)`;
    }

    hit(damage) {
        this.hp -= damage;
        if (this.hp <= 0) {
            this.hp = 0;
            this.markedForDeletion = true;
            return true; // Destroyed
        }
        return false;
    }
}

class Item {
    constructor(x, y, radius, type) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.type = type; // 'ADD_BALL', 'POWER_UP'
        this.markedForDeletion = false;
    }

    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'white';
        ctx.fill();
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Inner circle
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius * 0.5, 0, Math.PI * 2);
        ctx.fillStyle = '#00ff00';
        ctx.fill();
    }
}
