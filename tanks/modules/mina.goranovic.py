#This is an example of a script that will move in a circle
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

#We save this variable outside of the function
memory = 0

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
    global memory #tell python we will use the global variable 'memory'
    old_memory = memory #save the old value of memory

    #update our current memory
    memory = memory + 1 #go to the next action
    memory = memory % 4 #make sure we never overflow past 4 
    #NOTE: This script will make it's tank move in the order
    #UP - RIGHT - DOWN - LEFT

    return old_memory #return our saved version