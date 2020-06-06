from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from game import Game
from MCTS_bot import bot
import copy

coordinate_map = {}

for (key, value) in Game.map_tile.items():
    coordinate_map[value] = key

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def main():
    return render_template('tictactoe.html')

class Server:
    def __init__(self):
        self.game = Game()
        self.next_moves = list(self.game.map_tile.keys())
        self.bot = bot()
        
        socketio.on_event('play', self.handlePlay)
        socketio.on_event('ai', self.handleAI)
        socketio.on_event('getBoard', self.handleBoard)
    
    def handleBoard(self):
        emit('getBoard', self.game.board.tolist())

    def handleAI(self):
        while True:
            player_move = self.bot.move(
                copy.deepcopy(self.game.board), copy.copy(self.next_moves)
            )

            if player_move[0] not in self.next_moves:
                continue

            next_moves = self.game.make_move(*player_move)

            if not next_moves == None:
                self.next_moves = next_moves

                outer = self.game.map_tile[player_move[0]]
                inner = self.game.map_tile[player_move[1]]

                play = {'i': outer // 3 * 3 + inner // 3, 'j': (outer % 3) * 3 + inner % 3, 'di': inner // 3, 'dj': inner % 3, 'player': self.game.tick(), 'nextMoves': [self.game.map_tile[x] for x in self.next_moves]}

                self.game.player_turn = 0 if self.game.player_turn == -1 else -1

                socketio.emit('play', play)

                return

    def handlePlay(self, play):
        outer = int(play['i']) // 3 * 3 + int(play['j']) // 3
        inner = (int(play['i']) % 3) * 3 + int(play['j']) % 3

        if coordinate_map[outer] in self.next_moves:
            next_moves = self.game.make_move(coordinate_map[outer], coordinate_map[inner])

            if next_moves != None:
                self.next_moves = next_moves

                play['player'] = self.game.tick()
                play['nextMoves'] = [self.game.map_tile[x] for x in self.next_moves]

                self.game.player_turn = 0 if self.game.player_turn == -1 else -1

                socketio.emit('play', play)

if __name__ == '__main__':
    server = Server()
    socketio.run(app, debug=True)