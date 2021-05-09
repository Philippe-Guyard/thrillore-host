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
    #o(n^2), probably need to optimise
    #probably need to use shortest path to choose return point
    death = [] #cant go there
    (x,y) = player_pos
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 2:
                death.append(i)
                death.append(j)
            elif grid[i][j] == 1 and (i not in death and j not in death): #even if position changes might as well try to shoot
                if i == x:
                    if j < y:
                        return 7
                    else:
                        return 5
                if j == y:
                    if i < x:
                        return 4
                    else:
                        return 6
            elif grid[i][j] == 0 and (i not in death and j not in death):
                if i == x:
                    if j < y:
                        return 3
                    else:
                        return 1
                if j == y:
                    if i < x:
                        return 0
                    else:
                        return 2
            else:
                return 8


#print(play_turn([[0,0,0,0],[0,1,2,0],[1,2,0,0],[2,2,0,0]], (0,2)))
