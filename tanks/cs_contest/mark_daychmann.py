def nplayers(grid, player_pos):
    x, y = player_pos
    pos = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                pos.append((i,j))

    pos.remove((x,y))
    return pos

def positionrisk(player_pos):
    x, y = player_pos
    if (x, y) in ((0,0), (0,8), (8,0), (8,8)):
        return 0
    elif x == 0 or y == 0 or x == 7 or y == 7:
        return 0.1
    elif x == 1 or y == 1 or x == 6 or y == 6:
        return 0.3
    elif x == 2 or y == 2 or x == 5 or y == 5:
        return 0.5
    elif x == 3 or y == 3 or x == 4 or y == 4:
        return 0.7

def invasionrisk(grid, test_pos, current):
    x, y = test_pos
    xcur, ycur = current
    risk = 0
    for i in range(-1, 2):
        if x + i < 0 or x + i > 7:
            continue
        for j in range(8):
            if (x+i, j) == (xcur, ycur):
                continue
            if grid[x + i][j] == 1:
                if i == 0:
                    risk += 1.0
                else:
                    risk += 0.3
    
    for i in range(-1, 2):
        if y + i < 0 or y + i > 7:
            continue
        for j in range(8):
            if (j, y+i) == (xcur, ycur):
                continue
            if grid[j][y + i] == 1:
                if i == 0:
                    risk += 1.0
                else:
                    risk += 0.3

    return risk

def legalmoves(grid, player_pos):
    x, y = player_pos
    # Stay, left, right, up, down
    possible_moves = [(x,y)]
    if y > 0 and grid[x][y-1] != 1:
        possible_moves.append((x, y-1))
    if y < 7 and grid[x][y+1] != 1:
        possible_moves.append((x, y+1)) 
    if x > 0 and grid[x-1][y] != 1:
        possible_moves.append((x-1, y))
    if x < 7 and grid[x+1][y] != 1:
        possible_moves.append((x+1, y))
     
    return possible_moves

def evaluaterisk(grid, player_pos, current):
    # Extra terms might be added later
    return invasionrisk(grid, player_pos, current) + positionrisk(player_pos)

def howtogetthere(destination, player_pos):
    x = destination[0] - player_pos[0]
    y = destination[1] - player_pos[1]
    if x == -1:
        return 0
    if x == 1:
        return 2
    if y == -1:
        return 3
    if y == 1:
        return 1
    return 8

def aim(grid, positions, player_pos):
    targets = []
    shootingdirections = {4:0, 5:0, 6:0, 7:0} # Counts the probability of hitting someone by shooting in the said direction
    x, y = player_pos
    for tank in positions:
        for move in legalmoves(grid, tank):
            targets.append(move)
    for xtarget, ytarget in targets:
        if xtarget == x:
            if ytarget < y:
                shootingdirections[7] += 1
            elif ytarget > y:
                shootingdirections[5] += 1
        elif ytarget == y:
            if xtarget < x:
                shootingdirections[4] += 1
            elif xtarget > x:
                shootingdirections[6] += 1
    bestdirection = max(shootingdirections, key = shootingdirections.get)
    if shootingdirections[bestdirection] == 0: # If you cannot hit anyone, move instead
        bestdirection = -1 
    return bestdirection

def _play_turn(grid, player_pos): 
    positions = nplayers(grid, player_pos)
    threshholdForShooting = 0.3 * (len(positions) - 1) # The more players there are the more defensive is the tank
    # Staying on the line/row with someone else carries the risk 1.0
    # Staying on the adjacent line/row with someone else carries the risk 0.3
    # The risks accumulate from different tanks
    # There is also an incentive to move towards the corners, as the limit the number of way you can be killed
    # The risk of staying/moving in the center ring is 0.7
    # The second ring is 0.5
    # The third ring is 0.3
    # The outer ring is 0.1
    # The corners carry no risks
    # In safe mode, the tank doesn't attack (unless the best move is to stay)
    # In which case, he attacks in the most likely direction 
    
    legalmov = legalmoves(grid, player_pos) # Find the legal moves (walls, other tanks)
    risks = {i:evaluaterisk(grid, i, player_pos) for i in legalmov} # Find the risks associated to these positions
    lowestriskposition = min(risks, key = risks.get) # Find the position with the smallest risk
    if risks[lowestriskposition] <= threshholdForShooting:
        move = howtogetthere(lowestriskposition, player_pos) # Returns a move (up, down, left, right, stay)
    else:
        move = aim(grid, positions, player_pos) # Aims the tank!
        if move == -1:
            move = howtogetthere(lowestriskposition, player_pos) # If the tank cannot possibly hit anyone, move instead
    return move

def play_turn(grid, player_pos):
    try:
        return _play_turn(grid, player_pos)
    except:
        return 5