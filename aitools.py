#functions for static evaluation of boards, collection of data, etc.

from tetrisgame import *

class evaluator():
    currentSef = 0

    currentBoard = []
    pieceList = []

    sefs = {
        0 : self.sef0,
        1 : self.sef1
    }

    def evaluate(self, board, pieceList):
        self.currentBoard = board
        self.pieceList = pieceList
        return self.sef[currentSef]

    def projectPieces(self)

    #Board height
    def sef0(self):
        height = 0
        for row in reversed(self.currentBoard):
            if 0 not in row:
                return height
            else
                height += 1
        return height

    
    def sef1(self):
        None