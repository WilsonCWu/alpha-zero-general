from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
import numpy as np

class ttGame(Game):
    _valid_chars = [0,1,2,3,4,5]
    def __init__(self):
        pass
    
    def _getNextPlayIndex(board):
        for j in range(5):
            for i in range(2):
                if board[i][j]==-1:
                    return (i,j)

        return (-1,-1) # nothing found

    def getBoardSize(self):
        return (2,5,2)

    def getInitBoard(self):
        return np.full(self.getBoardSize(), -1)

    def getActionSize(self):
        len(_valid_chars)*25

    def getValidMoves(self, board, player):
        valids = np.zeros(self.getActionSize())
        i, j = ttGame._getNextPlayIndex(board)

        invalid_chars = set()
        invalid_pos = set()
        for char, pos in board[i]:
            if char == -1:
                break
            invalid_chars.add(char)
            invalid_pos.add(pos)
        for char_i in range(len(self._valid_chars)):
            for pos_i in range(25):
                char = self._valid_chars[char_id]
                pos = pos_i+1
                if char in invalid_chars or pos in invalid_pos:
                    continue
                valids[char_i*25+pos_i] = 1
        return valids

    def getNextState(self, board, player, action): # player == 1 or -1
        i, j = ttGame._getNextPlayIndex(board)
        for action_i in range(len(action)): # we do this bc getting index using numpy way is slow
            if action[action_i] != 0:
                break
        pos_i = action_i%25
        char_i = action_i//25
        board_new = np.copy(board)
        board_new[i][j][0] = self._valid_chars[char_i]
        board_new[i][j][1] = pos_i+1
        return (board_new, -player)

    def getGameEnded(self, board, player):
        if board[-1][-1][0] == -1:
            return 0
        isWin = board[0][0][0] > board[1][0][0] #TODO
        return 1 if isWin else -1

    def getCanonicalForm(self, board, player):
        return board

    def getSymmetries(self, board, pi):
        return []

    def stringRepresentation(self, board):
        return str(board)



