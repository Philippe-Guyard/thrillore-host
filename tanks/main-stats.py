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
    
    if filename in ('evdokia_gneusheva.py', 'lorentz_dutrievoz.py', 'nhat_vo.py', 'mert_unsal.py', 'anonymous.py', 'mark_daychmann.py'):
        continue

    if not filename.endswith('.py'):
        continue

    full_path = DIR + '.' + filename
    module = dynamic_import(full_path[:-3])
    functions.append((module.play_turn, filename[:-3]))

wins = {}
draws = 0
for g in range(1000):
    game = Game(functions)
    for _ in range(50):
        game.play_turn()

    if len(game.players) < 2:
        for player in game.players:
            if player.label not in wins:
                wins[player.label] = 1
            else:             
                wins[player.label] += 1

tuple_wins = [(key, value) for key, value in wins.items()]
print(*sorted(tuple_wins, key=lambda x: x[1]))
'''
    d = {
        'grid_history': game.state_history,
        'turns': game.turn,
        'die_history': game.die_history,
        'shoot_history': game.shoot_history,
        'alive_history': game.alive_history,
        'player_count': len(functions)
    }

    json.dump(d, open('data.json', 'w'))
'''