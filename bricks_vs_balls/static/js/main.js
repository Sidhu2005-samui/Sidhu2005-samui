window.onload = function() {
    const canvas = document.getElementById('gameCanvas');

    function resize() {
        // Full screen, but maybe cap width for gameplay balance if on desktop
        // For mobile APK, we usually want full width.
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    // Initial resize
    resize();

    // Start Game
    const game = new Game(canvas);

    // Handle resize events (optional: might need to reset game or scale entities)
    window.addEventListener('resize', () => {
        resize();
        game.width = canvas.width;
        game.height = canvas.height;
        game.colWidth = game.width / 7; // Re-calc grid
        game.rowHeight = game.colWidth * 0.6;
        // Re-positioning existing entities is hard, usually easier to just let it be or restart
    });

    let lastTime = 0;
    function loop(timestamp) {
        const dt = (timestamp - lastTime) / 1000;
        lastTime = timestamp;

        // Cap dt to prevent huge jumps if tab is inactive
        const safeDt = Math.min(dt, 0.1);

        game.update(safeDt);
        game.draw();

        requestAnimationFrame(loop);
    }

    requestAnimationFrame(loop);
};
