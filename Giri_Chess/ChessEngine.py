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
    
    # Works only for normal moves: (Not castling,En passent, Pawn Promotion)
    def make_move(self,move):
        self.board[move.startrow][move.startcol] = '--' # make the space piece just left empty
        self.board[move.endrow][move.endcol] = move.piece_moved
        self.moveLog.append(move)               # maintain move history (to undo)
        self.whiteToMove = not self.whiteToMove   #swap turns after a move
    
    def undo_move(self):
        if len(self.moveLog)!=0: #make sure movLog is not 0
            move = self.moveLog.pop()
            self.board[move.startrow][move.startcol] = move.piece_moved
            self.board[move.endrow][move.endcol] = move.piece_captured
            self.whiteToMove = not self.whiteToMove #switch turns back 
        else:
            return
    
    #Legal Moves
    """
    -get all possible moves
    -for each possible move check if it is a valid move by checking the following
        1) make the move
        2)generate all possible moves by the opposing team
        3)see if any moves attack our king
        4)if the king is safe, it is a valid move and add it to the list
    - return the list of valid moves only
    """
    #All moves considering checks
    
    def all_valid_moves(self):
        return self.all_possible_moves()        # we are worrying about checks rightnow
    #All moves without considering chess, generate all possible moves
    def all_possible_moves(self):
        moves = [Move((6,4),(4,4),self.board)]
        #nested loop for each square check
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                #make sure if the piece we look at is the same as the player who's turn it is
                if (turn =='w' and self.whiteToMove==True) or (turn=='b' and self.whiteToMove==False):
                    #identify the type of piece
                    piece = self.board[r][c][1]
                    #generate moves according to the piece type and positions using helper functions
                    if piece == 'p':
                        self.getPawnMoves(r,c,moves)
                    elif piece == 'N':
                        self.getKnightMoves(r,c,moves)
                    elif piece == 'B':
                        self.getBishopMoves(r,c,moves)
                    elif piece == 'R':
                        self.getRookMoves(r,c,moves)
                    elif piece == 'K':
                        self.getKingMoves(r,c,moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r,c,moves)
                    else:
                        pass
        return moves
                        
    #Get all the pawn moves for the pawn located at row,col and add these into the move list                    
    def getPawnMoves(self,r,c,moves):
        pass   
                 
    #Get all the Rook moves for the Rook located at row,col and add these into the move list                    
    def getRookMoves(self,r,c,moves):
        pass   
    
    #Get all the Knight moves for the Knight located at row,col and add these into the move list                    
    def getKnightMoves(self,r,c,moves):
        pass   
    
    #Get all the Bishop moves for the Bishop located at row,col and add these into the move list                    
    def getBishopMoves(self,r,c,moves):
        pass   
              
    #Get all the King moves for the King located at row,col and add these into the move list                    
    def getKingMoves(self,r,c,moves):
        pass   
    
    #Get all the Queen moves for the Queen located at row,col and add these into the move list                    
    def getQueenMoves(self,r,c,moves):
        pass   
              
                
        

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
        
        #for testing hard coded moves: Unique number with formula given below
        self.moveID = self.startrow*1000+self.startcol*100+self.endrow*10+self.endcol
        
    #Overriding the equals method
    """
    For testing all_valid_moves out
    If we add, any moves in the moves[] list manually they shouldn't seem like a different obj
    so we override '=' operator to call two functions with same attributes as equal
    """
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID==other.moveID
        return False
    
    
    #Allows us to get the real chess notations
    def Get_chessNotation(self):
        return self.convertRankFile(self.startrow,self.startcol)+self.convertRankFile(self.endrow,self.endcol)
    
    def convertRankFile(self,r,c):
        return self.colstofiles[c]+self.rowstoranks[r]