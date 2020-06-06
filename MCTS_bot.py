from game import Game
import random
from mcts import mcts
import copy
import numpy as np
from time import sleep 

def check_win(tile):
    for tick in ['X', 'O']:
        for i in range(3):
            if all(tick == x for x in tile[i * 3 : (i * 3) + 3]):
                return tick

        for i in range(3):
            if all(tick == x for x in tile[[i, i + 3, i + 6]]):
                return tick
        
        if all(tick == x for x in tile[[0, 4, 8]]) or all(tick == x for x in tile[[2, 4, 6]]):
            return tick
        
    return '-' if all(x != '.' for x in tile) else '.'

class Game_State:
    def __init__(self, board: np.array([[str]]), forced_move: list(Game.map_tile.keys()), init_player: str):
        self.board = board.copy()
        self.forced_move = copy.copy(forced_move)
        self.init_player = init_player
        self.current_player = init_player

    def getCurrentPlayer(self):
        return 1 if self.current_player == self.init_player else -1
    
    def getPossibleActions(self):
        actions = []

        for i in self.forced_move:
            for j in np.where(self.board[i] == '.')[0]:
                actions.append((i, j))
        
        return actions

    def takeAction(self, action):
        next_state = self.copy()
        next_state.board[action[0]][action[1]] = self.current_player

        tile_wins = [check_win(row) for row in next_state.board]
                
        if tile_wins[action[1]] == '.':
            next_state.forced_move = [action[1]]
        else:
            next_state.forced_move = np.where(np.array(tile_wins) == '.')[0]

        next_state.current_player = 'X' if self.current_player == 'O' else 'O'

        return next_state

    def isTerminal(self):
        tile_wins = np.array([check_win(tile) for tile in self.board])

        return check_win(tile_wins) != '.' or not '.' in tile_wins

    def getReward(self):
        tile_wins = np.array([check_win(tile) for tile in self.board])

        return 1 if check_win(tile_wins) == self.init_player else (0 if not '.' in tile_wins else -1)

    def copy(self):
        state = Game_State(self.board, self.forced_move, self.init_player)
        state.current_player = self.current_player
        return state

    def __eq__(self, other):
        return isinstance(other, Game_State) and np.array_equal(other.board, self.board)
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        s = "\n\n"

        for i in range(3):
            s += "-" * 25 + '\n'
            for j in range(3):
                s += "| " + " ".join(self.board[i * 3][j * 3 : (j * 3) + 3]) + " | " + " ".join(self.board[(i * 3) + 1][j * 3 : (j * 3) + 3]) + " | " + " ".join(self.board[(i * 3) + 2][j * 3 : (j * 3) + 3]) + " |" + '\n'

        s += "-" * 25

        return s

class bot:
    def __init__(self):
        self.team_name = "MCTS"
        self.monte_carlo_tree = None
        self.tick = None
        
    def move(self, board: np.array([[str]]), forced_move: list(Game.map_tile.keys())):
        if self.tick == None:
            if forced_move == None or len(forced_move) > 1:
                self.tick = "X"
            else:
                self.tick = "O"

        coordinate_map = {}

        for (key, value) in Game.map_tile.items():
            coordinate_map[value] = key

        mc = mcts(500)

        action = mc.search(Game_State(board, [Game.map_tile[x] for x in forced_move], self.tick))

        return [coordinate_map[x] for x in action]