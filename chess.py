#!/usr/bin/python
from copy import deepcopy
class ChessGame:
    def __init__(self):
        self.is_white_turn = True
        self.is_white_victory = False
        self.is_black_victory = False
        #init the game boards
	self.gameboard = self.initboard()

    def initboard():
	boardrow = [line for line in range(8)]
	boardgrid = [deepcopy(piecearray) for line in range(8)]
	#consider dict instead of list?	
	for line in range(8):
            for newline in range(8):
                newdict.update({(line,newline): 'Blank'})
    #init the arrays for captured pieces?
class ChessPiece(object):
    def __init__(self, color='Blank', piecechar='.'):
        self.color = color
        self.piecechar = piecechar
   
    def validmove(self, chessboard, curr_location, dest_location):
        pass	 
   
    def makemove(self, chessboard, curr_location, dest_location):
        pass 	
		
class Rook(ChessPiece):
    
    def __init__(self, color):
        mypiecestr = 'R'
        if color == 'White':
            mypiecestr = 'r'
        super(Rook,self).__init__(color, mypiecestr) 
   
    def validmove(self, chessboard, curr_location, dest_location):
        pass	 
   
    def makemove(self, chessboard, curr_location, dest_location):
        pass 	
		
		
       
