from game import Game

class bot:
    def __init__(self):
        self.team_name = "Human"
                 
    def move(self, board, forced_move):
        i = forced_move[0]

        if len(forced_move) > 1:
            i = input("Enter Big Coordinate in %s: " % forced_move)
        else:
            print("Forced Big Coordiante: %s" % i)

        j = input("Enter Small Coordiante (e.g. SE): ")

        return [i.upper(), j.upper()]
