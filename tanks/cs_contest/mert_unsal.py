#This is an example of a script that will shoot up every turn
import numpy as np
import random

MOVE_UP = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
SHOOT_UP = 4
SHOOT_RIGHT = 5
SHOOT_DOWN = 6
SHOOT_LEFT = 7
STAND_STILL = 8

def check(i,j):
    if i >= 8 or i < 0 or j >= 8 or j < 0:
        return False
    return True

def play_turn(grid, player_pos):
    ''''    
    Determines the action your player will make on the next turn
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
    
    # let's preprocess the current condition of the grid
    S = 8
    i0, j0 = player_pos
    
    # find locations of the players
    players = []
    N = 0
    for i in range(S):
        for j in range(S):
            if grid[i][j] == 1 and not(i == i0 and j == j0): # avoid counting myself
                N += 1
                players.append((i,j))
                
    # now we have the number of players 'N' and locations of the players in the list 'players'
    # let us find the dangerous locations in which other players can shoot so that we avoid them
    # all players can shoot up down right left so if a location has the same i or same j with a player it's a dangerous spot
    # I guess i is the row and j is the column
    # dangerous[i][j] = 1 if the place is dangerous else it's 0
    dangerous = np.zeros((S,S))
    for i in range(S):
        for j in range(S):
            for player in players:
                pi, pj = player
                if pi == i or pj == j:
                    dangerous[i][j] = 1
                    
                    
    # now let's check if we're in a dangerous location, then we have to move
    if dangerous[i0][j0] == 1:
        # goddamn it bruh
        # we gotta move those refrigerators : https://www.youtube.com/watch?v=wTP2RUD_cL0
        OPTIONS = []
        
        # down
        if check(i0 + 1, j0) and dangerous[i0 + 1][j0] == 0:
            OPTIONS.append(2)
            
        # up
        if check(i0 - 1, j0) and dangerous[i0 - 1][j0] == 0:
            OPTIONS.append(0)
            
        # left
        if check(i0, j0-1) and dangerous[i0][j0 - 1] == 0:
            OPTIONS.append(3)
            
        # right
        if check(i0, j0 + 1) and dangerous[i0][j0 + 1] == 0:
            OPTIONS.append(1)
            
        # if there are no options, we're fucked, so we have to shoot back those bitches threatening us
        if len(OPTIONS) == 0:
            for player in players:
                pi, pj = player
                if pi == i0: # we are on the same row
                    if pj > j0: # he is on right
                        return 5
                    else:
                        return 7
                        
                elif pj == j0:
                    if pi > i0:
                        return 6
                    else:
                        return 4       
            
        else:
            # stochastically we should stay close to middle (assuming we start close to middle) so I don't see why we would need an optimization
            # also i am smarter than you so yeah... by lorentz dutrievoz
            # also staying close to the middle might not be the best way to go
            # could have done a better implementation but writing code at a party for Philippe so can't be bothered <3
            return random.choice(OPTIONS)
            
            
    else: # the case where we are not in a dangerous position: we try to shoot some bitches
    # to do that we look for locations they can possibly move and we can shoot at the same time, if not we stay still
    
        OPTIONS = []
        for player in players:
            pi, pj = player
            if (pi == i0 + 1 or pi == i0 - 1) and j > j0:
                OPTIONS.append(5)
                
            elif (pi == i0 + 1 or pi == i0 -1) and j < j0: 
                OPTIONS.append(7)
            
            elif (pj == j0 + 1 or pj == j0 - 1) and i > i0:
                OPTIONS.append(6)
                
            elif (pj == j0 + 1 or pj == j0 - 1) and i < i0:
                OPTIONS.append(4)
            
            
        if len(OPTIONS) == 0:
            return 8
        else:
            return random.choice(OPTIONS)
            
                
    
    