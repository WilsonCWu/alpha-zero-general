import numpy as np

class HumanTTPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        print(game.stringRepresentation(board))
        valid = self.game.getValidMoves(board, 1)
        while True:
            input_move = input()
            input_a = input_move.split(" ")
            if len(input_a) == 2:
                try:
                    pos, charType = [int(i) for i in input_a]
                    v = (pos-1)//5
                    h = (pos-1)%5
                    move = np.zeros((self._num_chars,5,5))
                    move[game._valid_chars.find(charType),h,v] = 1
                    a = move.flatten().find(1)
                    if valid[a]:
                        break
                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            print('Invalid move')
        return a