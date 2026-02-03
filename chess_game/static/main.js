// Global Variables
let scene, camera, renderer, raycaster, mouse;
let boardGroup, piecesGroup;
let socket;
let gameMode = 'single';
let roomCode = 'default';
let playerColor = 'white'; // Default
let chessGame = new Chess();
let selectedPiece = null;
let possibleMoves = [];
let highlightedSquares = [];

// Configuration
let config = {
    squareSize: 10,
    colors: {
        board1: 0xffffff,
        board2: 0x444444,
        white: 0xeeeeee,
        black: 0x111111,
        highlight: 0xffff00,
        selected: 0x00ff00
    }
};

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x333333);

    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(0, 120, 100);
    camera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(50, 100, 50);
    dirLight.castShadow = true;
    scene.add(dirLight);

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();
    window.addEventListener('resize', onWindowResize, false);
    window.addEventListener('click', onMouseClick, false);

    socket = io();
    setupSocketListeners();

    boardGroup = new THREE.Group();
    piecesGroup = new THREE.Group();
    scene.add(boardGroup);
    scene.add(piecesGroup);

    createBoard();
    drawPieces(chessGame.fen());

    animate();
}

function createBoard() {
    while(boardGroup.children.length > 0){
        boardGroup.remove(boardGroup.children[0]);
    }

    const geometry = new THREE.BoxGeometry(config.squareSize, 2, config.squareSize);
    const offset = (config.squareSize * 3.5);

    for (let x = 0; x < 8; x++) {
        for (let z = 0; z < 8; z++) {
            let isWhite = (x + z) % 2 === 0;
            let color = isWhite ? config.colors.board1 : config.colors.board2;

            const material = new THREE.MeshPhongMaterial({ color: color });
            const cube = new THREE.Mesh(geometry, material);

            cube.position.x = (x * config.squareSize) - offset;
            cube.position.z = (z * config.squareSize) - offset;
            cube.position.y = -1;

            cube.receiveShadow = true;

            const file = String.fromCharCode(97 + x);
            const rank = 8 - z;
            cube.userData = { square: file + rank, isSquare: true, originalColor: color };

            boardGroup.add(cube);
        }
    }

    const borderGeom = new THREE.BoxGeometry(config.squareSize * 8 + 4, 1, config.squareSize * 8 + 4);
    const borderMat = new THREE.MeshPhongMaterial({ color: 0x664422 });
    const border = new THREE.Mesh(borderGeom, borderMat);
    border.position.y = -2;
    boardGroup.add(border);
}

function createPieceMesh(type, color) {
    const material = new THREE.MeshPhongMaterial({ color: color });
    let mesh = new THREE.Group();

    const baseGeom = new THREE.CylinderGeometry(3.5, 3.5, 1, 32);
    const base = new THREE.Mesh(baseGeom, material);
    base.position.y = 0.5;
    base.castShadow = true;
    mesh.add(base);

    if (type === 'p') {
        const bodyGeom = new THREE.ConeGeometry(2.5, 6, 16);
        const body = new THREE.Mesh(bodyGeom, material);
        body.position.y = 4;
        body.castShadow = true;
        mesh.add(body);
        const headGeom = new THREE.SphereGeometry(1.5, 16, 16);
        const head = new THREE.Mesh(headGeom, material);
        head.position.y = 7;
        head.castShadow = true;
        mesh.add(head);
    }
    else if (type === 'r') {
        const bodyGeom = new THREE.CylinderGeometry(2.5, 2.5, 6, 16);
        const body = new THREE.Mesh(bodyGeom, material);
        body.position.y = 4;
        body.castShadow = true;
        mesh.add(body);
        const headGeom = new THREE.CylinderGeometry(3, 3, 2, 8);
        const head = new THREE.Mesh(headGeom, material);
        head.position.y = 7.5;
        head.castShadow = true;
        mesh.add(head);
    }
    else if (type === 'n') {
        const bodyGeom = new THREE.BoxGeometry(3, 7, 3);
        const body = new THREE.Mesh(bodyGeom, material);
        body.position.y = 4.5;
        body.castShadow = true;
        mesh.add(body);
        const headGeom = new THREE.BoxGeometry(3, 2, 5);
        const head = new THREE.Mesh(headGeom, material);
        head.position.y = 8;
        head.position.z = -1;
        head.castShadow = true;
        mesh.add(head);
    }
    else if (type === 'b') {
        const bodyGeom = new THREE.CylinderGeometry(1.5, 2.5, 7, 16);
        const body = new THREE.Mesh(bodyGeom, material);
        body.position.y = 4.5;
        body.castShadow = true;
        mesh.add(body);
        const headGeom = new THREE.SphereGeometry(1, 16, 16);
        const head = new THREE.Mesh(headGeom, material);
        head.position.y = 8.5;
        head.castShadow = true;
        mesh.add(head);
        const hatGeom = new THREE.ConeGeometry(2, 3, 16);
        const hat = new THREE.Mesh(hatGeom, material);
        hat.position.y = 7;
        hat.castShadow = true;
        mesh.add(hat);
    }
    else if (type === 'q') {
        const bodyGeom = new THREE.CylinderGeometry(2, 3, 9, 16);
        const body = new THREE.Mesh(bodyGeom, material);
        body.position.y = 5.5;
        body.castShadow = true;
        mesh.add(body);
        const headGeom = new THREE.SphereGeometry(2, 16, 16);
        const head = new THREE.Mesh(headGeom, material);
        head.position.y = 10.5;
        head.castShadow = true;
        mesh.add(head);
        const crownGeom = new THREE.CylinderGeometry(3.5, 1.5, 1, 8, 1, true);
        const crown = new THREE.Mesh(crownGeom, material);
        crown.position.y = 10;
        crown.castShadow = true;
        mesh.add(crown);
    }
    else if (type === 'k') {
        const bodyGeom = new THREE.CylinderGeometry(2.5, 3, 10, 16);
        const body = new THREE.Mesh(bodyGeom, material);
        body.position.y = 6;
        body.castShadow = true;
        mesh.add(body);
        const vBarGeom = new THREE.BoxGeometry(1, 3, 1);
        const vBar = new THREE.Mesh(vBarGeom, material);
        vBar.position.y = 12;
        vBar.castShadow = true;
        mesh.add(vBar);
        const hBarGeom = new THREE.BoxGeometry(2.5, 1, 1);
        const hBar = new THREE.Mesh(hBarGeom, material);
        hBar.position.y = 12;
        hBar.castShadow = true;
        mesh.add(hBar);
    }

    return mesh;
}

function drawPieces(fen) {
    while(piecesGroup.children.length > 0){
        piecesGroup.remove(piecesGroup.children[0]);
    }

    chessGame.load(fen);
    const board = chessGame.board();

    for(let r=0; r<8; r++) {
        for(let c=0; c<8; c++) {
            const piece = board[r][c];
            if(piece) {
                const type = piece.type;
                const colorCode = piece.color;
                const color = colorCode === 'w' ? config.colors.white : config.colors.black;

                const mesh = createPieceMesh(type, color);

                const offset = (config.squareSize * 3.5);
                const x = (c * config.squareSize) - offset;
                const z = (r * config.squareSize) - offset;

                mesh.position.set(x, 0, z);

                const square = String.fromCharCode(97+c) + (8-r);
                mesh.userData = { piece: piece, square: square, isPiece: true };

                piecesGroup.add(mesh);
            }
        }
    }
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

// ---------------------- Interaction & Logic ----------------------

function startGame(mode) {
    gameMode = mode;
    roomCode = document.getElementById('room-code').value;
    const difficulty = document.getElementById('ai-difficulty').value;

    socket.emit('join_game', { room: roomCode, mode: mode });

    document.getElementById('main-menu').style.display = 'none';
    document.getElementById('game-hud').style.display = 'block';

    if (mode === 'single') {
        // Store difficulty for AI request
        window.aiDifficulty = difficulty;
    }
}

function showMenu() {
    document.getElementById('main-menu').style.display = 'block';
    document.getElementById('game-hud').style.display = 'none';
}

function resetGame() {
    socket.emit('reset_game', { room: roomCode });
}

function requestAnalysis() {
    socket.emit('get_analysis', { room: roomCode });
}

function requestHint() {
    socket.emit('get_hint', { room: roomCode });
}

function updateColors() {
    config.colors.board1 = new THREE.Color(document.getElementById('color-board-1').value).getHex();
    config.colors.board2 = new THREE.Color(document.getElementById('color-board-2').value).getHex();
    config.colors.white = new THREE.Color(document.getElementById('color-white').value).getHex();
    config.colors.black = new THREE.Color(document.getElementById('color-black').value).getHex();

    createBoard();
    drawPieces(chessGame.fen());
}

function onMouseClick(event) {
    event.preventDefault();

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);

    // Intersect pieces and board
    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
        // Find the first object that is a square or a piece
        let target = null;
        for (let i = 0; i < intersects.length; i++) {
            let obj = intersects[i].object;
            // Traverse up to find the group with userData
            while(obj.parent && obj.parent.type !== 'Scene' && !obj.userData.isSquare && !obj.userData.isPiece) {
                obj = obj.parent;
            }
            if (obj.userData.isSquare || obj.userData.isPiece) {
                target = obj;
                break;
            }
        }

        if (target) {
            handleSquareClick(target.userData.square);
        }
    }
}

function handleSquareClick(square) {
    // If it's not my turn and online, ignore (basic check)
    // Note: Local mode allows moving both.

    // Check if we selected a piece
    const piece = chessGame.get(square);

    if (selectedPiece) {
        // Try to move
        const move = {
            from: selectedPiece,
            to: square,
            promotion: 'q' // Always promote to queen for simplicity
        };

        const legalMove = chessGame.move(move); // Returns move object if legal, null otherwise

        if (legalMove) {
            // Valid move on client side
            chessGame.undo(); // Undo to wait for server confirmation or just send it
            // Actually, we should send move to server.
            socket.emit('make_move', { room: roomCode, move: legalMove.from + legalMove.to + (legalMove.promotion || '') });

            clearHighlights();
            selectedPiece = null;
            return;
        } else {
            // Invalid move. If clicked on another own piece, select it.
            if (piece && (isMyPiece(piece))) {
                selectPiece(square);
            } else {
                clearHighlights();
                selectedPiece = null;
            }
        }
    } else {
        if (piece && isMyPiece(piece)) {
            selectPiece(square);
        }
    }
}

function isMyPiece(piece) {
    if (gameMode === 'local') return true;
    if (gameMode === 'single') return piece.color === 'w'; // User is always white in Single for now
    if (gameMode === 'multi') return (piece.color === 'w' && playerColor === 'white') || (piece.color === 'b' && playerColor === 'black');
    return false;
}

function selectPiece(square) {
    selectedPiece = square;
    possibleMoves = chessGame.moves({ square: square, verbose: true });
    highlightSquares(possibleMoves.map(m => m.to).concat([square]));
}

function highlightSquares(squares) {
    clearHighlights();

    boardGroup.children.forEach(mesh => {
        if (squares.includes(mesh.userData.square)) {
            mesh.material.color.setHex(config.colors.highlight);
            highlightedSquares.push(mesh);
        }
    });
}

function clearHighlights() {
    boardGroup.children.forEach(mesh => {
        if (mesh.userData.isSquare) {
            mesh.material.color.setHex(mesh.userData.originalColor);
        }
    });
    highlightedSquares = [];
}

function setupSocketListeners() {
    socket.on('color_assignment', (data) => {
        playerColor = data.color;
        console.log("Assigned color: " + playerColor);
        // Rotate board if black?
        if (playerColor === 'black') {
            camera.position.set(0, 120, -100);
            camera.lookAt(0, 0, 0);
            // Flip board logic?
            // My board generation maps z=0 to rank 8.
            // White view: rank 1 (z=7) is close.
            // Black view: rank 8 (z=0) should be close.
            // Camera at z=-100 looks at 0. It sees rank 8 close. Correct.
        } else {
            camera.position.set(0, 120, 100);
            camera.lookAt(0, 0, 0);
        }
    });

    socket.on('board_state', (data) => {
        chessGame.load(data.fen);
        drawPieces(data.fen);

        let status = "";
        if (data.game_over) {
            status = "Game Over! " + data.result;
        } else {
            status = (chessGame.turn() === 'w' ? "White" : "Black") + "'s Turn";
            if (chessGame.in_check()) status += " (Check)";
        }
        document.getElementById('status-text').innerText = status;

        // Trigger AI if needed
        if (gameMode === 'single' && chessGame.turn() === 'b' && !data.game_over) {
             setTimeout(() => {
                 socket.emit('request_ai_move', { room: roomCode, difficulty: window.aiDifficulty });
             }, 500);
        }
    });

    socket.on('invalid_move', (data) => {
        alert("Invalid Move: " + data.move);
        // Sync board just in case
        socket.emit('join_game', { room: roomCode, mode: gameMode }); // Re-join to get state? Or separate get_state
    });

    socket.on('analysis_result', (data) => {
        document.getElementById('analysis-output').innerText = "Eval: " + data.score;
    });

    socket.on('hint_result', (data) => {
        const move = data.move; // e.g. "e2e4"
        const from = move.substring(0, 2);
        const to = move.substring(2, 4);

        // Highlight hint
        clearHighlights();

        boardGroup.children.forEach(mesh => {
            if (mesh.userData.square === from || mesh.userData.square === to) {
                mesh.material.color.setHex(0x0000ff); // Blue for hint
                highlightedSquares.push(mesh);
            }
        });

        alert("Hint: " + from + " to " + to);
    });
}

// Start
init();
