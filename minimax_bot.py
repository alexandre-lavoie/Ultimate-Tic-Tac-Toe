from game import Game
import random
import numpy as np

class bot:
    def __init__(self):
        self.team_name = "Minimax"
        self.tick = None
        self.max_depth = 4
        self.coordinate_map = {}

        for (key, value) in Game.map_tile.items():
            self.coordinate_map[value] = key

    def check_win(self, tile):
        # Horizontal
        for i in range(3):
            if all(self.tick == x for x in tile[i * 3 : (i * 3) + 3]):
                return 1
            elif all(("O" if self.tick == "X" else "X") == x for x in tile[i * 3 : (i * 3) + 3]):
                return -1

        # Vertical
        for i in range(3):
            if all(self.tick == x for x in tile[[i, i + 3, i + 6]]):
                return 1
            elif all(("O" if self.tick == "X" else "X") == x for x in tile[[i, i + 3, i + 6]]):
                return -1
        
        # Diagonal
        if all(self.tick == x for x in tile[[0, 4, 8]]) or all(self.tick == x for x in tile[[2, 4, 6]]):
            return 1
        elif all(("O" if self.tick == "X" else "X") == x for x in tile[[0, 4, 8]]) or all(("O" if self.tick == "X" else "X") == x for x in tile[[2, 4, 6]]):
            return -1

        return 0

    def calculate_score(self, board, depth):
        if depth == 0:
            return 0
        
        score = 0

        win_states = np.array([])

        for tile in board:
            win = self.check_win(tile)

            win_states = np.append(win_states, self.tick if win == 1 else ('.' if win == 0 else ("O" if self.tick == "X" else "X")))

            if win != 0:
                score += win * 100
            else:
                score += sum((1 if x == self.tick else (0 if x == None else -1)) for x in tile) ** 2

        score += self.check_win(win_states) * 1000

        return score * (self.max_depth - depth)

    def minimax(self, board, forced_index, isMe, depth):
        scores = []

        if depth == self.max_depth - 1:
            return (None, None, self.calculate_score(board, depth))

        for i in forced_index:
            for j, e in enumerate(board[i]):
                if e == '.':
                    board[i][j] = self.tick if isMe else ("O" if self.tick == "X" else "X")

                    won_board = False

                    if self.check_win(board[i]) != 0:
                        next_moves = [k for k, x in enumerate(board) if self.check_win(x) == 0]
                        win_board = True
                    else:
                        next_moves = [j]

                    scores.append((i, j, self.minimax(board, next_moves, not isMe, depth + 1)[2]))
                    board[i][j] = '.'

        if len(scores) == 0:
            return (None, None, 0)

        if isMe:
            return max(scores, key=lambda x: x[2])
        else:
            return min(scores, key=lambda x: x[2])
        
            
    def move(self, board, forced_move):
        if self.tick == None:
            if len(forced_move) > 1:
                self.tick = "X"

                return ['C', 'C']
            else:
                self.tick = "O"

        if len(forced_move) > 1:
            moves = [k for k, x in enumerate(board) if self.check_win(x) == 0]
        else:
            moves = [Game.map_tile[m] for m in forced_move]
        
        print([self.coordinate_map[x] for x in moves])

        move_i, move_j, score = self.minimax(board, moves, True, 0)

        if move_i == None:
            return [random.choice(forced_move), random.choice(list(Game.map_tile.keys()))]
        else:
            return [self.coordinate_map[move_i], self.coordinate_map[move_j]]
