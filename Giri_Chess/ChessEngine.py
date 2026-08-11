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
        
        self.moveFunctions = {'p':self.getPawnMoves,'R':self.getRookMoves,'Q':self.getQueenMoves,
                              'K':self.getKingMoves, 'N':self.getKnightMoves,'B':self.getBishopMoves}
        
        self.whiteToMove = True
        self.moveLog = []
        #For check logic and ease of use we keep a log of kings location
        self.whiteKingLocation = (7,4)     
        self.blackKingLocation =  (0,4)
        
        #Naive check-detection
        '''#Checkmate & Stalemate
        self.checkmate = False
        self.stalemate = False'''
        
        #Advanced check-detection
        self.inCheck =  False
        self.pins = []
        self.checks = []
        
        #En-passent
        self.enpassent_possible = () #Records the squares where enpassent is possible
        
    # Works only for normal moves: (Not castling,En passent, Pawn Promotion)
    def make_move(self,move):
        self.board[move.startrow][move.startcol] = '--' # make the space piece just left empty
        self.board[move.endrow][move.endcol] = move.piece_moved
        self.moveLog.append(move)               # maintain move history (to undo)
        self.whiteToMove = not self.whiteToMove   #swap turns after a move
        
        #update king's location if needed:
        if move.piece_moved == 'wK':
            self.whiteKingLocation = (move.endrow,move.endcol)
        elif move.piece_moved == 'bK':
            self.blackKingLocation = (move.endrow,move.endcol)
        
        #pawn promotion (Only queen promotion)
        if move.is_pawn_promotion:
            self.board[move.endrow][move.endcol] = move.piece_moved[0]+'Q'
        
        #En-passent
        if move.is_enpassent:
            self.board[move.startrow][move.endcol] = '--'  #Capturing the pawn
        
        #update en-passent variable
        if move.piece_moved[1] =='p' and abs(move.startrow - move.endrow)==2:   #check only 2 square advances
            self.enpassent_possible = ((move.startrow+move.endrow)//2,move.startcol)
        else:
            self.enpassent_possible = ()
            
    
    def undo_move(self):
        if len(self.moveLog)!=0: #make sure movLog is not 0
            move = self.moveLog.pop()
            self.board[move.startrow][move.startcol] = move.piece_moved
            self.board[move.endrow][move.endcol] = move.piece_captured
            self.whiteToMove = not self.whiteToMove #switch turns back
            
            #update king's location if needed:
            if move.piece_moved == 'wK':
                self.whiteKingLocation = (move.startrow,move.startcol)
            elif move.piece_moved == 'bK':
                self.blackKingLocation = (move.startrow,move.startcol)
            
            #undo enpassent
            if move.is_enpassent:
                self.board[move.endrow][move.endcol]= '--' #Make the landing square blank
                self.board[move.startrow][move.endcol] = move.piece_captured
                self.enpassent_possible = (move.endrow,move.endcol)
            
            #undo the pawn advance
            if move.piece_moved[1] =='p' and abs(move.startrow - move.endrow)==2:
                self.enpassent_possible = ()
                   
        else:
            return
    
    #Legal Moves (NAIVE)
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
    
    #NAIVE ALGORITHM
    '''def all_valid_moves(self):
        #1) Generate all possible moves
        moves = self.all_possible_moves()
        
        #2) Make the move on the board
        for i in range(len(moves)-1,-1,-1):     #always iterate backwards when we need to remove from the list so as to not disturb indices:
            self.make_move(moves[i])
            #3) Generate all of the opponent's moves
            #4) Moves that attack the king are not valid
            self.whiteToMove = not self.whiteToMove     #make_move function has swapped turns again 
            if self.in_check():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove     #switch back becuz make moves will switch again
            self.undo_move()
        
        if len(moves)== 0:  #check mate or stalemate
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        
            
        return moves
        
    #decide if the current player is in check? 
    def in_check(self):
        if self.whiteToMove:
            return self.square_under_attack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.square_under_attack(self.blackKingLocation[0],self.blackKingLocation[1])
    
    #retrive if r,c square can be attacked or not? 
    def square_under_attack(self,r,c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        opp_moves = self.all_possible_moves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in opp_moves:
            if (move.endrow == r) and (move.endcol == c):   #under attack
                return True
        return False'''
    
    
    
    
    
    #ADVANCED ALGORITHM
    def all_valid_moves_advanced(self):
        moves = []
        self.inCheck,self.pins,self.checks = self.pins_and_checks()
        if self.whiteToMove:
            kingrow = self.whiteKingLocation[0]
            kingcol = self.whiteKingLocation[1]
        else:
            kingrow = self.blackKingLocation[0]
            kingcol = self.blackKingLocation[1]
        
        if self.inCheck:
            if len(self.checks)==1:     #check by only 1 piece: options are 1)block or 2)move king
                moves = self.all_possible_moves()
                #to block a check you must move a piece into the kings way
                check = self.checks[0]  #check info
                checkrow = check[0]
                checkcol = check[1]
                pieceChecking = self.board[checkrow][checkcol]
                valid_squares = []      #squares that pieces can move to
                #if knight, must either capture the knight or move
                if pieceChecking[1]=='N':
                    valid_squares = [(checkrow,checkcol)]
                else:
                    for i in range(1,8):
                        valid_square = (kingrow+check[2]*i,kingcol+check[3]*i) #check[2] and check[3] are the directions
                        valid_squares.append(valid_square)
                        if valid_square[0]== checkrow and valid_square[1]==checkcol: #once you get to the piece end checks
                            break
                
                #get rid of the moves that don't block checks
                for i in range(len(moves)-1,-1,-1): #while removing iterating backwards makes sense
                    if moves[i].piece_moved[1] !='K':  #move doesn't move king so it must block or capture
                        if not (moves[i].endrow,moves[i].endcol) in valid_squares:  #move doesn't block or capture
                            moves.remove(moves[i])
            else: #double check king has to move
                self.getKingMoves(kingrow,kingcol,moves)
        else:   # not in check so all moves are fine
            moves = self.all_possible_moves()
        
        return moves
            
                            
    # returns if the current player is in check and list of any pinned pieces and list of checks
    def pins_and_checks(self):
        pins = []       #square where allied pinned piece is and the direction it is pinned from
        checks = []     #squares where enemy is applying check
        inCheck = False
        
        #define enemy color and ally color and king location
        if self.whiteToMove:
            enemy_color = 'b'
            ally_color = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        
        #From kings location in all directions check for pins and checks
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePins = ()   #Reset possible pins
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                
                if 0<= endRow <8 and 0<= endCol <8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0]==ally_color and endPiece[1]!='K': #Could be a pin
                        
                        if possiblePins==():    #first allied piece could be pinned
                            possiblePins = (endRow,endCol,d[0],d[1])
                        else:                   #second allied piece means not pinned
                            break
                    
                    elif endPiece[0]== enemy_color:
                        type = endPiece[1]
                        #There are 5 possibilites now
                        #1.Orthogonally away from the king,  and Piece is Rook
                        #2.Diagonally away from the king, and Piece is Bishop
                        #3.1 square diagonally away from the king, and Piece is Pawn
                        #4.Any direction and piece is Queen
                        #5.Any direction but only 1 square away and the piece is King ( to avoid moving next opponent king)
                        
                        #Note: Knight moves will be handled seperately becuz the direction are different
                        
                        if (0<=j<=3 and type == 'R') or \
                            (4<=j<=7 and type == 'B') or \
                            ((i==1 and type == 'p') and ((enemy_color=='w' and 6<=j<=7) or (enemy_color=='b' and 4<=j<=5))) or \
                            (type == 'Q') or (i==1 and type=='K'):
                                if possiblePins==():    #No piece to block check
                                    inCheck = True
                                    checks.append((endRow,endCol,d[0],d[1]))
                                    break
                                else:                   #Some piece is blocking the check thus a pin
                                    pins.append(possiblePins)
                                    break
                        else:                           # Enemy piece is not checking you
                            break
                else:                                   # Off board
                    break   
                            
        #KNIGHT MOVES
        knight_moves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for m in knight_moves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0<= endRow <8 and 0<= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0]==enemy_color and endPiece[1]=='N': # Enemy knight attacks the king
                    inCheck = True
                    checks.append((endRow,endCol,m[0],m[1]))

        return inCheck,pins,checks
                              
                                    
    
    
    #All moves without considering chess, generate all possible moves
    def all_possible_moves(self):
        moves = []
        #nested loop for each square check
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                #make sure if the piece we look at is the same as the player who's turn it is
                if (turn =='w' and self.whiteToMove==True) or (turn=='b' and self.whiteToMove==False):
                    #identify the type of piece
                    piece = self.board[r][c][1]
                    #generate moves according to the piece type and positions using helper functions
                    self.moveFunctions[piece](r,c,moves)        #calls the apt move function
        return moves
    
    
    
    '''
    
    PIECE MOVES
    
    '''
    #Get all the pawn moves for the pawn located at row,col and add these into the move list                    
    def getPawnMoves(self,r,c,moves):
        #Handle Pins
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]== r and self.pins[i][1]==c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        
        
        if self.whiteToMove:        #white pawn moves
            
            if self.board[r-1][c]=="--":    # 1 square move
                if not piecePinned or pinDirection ==(-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r==6 and self.board[r-2][c]=="--":
                        moves.append(Move((r,c),(r-2,c),self.board))
            
            if c-1>=0:
                if self.board[r-1][c-1][0]=='b':    #capturable piece on left
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                
                # En passent
                elif (r-1,c-1)==self.enpassent_possible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,enpassent_move=True))
            
            if c+1<=7:
                if self.board[r-1][c+1][0]=='b':    #capturable piece on right
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                
                # En passent
                elif (r-1,c+1)==self.enpassent_possible:
                    moves.append(Move((r,c),(r-1,c+1),self.board,enpassent_move=True))    
                    
        
        else:                           #Black pawn moves
            if self.board[r+1][c]=="--":
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r,c),(r+1,c),self.board))
            
                    if (r==1) and  self.board[r+2][c]=="--":
                        moves.append(Move((r,c),(r+2,c),self.board))
       
            if (c+1<=7):
                if self.board[r+1][c+1][0]=='w':
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r,c),(r+1,c+1),self.board))
                
                # En passent
                elif (r+1,c+1)==self.enpassent_possible:
                    moves.append(Move((r,c),(r+1,c+1),self.board,enpassent_move=True))
                
            if (c-1>=0):
                if self.board[r+1][c-1][0]=='w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                
                # En passent
                elif (r+1,c-1)==self.enpassent_possible:
                    moves.append(Move((r,c),(r+1,c-1),self.board,enpassent_move=True))
                    
                 
    #Get all the Rook moves for the Rook located at row,col and add these into the move list                    
    def getRookMoves(self,r,c,moves):
        #Handle Pins
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]== r and self.pins[i][1]==c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1]!='Q':    #Can't remove queen from pin on rook moves
                    self.pins.remove(self.pins[i])
                break
        
        direction = ((-1,0),(1,0),(0,1),(0,-1))
        enemy_color = 'b' if self.whiteToMove else 'w'
        
        for d in direction:
            for i in range(1,8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                
                if 0<= endRow<8 and 0<=endCol<8:  #move should be on board
                    if not piecePinned or pinDirection==d or pinDirection==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0]==enemy_color:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:   #Friendly piece
                            break
                else:       #off board
                    break
                    
    
    #Get all the Bishop moves for the Bishop located at row,col and add these into the move list                    
    def getBishopMoves(self,r,c,moves):
        #Handle Pins
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]== r and self.pins[i][1]==c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        direction = ((1,1),(1,-1),(-1,1),(-1,-1))
        enemy_color = 'b' if self.whiteToMove else 'w'
        
        for d in direction:
            for i in range(1,8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                
                if 0<= endRow<8 and 0<=endCol<8:  #move should be on board
                    if not piecePinned or pinDirection==d or pinDirection==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0]==enemy_color:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:   #Friendly piece
                            break
                else:       #off board
                    break
        
         
    
    #Get all the Knight moves for the Knight located at row,col and add these into the move list                    
    def getKnightMoves(self,r,c,moves):
        #Handle Pins (Pin directions don't matter as knight can't capture the piece that is pinning it)
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]== r and self.pins[i][1]==c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
            
        direction = ((1,2),(-1,2),(-1,-2),(1,-2),(2,-1),(2,1),(-2,1),(-2,-1))
        enemy_color = 'b' if self.whiteToMove else 'w'
        
        for d in direction:
            endRow = r+d[0]
            endCol = c+d[1]
            
            if 0<= endRow<8 and 0<=endCol<8:  #move should be on board
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemy_color:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
            
              
    #Get all the King moves for the King located at row,col and add these into the move list                    
    def getKingMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        ally_color = 'w' if self.whiteToMove else 'b'
        
        for d in directions:
            endRow = r+d[0]
            endCol = c+d[1]
            
            if 0<= endRow<8 and 0<=endCol<8:  #move should be on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally_color :
                    if ally_color=='w':
                        self.whiteKingLocation = (endRow,endCol)
        
                    else:
                        self.blackKingLocation = (endRow,endCol)
                    
                    inCheck,pins,checks = self.pins_and_checks()
                    if not inCheck:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    
                    #place king back on original location
                    if ally_color =='w':
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r,c)
                    

    
    #Get all the Queen moves for the Queen located at row,col and add these into the move list                    
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)



class Move:
    
    #dictonaries for notation conversion
    rankstorows = {'1':7,'2':6,'3':5,'4':4,'5':3,'6':2,'7':1,'8':0}
    rowstoranks = {7:'1',6:'2',5:'3',4:'4',3:'5',2:'6',1:'7',0:'8'}
    
    filestocols = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    colstofiles = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
    
    
    def __init__(self,startsq,endsq,board,enpassent_move = False):
        self.startrow = startsq[0]
        self.startcol = startsq[1]
        self.endrow = endsq [0]
        self.endcol = endsq[1]
        self.piece_moved = board[self.startrow][self.startcol]
        self.piece_captured = board[self.endrow][self.endcol]      #this may even capture empty sqaures in which case nothing is captured
        
        
        #Pawn promotion
        self.is_pawn_promotion = False
        if (self.piece_moved == 'wp' and self.endrow==0) or (self.piece_moved=='bp' and self.endrow==7):
            self.is_pawn_promotion = True
        self.promotion_choice = 'Q'
        
        #En-passent
        self.is_enpassent = enpassent_move
        if self.is_enpassent:
            self.piece_captured = 'wp' if self.piece_moved =='bp' else 'bp'
        
        
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
            #print(self.moveID,other.moveID)
            return self.moveID==other.moveID
        return False
    
    
    #Allows us to get the real chess notations
    def Get_chessNotation(self):
        return self.convertRankFile(self.startrow,self.startcol)+self.convertRankFile(self.endrow,self.endcol)
    
    def convertRankFile(self,r,c):
        return self.colstofiles[c]+self.rowstoranks[r]


#git switch main
#git stash pop