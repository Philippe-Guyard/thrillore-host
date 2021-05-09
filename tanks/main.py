import os, json

from game import Game


def dynamic_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod

functions = []
DIR = 'cs_contest'
for filename in os.listdir(DIR):
    if filename.startswith('__'): #init or something
        continue
    
    if not filename.endswith('.py'):
        continue

    full_path = DIR + '.' + filename
    module = dynamic_import(full_path[:-3])
    functions.append((module.play_turn, filename[:-3]))



game = Game(functions)
for _ in range(Game.MAX_TURNS):
    game.play_turn()

d = {
    'grid_history': game.state_history,
    'turns': game.turn,
    'die_history': game.die_history,
    'shoot_history': game.shoot_history,
    'alive_history': game.alive_history,
    'player_count': len(functions)
}

json.dump(d, open('data.json', 'w'))
