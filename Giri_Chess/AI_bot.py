"""
This file will handle move decisons made by the computer opponent (bot).
"""

import random

#Piece values
piece_score = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
CHECKMATE = 1000
STALEMATE = 0

#The computer randomly plays a move from the list of valid moves
def findRandomMoves(validMoves):
    move = validMoves[random.randint(0,len(validMoves)-1)]
    piece = ['Q','R','N','B']
    promotion_choice = random.choice(piece)
    
    return move,promotion_choice

def findBestMoves(gs,validMoves):
    #greedy algorithm (move the gives max score)
    turn_multiplier = 1 if gs.whiteToMove else -1
    
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    #move = []
    
    for playerMove in validMoves:
        gs.make_move(playerMove)
        opponentsMoves = gs.all_valid_moves_advanced()
        opponentsMaxScore = -CHECKMATE
        
        if gs.stalemate:
            opponentsMaxScore = STALEMATE
        elif gs.checkmate:
            opponentsMaxScore = -CHECKMATE
        else:
            for opponentsMove in opponentsMoves:
                gs.make_move(opponentsMove)
                gs.all_valid_moves_advanced()
                if gs.checkmate:
                    score = CHECKMATE
                
                elif gs.stalemate:
                    score = STALEMATE
                
                else:
                    score = -turn_multiplier*scoreMaterial(gs.board)
                
                if score > opponentsMaxScore:
                    opponentsMaxScore = score
                    
                gs.undo_move()
                #move.append((playerMove.Get_chessNotation(),score))
        if opponentsMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentsMaxScore
            bestPlayerMove = playerMove
        gs.undo_move()
        choice = 'Q'
    #print(move)
        
    return bestPlayerMove,choice

"""
Score the board based on the material
(We can plug in other scoring methods to getting the board score later)
"""
def scoreMaterial(board):
    score = 0
    
    for row in board:
        for square in row:
            
            if square[0] == 'w':
                score+= piece_score[square[1]]
            
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    
    return score