class LevelGenerator {
    constructor(cols) {
        this.cols = cols;
    }

    generateLevel(levelNumber) {
        const bricks = [];
        const items = [];
        const rows = 5 + Math.floor(levelNumber / 10); // Increase rows slightly every 10 levels
        const maxHp = levelNumber; // Base HP scales with level

        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                // Random chance to place a brick
                if (Math.random() > 0.3) { // 70% fill rate
                    const hp = Math.max(1, Math.floor(Math.random() * maxHp) + 1);

                    // Special types
                    let type = 'NORMAL';
                    const rand = Math.random();
                    if (rand < 0.05) type = 'EXPLOSIVE';
                    else if (rand < 0.1) type = 'HEALER';

                    // Calculate position based on grid (will be scaled in Game class)
                    // We store grid coordinates here, Game class will map to pixels
                    bricks.push({
                        c: c,
                        r: r,
                        hp: hp,
                        type: type
                    });
                } else if (Math.random() < 0.1) {
                    // Chance for item
                    items.push({
                        c: c,
                        r: r,
                        type: 'ADD_BALL'
                    });
                }
            }
        }
        return { bricks, items };
    }
}
