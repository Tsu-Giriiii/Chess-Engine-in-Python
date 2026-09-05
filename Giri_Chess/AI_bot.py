"""
This file will handle move decisons made by the computer opponent (bot).
"""

import random

#The computer randomly plays a move from the list of valid moves
def findRandomMoves(validMoves):
    move = validMoves[random.randint(0,len(validMoves)-1)]
    piece = ['Q','R','N','B']
    promotion_choice = random.choice(piece)
    
    return move,promotion_choice

def findBestMoves():
    return