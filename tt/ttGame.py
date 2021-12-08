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
        self._num_chars = len(self._valid_chars)

    def getBoardSize(self):
        return (self._num_chars+1,5,10)
    def _getHalfBoardSize(self):
        return (self._num_chars+1,5,5)

    def getInitBoard(self):
        board = np.zeros(self.getBoardSize())
        board[-1,:,:5] = 1
        board[-1,:,5:] = -1
        return board

    def getActionSize(self):
        return self._num_chars*5*5

    def getValidMoves(self, board, player):
        pBoard = board[:,:,:5]
        for h in range(5):
            for v in range(5):
                pBoard[:self._num_chars,h,v] = 0 if 1 in pBoard[:self._num_chars,h,v] else 1
        return pBoard.flatten()


    def getNextState(self, board, player, action): # player == 1 or -1
        assert player == board[-1,0,0]
        move = [0]*self.getActionSize()
        move[action] = 1
        newBoard = np.copy(board)
        newBoard[:,:,:5] += move.reshape(self._getHalfBoardSize())

        return (newBoard, -player)

    def _maxPrestige(charType):
        #there is currently a unity side hack to fix this to 10 star
        return -1

    def _createPlacementJsonStr(board):
        formatData = []
        setValuesP1 = np.where(board[:self._num_chars,:,:5] == 1)
        setValuesP2 = np.where(board[:self._num_chars,:,5:] == 1)

        setValues = [[*setValuesP1[0],*setValuesP2[0]],[*setValuesP1[1],*setValuesP2[1]],[*setValuesP1[2],*setValuesP2[2]]]
        for h,v,char_i in zip(setValues):
            curCharType = self._valid_chars[char_i]
            formatData.extend([v*5+h, curCharType, 240, _maxPrestige(curCharType)])
        return placementStr % tuple(formatData)

    def _checkServerWin(self, board):
        assert board[-1,0,0] == 1
        placementJsonStr = ttGame._createPlacementJsonStr(board)
        response = requests.get("http://localhost:8007/simulate/", data=placementJsonStr)
        return json.loads(response.text.lower())

    def getGameEnded(self, board, player):
        numPlaced = len(np.where(board[:-1,:,:] == 1)[0])
        assert numPlaced <= 10, numPlaced
        if numPlaced < 10:
            return 0
        isWin = self._checkServerWin(board)
        print(self.stringRepresentation(board))
        return 1 if isWin else -1

    def getCanonicalForm(self, board, player):
        newBoard = np.copy(board)
        if newBoard[-1,0,0] == player:
            return newBoard
        newBoard[:,:,:5], newBoard[:,:,5:] = newBoard[:,:,5:], newBoard[:,:,:5].copy()
        return newBoard

    def getSymmetries(self, board, pi):
        return [(board, pi)]

    def stringRepresentation(self, board):
        ret = []
        ret.append(f"Player {board[-1,0,0]}")
        setValuesP1 = np.where(board[:self._num_chars,:,:5] == 1)
        for h,v,char_i in zip(*setValuesP1):
            ret.append(f"{h+v*5}: {self._valid_chars[char_i]}")

        ret.append(f"Player {board[-1,-1,-1]}")
        setValuesP2 = np.where(board[:self._num_chars,:,5:] == 1)
        for h,v,char_i in zip(*setValuesP2):
            ret.append(f"{h+v*5}: {self._valid_chars[char_i]}")
        return "\n".join(ret)



