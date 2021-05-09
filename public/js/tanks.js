const GRID_SIDE = 8;
const DIRECTION_UP = 0;
const DIRECTION_DOWN = 1;
const DIRECTION_LEFT = 2;
const DIRECTION_RIGHT = 3;

const toID = (x, y) => GRID_SIDE * x + y + 1; //id is 1-indexed
const fromID = id => {return {x: Math.floor((id - 1) / GRID_SIDE), y: (id - 1) % GRID_SIDE}}

const loadData = () => {
    return $.getJSON("data/data.json");
}

const fillGrid = () => {
    function createnewCell(id) {
        const templateHtml = $("#template_grid_cell").html();
        const templateWithID = templateHtml.replace('{CELL_ID}', `cell-${id}`);
        const gridCell = $.parseHTML(templateWithID);
        $(gridCell).appendTo(".grid");
    }

    for (let i = 0; i < GRID_SIDE * GRID_SIDE; i++) {
        createnewCell(i + 1);
    }
}

$(document).ready(async function () {
    const data = await loadData();

    fillGrid();

    const gameManager = new GameManager(data.grid_history, data.player_count, data.die_history, data.shoot_history, data.alive_history);
    //WAit for pictures to load
    setTimeout(() => {
        setInterval(() => gameManager.loopOnce(), 60);
    }, 2000);
});

class GameManager {
    constructor(gridHistory, playerCount, dieHistory, shootHistory, aliveHistory) {
        this.blueTankImage = new Image();
        this.blueTankImage.src = 'data/bluetank.png';
        this.blueTankImage.onload = () => {
            console.log('Blue loaded!');
            this.isBlueLoaded = true; //anonymous function keeps 'this' as GameManager
        }

        this.explosionImage = new Image();
        this.explosionImage.src = 'data/explosion.png';

        this.frameCount = 0;
        this.turn = 0;
        this.tankFrame = 0;

        this.gridHistory = gridHistory;
        this.dieHistory = dieHistory;
        this.shootHistory = shootHistory;
        this.aliveHistory = aliveHistory;

        this.players = [];
        for(let i = 0; i < playerCount; i++)
            this.players.push({id: -1, direction: DIRECTION_UP, dead: false, explosionFrame: 0, waitFrames: 0});

        this.gameFinished = false;

        this.tableHeadStr = $('#table_head').html();
        this.tableRowTemplateStr = $('#template_player_line').html();
        this.gameOverDrawn = false;
    }

    _getCtxFromID(cellID) {
        const canvas = document.getElementById(`cell-${cellID}`);
        const ctx = canvas.getContext("2d");

        return { ctx, width: canvas.width, height: canvas.height };
    }

    _getPlayerFromStr(s) {
        const playerIdx = Number.parseInt(s[s.length - 1]);
        return this.players[playerIdx - 1];
    }

    _clearCell(cellID) {
        //clear laser
        $(`#cell-${cellID}`).css('background-color', 'rgba(238, 228, 218, 0.35)');

        //clear images
        const { ctx, width, height } = this._getCtxFromID(cellID);
        ctx.clearRect(0, 0, width, height);
    }

    _drawLaser(cellID) {
        $(`#cell-${cellID}`).css('background-color', 'red');
    }

    //direction: one of DIRECTION_UP, DIRECTION_DOWN, ... 
    //xFrame is the current animation frame
    _drawBlueTank(cellID, direction, xFrame = 0) {
        if (!this.isBlueLoaded) {
            console.log('not loaded');
            return false;
        }

        this._clearCell(cellID);
        const { ctx, width, height } = this._getCtxFromID(cellID);
        ctx.drawImage(this.blueTankImage, 32 * xFrame, 32 * direction, 32, 32, 0, 0, width, height);

        return true;
    }

    _drawExplosion(cellID, xFrame, yFrame) {
        this._clearCell(cellID);
        const { ctx, width, height } = this._getCtxFromID(cellID);
        ctx.drawImage(this.explosionImage, 100 * xFrame, 100 * yFrame, 100, 100, 0, 0, width, height);
        return true;
    }

    _moveTank(oldID, newID, xFrame = 0) {
        this._clearCell(oldID);
        let direction;
        if (newID == oldID + 1)  //Move to the right
            direction = DIRECTION_RIGHT;
        else if (newID == oldID - 1)
            direction = DIRECTION_LEFT;
        else if (newID == oldID + GRID_SIDE)
            direction = DIRECTION_DOWN;
        else
            direction = DIRECTION_UP;

        this._drawBlueTank(newID, direction, xFrame);
        return direction;
    }

    _drawDeadPlayers() {
        let allDead = true;
        for (let player of this.players) {
            if (player.dead && player.explosionFrame < 75) {
                if (player.waitFrames < 3) {
                    this._drawBlueTank(player.id, player.direction, this.tankFrame);
                    player.waitFrames += 1;
                }
                else {
                    this._drawExplosion(player.id, player.explosionFrame % 9, Math.floor(player.explosionFrame / 9));
                    player.explosionFrame += 2;
                }
                allDead = false;
            }
        }

        return allDead;
    }

    _updateLeaderboard() {
        const alivePlayers = this.aliveHistory[this.turn];
        let newHtml = this.tableHeadStr + '\n';
        for (let player of alivePlayers) {
            newHtml += this.tableRowTemplateStr.replace('{HANDLE}', player);
        }
        $('#leaderboard').html(newHtml);
    }

    _gameOverScreen() {
        $('.overlay').fadeIn(1000);
        this.gameOverDrawn = true;
    }

    loopOnce() {
        if (this.gameFinished) {
            const allDead = this._drawDeadPlayers();
            if (allDead && !this.gameOverDrawn) {
                for (let id = 1; id <= GRID_SIDE * GRID_SIDE; id++)
                    this._clearCell(id);
                
                this._gameOverScreen();
            }
            return
        }
        
        if (this.frameCount % 10 == 0) { 
            const dieResults = this.dieHistory[this.turn];
            for(let playerStr in dieResults) {
                const player = this._getPlayerFromStr(playerStr);
                const position = dieResults[playerStr];
                player.dead = true;
                player.id = toID(position[0], position[1]);
            }

            const shootResults = this.shootHistory[this.turn];
            for(let playerKey in shootResults) {
                const shootResult = shootResults[playerKey];
                const player = this._getPlayerFromStr(playerKey);
                const direction = {
                    'UP': DIRECTION_UP,
                    'LEFT': DIRECTION_LEFT,
                    'RIGHT': DIRECTION_RIGHT,
                    'DOWN': DIRECTION_DOWN}[shootResult];
                
                player.direction = direction;
            }

            const grid = this.gridHistory[this.turn];
            for(let i = 0; i < GRID_SIDE; i++) {
                for(let j = 0; j < GRID_SIDE; j++) {
                    const curID = toID(i, j);
                    this._clearCell(curID); //clear all cells before doing anything
                    if (grid[i][j].startsWith('P')) {
                        const player = this._getPlayerFromStr(grid[i][j]); 
                        if (player.id == -1)
                            player.id = curID;

                        if (player.id != curID) {
                            player.direction = this._moveTank(player.id, curID, this.tankFrame);
                            player.id = curID;
                        }
                        else 
                            this._drawBlueTank(player.id, player.direction, this.tankFrame);                        

                    }
                    else if (grid[i][j] == '2') 
                        this._drawLaser(curID);
                }
            }

            this._updateLeaderboard();

            this.turn++;
            this.gameFinished = this.turn == this.gridHistory.length;
        }
        else {
            for(let player of this.players) {
                if (player.dead)
                    continue;
                    
                this._drawBlueTank(player.id, player.direction, this.tankFrame);
            }
        }
        this._drawDeadPlayers();

        this.frameCount++;
        this.tankFrame = (this.tankFrame + 1) % 7; //7 frames in animation
    }
}