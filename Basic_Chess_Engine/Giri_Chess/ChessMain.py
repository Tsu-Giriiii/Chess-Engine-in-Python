''' This is the driver file that handles input-output and GameState information'''

import pygame as p
import ChessEngine

p.init()
HEIGHT = WIDTH = 512 #400 is also good
DIMENSIONS = 8 #dimension of the chess board 8x8
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15
IMAGES = {}

#Load the images
#Initialize a global dictionary of images, it will be loaded only once to save computation

def Load_Images ():
    root = "Giri_Chess/Pieces/"
    piece_list = ["bR","bN","bB","bQ","bK","bB","bN","bR","bp","wR","wN","wB","wQ","wK","wB","wN","wR","wp"]
    for piece in piece_list:
        IMAGES[piece] = p.transform.scale(p.image.load(root+piece+".png"),(SQ_SIZE,SQ_SIZE))

#We can access the image of pieces using dictionary eg: IMAGES["wp"]
#transform and scale the image to take up the whole square on the board

#Main driver code: This will handle the user input and updating the graphics
def main():
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    p.display.update()
    gs = ChessEngine.GameState()
    print(gs.board)
    Load_Images()   #Only do this once before the while loop
    running = True
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_Gamestate(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        
"""
Responsible for graphics in used and displayed in the game
"""
def draw_Gamestate(screen,gs):
    draw_Board(screen)    #To draw the squares on the board
    #add in piece highlighting and move suggestions
    draw_Pieces(screen,gs.board)    #draw the pieces on top of the Board
 

"""
Draw the squares on the board.
"""  
def draw_Board(screen):
    #squares
    '''for i in range(0,(DIMENSIONS+1)*SQ_SIZE,SQ_SIZE*2):
        for j in range(0,(DIMENSIONS+1)*SQ_SIZE,SQ_SIZE*2):
            p.draw.rect(screen,[255,255,200],[i,j,SQ_SIZE,SQ_SIZE])
            p.draw.rect(screen,[50,150,50],[i,j-64,SQ_SIZE,SQ_SIZE])
            p.draw.rect(screen,[50,150,50],[i-64,j,SQ_SIZE,SQ_SIZE])'''
    
    colors = [[255,255,200],[50,150,50]]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            if (r+c)%2==0:
                p.draw.rect(screen,colors[0],p.Rect(r*SQ_SIZE,c*SQ_SIZE,SQ_SIZE,SQ_SIZE))
            else:
                p.draw.rect(screen,colors[1],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    
    #ranks and files (add later)
    
    return screen

"""
Draw pieces on the board, using the current gamestate.board variable
"""
def draw_Pieces(screen,board):          
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece!='--': #Not empty square
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

if __name__=="__main__":
    main()