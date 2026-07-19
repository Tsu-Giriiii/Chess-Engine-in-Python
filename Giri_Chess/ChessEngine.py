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
        
        self.whiteToMove = True
        self.moveLog = []
    
    def make_move(self,move):
        self.board[move.startrow][move.startcol] = '--' # make the space piece just left empty
        self.board[move.endrow][move.endcol] = move.piece_moved
        self.moveLog.append(move)               # maintain move history (to undo)
        self.whiteToMove = not self.whiteToMove   #swap turns after a move
        

class Move:
    
    #dictonaries for notation conversion
    rankstorows = {'1':7,'2':6,'3':5,'4':4,'5':3,'6':2,'7':1,'8':0}
    rowstoranks = {7:'1',6:'2',5:'3',4:'4',3:'5',2:'6',1:'7',0:'8'}
    
    filestocols = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    colstofiles = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
    
    
    def __init__(self,startsq,endsq,board):
        self.startrow = startsq[0]
        self.startcol = startsq[1]
        self.endrow = endsq [0]
        self.endcol = endsq[1]
        self.piece_moved = board[self.startrow][self.startcol]
        self.piece_captured = board[self.endrow][self.endcol]      #this may even capture empty sqaures in which case nothing is captured
        
    
    #Allows us to get the real chess notations
    def Get_chessNotation(self):
        return self.convertRankFile(self.startrow,self.startcol)+self.convertRankFile(self.endrow,self.endcol)
    
    def convertRankFile(self,r,c):
        return self.colstofiles[c]+self.rowstoranks[r]