import numpy as np


class Game:

    map_tile = {
        "NW": 0,
        "N": 1,
        "NE": 2,
        "W": 3,
        "C": 4,
        "E": 5,
        "SW": 6,
        "S": 7,
        "SE": 8,
    }

    def __init__(self):
        self.board = np.array([["." for x in range(9)] for _ in range(9)])
        self.win_status = np.array([None] * 9)
        self.player_turn = -1
        self.next_tile = Game.map_tile.keys()

    def _show_board(self):
        for i in range(3):
            print("-" * 25)
            for j in range(3):
                print(
                    "| "
                    + " ".join(self.board[i * 3][j * 3 : (j * 3) + 3])
                    + " | "
                    + " ".join(self.board[(i * 3) + 1][j * 3 : (j * 3) + 3])
                    + " | "
                    + " ".join(self.board[(i * 3) + 2][j * 3 : (j * 3) + 3])
                    + " |"
                )
        print("-" * 25)

    def status(self):
        print(
            f"Turn: Player {self.player_turn + 1} ({self.tick()})'s\nPossible tile: {self.next_tile}"
        )
        self._show_board()
        print()

    def check_win(self, tile):
        tick = self.tick()

        # Horizontal
        for i in range(3):
            if all(tick == x for x in tile[i * 3 : (i * 3) + 3]):
                return True

        # Vertical
        for i in range(3):
            if all(tick == x for x in tile[[i, i + 3, i + 6]]):
                return True

        # Diagonal
        return all(tick == x for x in tile[[0, 4, 8]]) or all(
            tick == x for x in tile[[2, 4, 6]]
        )

    def check_draw(self):
        if all(self.win_status != None):
            return True

        for i, x in enumerate(self.win_status):
            if x == None:
                if any(self.board[i] == "."):
                    return False

        return True

    def make_move(self, outer_tile, inner_tile):

        if (
            self.board[Game.map_tile[outer_tile]][Game.map_tile[inner_tile]] != "."
            or self.win_status[Game.map_tile[outer_tile]] is not None
        ):
            return None

        self.board[Game.map_tile[outer_tile]][Game.map_tile[inner_tile]] = self.tick()

        # Determine next playable outer tile(s)
        if self.win_status[Game.map_tile[inner_tile]] is None:
            self.next_tile = [inner_tile]
        else:
            self.next_tile = [
                tile
                for tile in Game.map_tile.keys()
                if self.win_status[Game.map_tile[tile]] is None
            ]

        return self.next_tile

    def tick(self):
        return "X" if self.player_turn == 0 else "O"
