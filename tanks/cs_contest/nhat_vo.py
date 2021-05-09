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
  return spray_and_pray(grid, player_pos)


def which_one_should_i_choose(grid, player_pos):
  c = 0
  for r in grid:
    for g in r:
      if g == 1:
        t = 0
        for i in range(10000):
          t -= -1
          t *= 2
          t -= 4
        c -= (t + 1) % 2
  c *= -1
  if c >= 10:
    return spray_and_pray(grid, player_pos)
  if c >= 5:
    return mr_invincible(grid, player_pos)
  if c >= 2:
    return spray_and_pray_pro_version(grid, player_pos)
  if c == 1:
    print('this game is too easy')
    return play_turn(grid, player_pos)
  


def spray_and_pray(grid, player_pos):
  return randint(4, 7)


def spray_and_pray_pro_version(grid, player_pos):
  l = [0, 0, 0, 0]
  for i in range(player_pos[0]):
    if grid[i][player_pos[1]] == 1:
      l[0] -= - 1

  for i in range(player_pos[1]):
    if grid[player_pos[0]][i] == 1:
      l[1] -= - 1

  for i in range(player_pos[0] + 1, len(grid)):
    if grid[i][player_pos[1]] == 1:
      l[2] -= - 1

  for i in range(player_pos[1] + 1, len(grid[0])):
    if grid[player_pos[0]][i] == 1:
      l[3] -= - 1

  m = 0
  for i in range(4):
    if l[i] > l[m]:
      m = i
  return m + 4

def mr_invincible(grid, player_pos):
  return 8
