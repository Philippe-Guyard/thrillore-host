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
turn = 0
goal = ""
boom = False


def play_turn(grid, players_pos):
    try:
        return __play_turn(grid, players_pos)
    except:
        return SHOOT_LEFT

def __play_turn(grid, player_pos):
    '''
    The goal is to go to a corner and then just shoot in the two directions
    '''

    global turn
    global goal
    global boom
    boom = not boom # alternate between true and false to alternate between shots in corners
        

    # Initiate goal
    if turn == 0:
        lu_quad = 0
        ld_quad = 0
        ru_quad = 0
        rd_quad = 0
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == 1:
                    if i <=3 and j <= 3:
                        lu_quad += 1
                    elif i <= 3 and j >= 4:
                        ru_quad += 1
                    elif i >= 4 and j <= 3:
                        ld_quad += 1
                    elif i >= 4 and j >= 4:
                        rd_quad += 1
        data = {'lu_quad': lu_quad, 'ld_quad': ld_quad, 'ru_quad': ru_quad, 'rd_quad': rd_quad}
        goal = min(data.items(), key = lambda item: item[1])[0]
        turn += 1 #increment turn
    pos_y, pos_x = player_pos[0],player_pos[1]
    tank_in_row = False
    tank_in_col = False
    #data = {'lu_quad': 1, 'ld_quad': 2, 'ru_quad': 3, 'rd_quad': 4}
    
    tank_in_left_col = False
    tank_in_right_col = False

    tank_in_up_row = False
    tank_in_down_row = False
    # check own row and column first for tanks, if tanks are there then shoot
    for j in range(len(grid)):
        if grid[pos_y][j] == 1:
            if j < pos_x:
                return SHOOT_LEFT
            else:
                return SHOOT_RIGHT
        if grid[j][pos_x] == 1:
            if j < pos_y:
                return SHOOT_UP
            else:
                return SHOOT_DOWN
        #check if adjacent row and column is empty
        if goal == "lu_quad":
            if grid[pos_y-1][j] == 1:
                tank_in_up_row = True
            if grid[j][pos_x-1]:
                tank_in_left_col = True
        if goal == "ld_quad":
            if grid[pos_y+1][j] == 1:
                tank_in_down_row = True
            if grid[j][pos_x-1]:
                tank_in_left_col = True
        if goal == "ru_quad":
            if grid[pos_y-1][j] == 1:
                tank_in_up_row = True
            if grid[j][pos_x+1]:
                tank_in_right_col = True
        if goal == "rd_quad":
            if grid[pos_y+1][j] == 1:
                tank_in_down_row = True
            if grid[j][pos_x+1]:
                tank_in_right_col = True

    # if in corner then shoot left and right alternatingly
    if goal == "lu_quad" and pos_y == 0 and pos_x == 0:
        if boom:
            return SHOOT_RIGHT
        else:
            return SHOOT_DOWN
    if goal == "ld_quad" and pos_y == 7 and pos_x == 0:
        if boom:
            return SHOOT_RIGHT
        else:
            return SHOOT_UP
    if goal == "ru_quad" and pos_y == 0 and pos_x == 7:
        if boom:
            return SHOOT_LEFT
        else:
            return SHOOT_DOWN
    if goal == "rd_quad" and pos_y == 7 and pos_x == 7:
        if boom:
            return SHOOT_LEFT
        else:
            return SHOOT_UP

    #try and move towards the corner
    if not tank_in_up_row and (goal == "lu_quad" or goal == "ru_quad"):
        return MOVE_UP
    if not tank_in_left_col and (goal == "lu_quad" or goal == "ld_quad"):
        return MOVE_LEFT
    if not tank_in_down_row and (goal == "ld_quad" or goal == "rd_quad"):
        return MOVE_DOWN
    if not tank_in_right_row and (goal == "rd_quad" or goal == "ru_quad"):
        return MOVE_RIGHT
    else:
        return STAND_STILL 