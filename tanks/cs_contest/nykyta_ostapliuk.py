MOVE_UP = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
SHOOT_UP = 4
SHOOT_RIGHT = 5
SHOOT_DOWN = 6
SHOOT_LEFT = 7
STAND_STILL = 8

my_lovely_corner = None
corner_reached = False
direction = -1

def find_target(grid, my_i, my_j):
    for i in range(8):
        if i != my_i and grid[i][my_j] == 1:
            return SHOOT_UP if i < my_i else SHOOT_DOWN
    for j in range(8):
        if j != my_j and grid[my_i][j] == 1:
            return SHOOT_LEFT if j < my_j else SHOOT_RIGHT

    for i in range(8):
        if i != my_i and ((my_j+1 < 8 and grid[i][my_j+1] == 1) or (my_j > 0 and grid[i][my_j-1] == 1)):
            return SHOOT_UP if i < my_i else SHOOT_DOWN
    for j in range(8):
        if j != my_j and ((my_i+1 < 8 and grid[my_i+1][j] == 1) or (my_i > 0 and grid[my_i-1][j] == 1)):
            return SHOOT_LEFT if j < my_j else SHOOT_RIGHT

    return None


def play_turn(grid, player_pos):
    '''
    Determines the action to make by your player on th next turn
    Inputs:
        -player_pos: a tuple (i, j) with the coordinates of your player
        -grid: the state of the board for the previous turn. We have:
            grid[i][j] = 0 if the cell (i, j) is empty
            grid[i][j] = 1 if the cell (i, j) has a tank on it
            grid[i][j] = 2 if the cell (i,j) has a laser on it

    Output:
        -An integer 0 <= x <= 8, that represents the 'code' of the action to make
        For example, x = 0 is equivalent to moving up (see constants above)
    '''

    global my_lovely_corner
    global corner_reached
    global direction

    my_i, my_j = player_pos
    if my_lovely_corner is None:
        my_lovely_corner = (0 if my_i < 4 else 7, 0 if my_j < 4 else 7)

    if player_pos == my_lovely_corner:
        corner_reached = True

    target = find_target(grid, my_i, my_j)
    if target is not None:
        return target

    if corner_reached:
        direction = (direction + 1) % 2
        if direction == 0:
            return MOVE_UP if my_lovely_corner[0] == 7 else MOVE_DOWN
        else:
            return MOVE_LEFT if my_lovely_corner[1] == 7 else MOVE_RIGHT
    else:
        if my_i != my_lovely_corner[0]:
            return MOVE_UP if my_lovely_corner[0] == 0 else MOVE_DOWN
        else:
            return MOVE_LEFT if my_lovely_corner[1] == 0 else MOVE_RIGHT

