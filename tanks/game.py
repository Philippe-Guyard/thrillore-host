from random import randint

#NOTE: This architecture is far from perfect, but I coded the entire game in a couple hours, so don't judge me

class Tile:
    EMPTY = 0
    TANK = 1
    LASER = 2

    def __init__(self, state=EMPTY):
        self.state = state
        self.player = None
        self.last_update = 0

    def set_state(self, new_state, turn, player=None):
        #Laser are nver overwritten on the same turn 
        if self.state == Tile.LASER and self.last_update == turn:
            self.player = player
        else:
            self.state = new_state
            self.player = player
            self.last_update = turn

    def __str__(self):
        return self.state


class Player:
    def __init__(self, action_func, position, initial_index, label):
        self.play_turn = action_func
        self.position = position
        self.initial_index = initial_index
        self.label = label

    def __str__(self):
        return 'P' + str(self.initial_index + 1)


class Game:
    GRID_SIDE = 8

    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    SHOOT_UP = 4
    SHOOT_RIGHT = 5
    SHOOT_DOWN = 6
    SHOOT_LEFT = 7
    STAND_STILL = 8

    MAX_TURNS = 80

    @staticmethod
    def get_random_coord():
        return randint(0, Game.GRID_SIDE - 1)

    def __init__(self, actions_funcs):
        self.grid = [[Tile() for _ in range(Game.GRID_SIDE)]
                     for _ in range(Game.GRID_SIDE)]

        self.players = []
        for action_func, label in actions_funcs:
            position = (Game.get_random_coord(), Game.get_random_coord())
            while self.at(position).state == 1:
                position = (Game.get_random_coord(), Game.get_random_coord())

            new_player = Player(action_func, position, len(self.players), label)
            self.players.append(new_player)
            
            self.at(position).set_state(Tile.TANK, 0, self.players[-1])

        # Maps action code -> function that accepts player
        self.action_map = {
            Game.MOVE_UP: lambda player: self._move(player, (player.position[0], player.position[1] + 1)),
            Game.MOVE_RIGHT: lambda player: self._move(player, (player.position[0] + 1, player.position[1])),
            Game.MOVE_DOWN: lambda player: self._move(player, (player.position[0], player.position[1] - 1)),
            Game.MOVE_LEFT: lambda player: self._move(player, (player.position[0] - 1, player.position[1])),
            Game.SHOOT_UP: lambda player: self._shoot(player, Game.SHOOT_UP),
            Game.SHOOT_RIGHT: lambda player: self._shoot(player, Game.SHOOT_RIGHT),
            Game.SHOOT_DOWN: lambda player: self._shoot(player, Game.SHOOT_DOWN),
            Game.SHOOT_LEFT: lambda player: self._shoot(player, Game.SHOOT_LEFT),
            Game.STAND_STILL: lambda player: None #do nothing
        }

        self.state_history = []
        self.die_history = []
        self.shoot_history = []
        self.alive_history = []

        self.game_ended = False
        self.turn = 0

    def at(self, position):
        return self.grid[position[0]][position[1]]

    def _move(self, player, new_pos):
        newpos_is_valid = 0 <= new_pos[0] < Game.GRID_SIDE and 0 <= new_pos[1] < Game.GRID_SIDE
        #tanks cannot collid
        if newpos_is_valid and self.at(player.position).state != Tile.TANK:
            self.at(player.position).set_state(Tile.EMPTY, self.turn)
            player.position = new_pos
            self.at(new_pos).set_state(Tile.TANK, self.turn, player)
            return True
        else:
            return False

    def _shoot(self, player, action):
        if action == Game.SHOOT_RIGHT:
            for j in range(player.position[1] + 1, Game.GRID_SIDE):
                pos = (player.position[0], j)
                self.at(pos).set_state(Tile.LASER, self.turn)
        elif action == Game.SHOOT_DOWN:
            for i in range(player.position[0] + 1, Game.GRID_SIDE):
                pos = (i, player.position[1])
                self.at(pos).set_state(Tile.LASER, self.turn)
        elif action == Game.SHOOT_LEFT:
            for j in range(0, player.position[1]):
                pos = (player.position[0], j)
                self.at(pos).set_state(Tile.LASER, self.turn)
        else:
            for i in range(0, player.position[0]):
                pos = (i, player.position[1])
                self.at(pos).set_state(Tile.LASER, self.turn)

    def _gen_killer_cloud(self):
        #every 20 turns there is one layer
        cloud_size = min(self.turn // 20, Game.GRID_SIDE // 2)
        for i in range(Game.GRID_SIDE):
            for j in range(cloud_size):
                pos_left = (i, j)
                self.at(pos_left).set_state(Tile.LASER, self.turn)

                pos_right = (i, Game.GRID_SIDE - j - 1)
                self.at(pos_right).set_state(Tile.LASER, self.turn)
        
        for i in range(cloud_size):
            for j in range(Game.GRID_SIDE):
                pos_up = (i, j)
                self.at(pos_up).set_state(Tile.LASER, self.turn)

                pos_bottom = (Game.GRID_SIDE - i - 1, j)
                self.at(pos_bottom).set_state(Tile.LASER, self.turn)

    def play_turn(self):
        if self.game_ended:
            return

        # keep the state grid as 'previous turn'
        state_grid = [[tile.state for tile in row] for row in self.grid]
        shoot_results = dict()
        for player in self.players:
            turn_result = player.play_turn(state_grid, player.position)

            self.action_map[turn_result](player)
            if turn_result == Game.SHOOT_RIGHT:
                shoot_results[str(player)] = 'RIGHT'
            if turn_result == Game.SHOOT_LEFT:
                shoot_results[str(player)] = 'LEFT'
            if turn_result == Game.SHOOT_UP:
                shoot_results[str(player)] = 'UP'
            if turn_result == Game.SHOOT_DOWN:
                shoot_results[str(player)] = 'DOWN'

        #remove previous lasers
        for i in range(Game.GRID_SIDE):
            for j in range(Game.GRID_SIDE):
                tile = self.at((i, j))
                # this tile was a laser on the turn before the current one, hence it becomes empty
                if tile.state == Tile.LASER and tile.last_update < self.turn:
                    tile.set_state(Tile.EMPTY, self.turn)

        #generate the killer cloud now that we removed old lasers
        self._gen_killer_cloud()

        # state grid for this turn (previous lasers are removed and new actions taken into account)
        state_grid = [[tile.state for tile in row]
                      for row in self.grid]

        to_remove = []
        die_results = dict()
        for idx, player in enumerate(self.players):
            # player is hit by lase
            if state_grid[player.position[0]][player.position[1]] == Tile.LASER:
                to_remove.append(idx)
                die_results[str(player)] = player.position
            else:
                state_grid[player.position[0]][player.position[1]
                                               ] = str(player)

        for idx, remove_idx in enumerate(to_remove):
            # idx = offset (we remove exactly idx tanks before)
            self.players.pop(remove_idx - idx)

        self.state_history.append([[str(x) for x in row]
                                  for row in state_grid])
        self.die_history.append(die_results)
        self.shoot_history.append(shoot_results)
        self.alive_history.append([p.label for p in self.players])

        self.game_ended = len(self.players) <= 1 or self.turn > Game.MAX_TURNS
        self.turn += 1
