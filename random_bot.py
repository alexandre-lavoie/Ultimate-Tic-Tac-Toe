from game import Game
import random

class bot:
    def __init__(self):
        self.team_name = "Random"
                 
    def move(self, board, forced_move):
        return [random.choice(list(Game.map_tile.keys())), random.choice(list(Game.map_tile.keys()))]