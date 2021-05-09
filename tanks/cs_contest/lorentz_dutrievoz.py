MOVE_UP = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
SHOOT_UP = 4
SHOOT_RIGHT = 5
SHOOT_DOWN = 6
SHOOT_LEFT = 7
STAND_STILL = 8



def play_turn(grid, player_pos):
    (i,j) = player_pos 

    if i>0:
        return MOVE_LEFT

    if j<=7:
        return SHOOT_RIGHT
    return MOVE_UP