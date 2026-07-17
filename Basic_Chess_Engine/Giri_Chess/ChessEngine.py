'''
This file stores all the information about the current state of the Chess game.
Also responsible to determining the valid moves in the current state. It will also keep a move log.
'''

class GameState:
    def __init__(self):
        #Numpy arrays based board will be faster for AI based engine
        #Initial position of the board from white's perspective
        self.board = [                                  
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        #Note: Board is an 8x8, 2-D list
        #Each cell is represented by two characters 1st: Color (b/w), 2nd: Piece type (K,Q,R,B,N,p)
        #Empty square is represented by "--"
        
        self.whitToMove = True
        self.moveLog = []
        
        