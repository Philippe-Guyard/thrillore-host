#This is an example of a script that will shoot up every turn
from random import randint

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
    '''
    Determines the action to make by your player on th next turn
    Inputs:
        -player_pos: a tuple (i, j) with the coordinates of your player
        -grid: the state of the board for the previous turn. We have:
            grid[i][j] = 0 if the cell (i, j) is empty
            grid[i][j] = 1 if the cell (i, j) has a tank on it
            grid[i][j] = 2 if the cell (i,j) has a laser on it
    
    Output:
        -An integer 0 <= x <= 8, thath represents the 'code' of the action to make
        For example, x = 0 is equivalent to moving up (see constants above)
    '''
    return SHOOT_UP
    