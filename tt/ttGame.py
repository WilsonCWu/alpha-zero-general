from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
import numpy as np
import requests
import json
placementStr = open("placement.json").read()

class ttGame(Game):
    _valid_chars = [0,4,5,6,7,8,9,10,11,12,13,16,17,18,19,21,22,23,24,26,30,31,32,33,34,35,37,38]
    def __init__(self):
        pass

    def getBoardSize(self):
        return (5,10,len(_valid_chars)) # 5*10*_valid_chars

    def getInitBoard(self):
        return np.zeros(self.getBoardSize())

    def getActionSize(self):
        return 5*5*len(_valid_chars)

    def getValidMoves(self, board, player):
        pass

    def getNextState(self, board, player, action): # player == 1 or -1
        pass

    def _maxPrestige(charType):
        print("todo")

    def _createPlacementJsonStr(board):
        formatData = []

        return placementStr % tuple(formatData)

    def _checkServerWin(self, board):
        placementJsonStr = ttGame._createPlacementJsonStr(board)
        response = requests.get("http://localhost:8007/simulate/", data=placementJsonStr)
        return json.loads(response.text.lower())

    def getGameEnded(self, board, player):
        if board[-1][-1][0] == -1:
            return 0
        isWin = self._checkServerWin(board)
        return 1 if isWin else -1

    def getCanonicalForm(self, board, player):
        pass

    def getSymmetries(self, board, pi):
        return [(board, pi)]

    def stringRepresentation(self, board):
        return str(board)



