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
    p.display.set_caption("GiriChess")
    Icon_image = p.image.load(R"Giri_Chess\Pieces\wN.png")
    p.display.set_icon(Icon_image)
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    p.display.update()
    
    gs = ChessEngine.GameState()
    validMoves = gs.all_valid_moves_advanced()
    #valid moves is going to be a very expensive operations so we don't wanna call it every frame
    move_made = False   #flag variable when user makes a move
    animate = False     #Flag variable when to run animation 
    show_end_screen = False #Flag variable when to display end_screen pop up
    show_promotion_screen = False #Flag variable when to display pawn promotion ui
    promotion_move = None
    
    
    print(gs.board)
    Load_Images()   #Only do this once before the while loop
    running = True
    
    #Store squares clicked
    sq_selected = ()     #this will store the current square selected tuple (row,col)
    player_clicks = []   # this will store starting pos, destination pos desired by the user[(3,6),(3,4)]
    end_screen_buttons = [] #this will store the (x,y,height,width) of each button on the end screen
    
    #Game-over
    GameOver = False
    
    #Game Loop
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse events
            #click and drag  (add later)
            if e.type ==p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()    #x,y location of the mouse
                
                if show_promotion_screen:       #Special activation for pawn moves UI only
                    choice = get_promotion_choice_click(location,gs,promotion_move)
                    if choice: # 'Q', 'R', 'B', or 'N'
                        
                        promotion_move.promotion_choice = choice
                        gs.make_move(promotion_move)
                        print(promotion_move.Get_chessNotation())
                        move_made = True
                        animate = True
                        validMoves = gs.all_valid_moves_advanced()
                        
                    #Reset states to resume normal gamplay either way
                    show_promotion_screen = False
                    promotion_move = None
                    validMoves = gs.all_valid_moves_advanced()
                        
                        
                        
                elif not GameOver:                    #Only allow the user to make moves using mouse if game's not over
                    
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sq_selected == (row,col):    # click the same square twice, unselect a sqaure
                        sq_selected = ()
                        player_clicks = []
                    else:                           # store the square clicked
                        sq_selected = (row,col)
                        player_clicks.append(sq_selected)
                    if len(player_clicks)==2:       # after 2nd click
                        move = ChessEngine.Move(player_clicks[0],player_clicks[1],gs.board)
                        
                        
                        #check if the move is valid one
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                
                                #check for pawn promotion move first
                                if validMoves[i].is_pawn_promotion:
                                    show_promotion_screen = True
                                    promotion_move = validMoves[i]
                                else:
                                    gs.make_move(validMoves[i])
                                    print(move.Get_chessNotation())
                                    move_made = True
                                    animate = True
                                sq_selected = ()    #reset user clicks
                                player_clicks = []
                        if not move_made and not show_promotion_screen:
                            player_clicks = [sq_selected]
                
                elif show_end_screen:
                    location = p.mouse.get_pos()
                    
                    if end_screen_buttons[0].collidepoint(location):# if 'X' on the pop up screen is clicked
                        show_end_screen = False                     #Hide everything in the next frame
                        end_screen_buttons = []                     #remove the buttons from the board
                    
                    elif end_screen_buttons[1].collidepoint(location):  #Open engine analysis panel
                        print("Game Review clicked")
                    
                    elif end_screen_buttons[2].collidepoint(location):  #Add the game to the user database later
                        print("Save clicked")
                        
                    elif end_screen_buttons[3].collidepoint(location):  #Reset the board without saving
                        gs,validMoves,sq_selected, player_clicks, move_made,animate ,GameOver,show_end_screen,end_screen_buttons,show_promotion_screen,promotion_move =reset_board()
                    
            
            #Key press events
            if e.type == p.KEYDOWN:
                if e.key== p.K_z:       #Undo when 'z' when z is pressed
                    gs.undo_move()
                    move_made = True
                    animate = False

                if e.key == p.K_r:      #Reset the Board when 'r' is pressed
                    gs,validMoves,sq_selected, player_clicks, move_made,animate ,GameOver,show_end_screen,end_screen_buttons,show_promotion_screen,promotion_move  =reset_board()
                    
                    
        
        if move_made:
            if animate:
                move_animation(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.all_valid_moves_advanced()
            move_made = False
            animate = False
            if len(validMoves) == 0:
                if gs.inCheck:
                    print("CHECKMATE!")
                else:
                    print("STALEMATE!")
            
        draw_Gamestate(screen,gs,validMoves,sq_selected)
        
        #Check if the move is promotion move:
        if show_promotion_screen:
            pawn_promotion_ui(screen,gs,promotion_move)
        
        #Check the first time when game ends, and end screen needs to be shown
        if (gs.checkmate or gs.stalemate) and not GameOver:
            GameOver = True
            show_end_screen = True
            
        # Draw the popup ONLY if show_end_screen is active
        if show_end_screen:
            if gs.checkmate:
                if gs.whiteToMove:
                    end_screen_buttons = end_screen(screen, 'Black won by checkmate')
                else:
                    end_screen_buttons = end_screen(screen, 'White won by checkmate')
            elif gs.stalemate:
                end_screen_buttons = end_screen(screen, 'Game Drawn by stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()


"""
Function that resets the board when called
"""
def reset_board():
    gs = ChessEngine.GameState()
    validMoves = gs.all_valid_moves_advanced()
    sq_selected = ()
    player_clicks = []
    move_made = False
    animate = False
    GameOver = False
    show_end_screen = False
    end_screen_buttons = []
    show_promotion_screen = False
    promotion_move = None
    
    return gs,validMoves,sq_selected, player_clicks, move_made,animate ,GameOver,show_end_screen,end_screen_buttons,show_promotion_screen,promotion_move


"""
Highlight selected piece and squares it can move to
"""
def highlight_Squares(screen,gs,validMoves,sq_selected):
    if sq_selected!=():
        r,c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):   #only current players pieces and moves can be highlighted
            #highlight the selected square
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)    #transparency value 0-> transparent, 255-> opaque
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            
            #move highlights from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if (move.startrow, move.startcol) == sq_selected:
                    screen.blit(s,(move.endcol*SQ_SIZE,move.endrow*SQ_SIZE))
    
    #highlight checks
    s = p.Surface((SQ_SIZE,SQ_SIZE))
    s.set_alpha(150)    #transparency value 0-> transparent, 255-> opaque     
    s.fill(p.Color('red'))
    if gs.inCheck and gs.whiteToMove:
        screen.blit(s,(gs.whiteKingLocation[1]*SQ_SIZE,gs.whiteKingLocation[0]*SQ_SIZE))
    elif gs.inCheck and not gs.whiteToMove:
        screen.blit(s,(gs.blackKingLocation[1]*SQ_SIZE,gs.blackKingLocation[0]*SQ_SIZE))
    
    #Highlight last move played (start square and end square)
    s.fill(p.Color('yellow'))
    if len(gs.moveLog)>0:
        last_move = gs.moveLog[-1]
        screen.blit(s,(last_move.startcol*SQ_SIZE,last_move.startrow*SQ_SIZE))
        screen.blit(s,(last_move.endcol*SQ_SIZE,last_move.endrow*SQ_SIZE))
        
        
                
                    
"""
Responsible for graphics in used and displayed in the game
"""
def draw_Gamestate(screen,gs,validMoves,sq_selected):
    draw_Board(screen)              #To draw the squares on the board
    #add in piece highlighting and move suggestions
    highlight_Squares(screen,gs,validMoves,sq_selected)
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
    global colors
    colors = [[255,255,200],[50,150,50]]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            if (r+c)%2==0:
                p.draw.rect(screen,colors[0],p.Rect(r*SQ_SIZE,c*SQ_SIZE,SQ_SIZE,SQ_SIZE))
            else:
                p.draw.rect(screen,colors[1],p.Rect(r*SQ_SIZE,c*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    
    
    
    return screen

"""
Draw pieces on the board, using the current gamestate.board variable
Also added ranks and files the remain constant on the board throughout the game
"""
def draw_Pieces(screen,board):          
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece!='--': #Not empty square
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    
    #ranks and files
    font = p.font.SysFont(None,25)
    s = "abcdefgh"
    for r in range(DIMENSIONS):
        rank = font.render(str(DIMENSIONS-r),True,[150,150,150])
        screen.blit(rank,[0,r*SQ_SIZE])
    for c in range(DIMENSIONS):
        files = font.render(s[c],True,[150,150,150])
        screen.blit(files,[c*SQ_SIZE+54,WIDTH-18])

"""
Function for animating moves
"""
def move_animation(move,screen,board,clock):
    global colors
    dR = move.endrow - move.startrow
    dC = move.endcol - move.startcol
    
    framesPerCount = 2 #speed to the animation is dependent on this variable
    frameCount = (abs(dR)+abs(dC))*framesPerCount
    
    for frame in range(frameCount+1):
        r,c = (move.startrow + dR*frame/frameCount,move.startcol + dC*frame/frameCount)
        draw_Board(screen)
        draw_Pieces(screen,board)
        
        #erase the piece moved from the ending square
        color = colors[(move.endrow+move.endcol)%2]
        endSquare = p.Rect(move.endcol*SQ_SIZE, move.endrow*SQ_SIZE, SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        
        #draw the captured piece on the rectangle
        if move.piece_moved == "--":
            screen.blit(IMAGES[move.piece_captured],endSquare)
        
        #draw the moving piece
        screen.blit(IMAGES[move.piece_moved],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
        
"""
Function to display the end screen of a game (will be used for the chess AI not required for the engine)
"""

def end_screen(screen,text):
    
    words = text.split()
    line1_text = f"{words[0]} {words[1]}"
    line2_text = f"{words[2]} {words[3]}"
    
    font_won = p.font.SysFont("Helvitca",64,False,False)
    font_endtype = p.font.SysFont("Helvitca",24,False,False)
    #Font for buttons
    font_btn = p.font.SysFont("Helvetica", 20, True, False)
    font_close = p.font.SysFont("Helvetica", 24, True, False)
    
    box_size = 5*SQ_SIZE
    header_height = 1.5*SQ_SIZE
    
    # Surface position on screen
    surface_x = 1.5 * SQ_SIZE
    surface_y = 1.5 * SQ_SIZE
    
    # add p.SRCALPHA to show transparency around the corners
    s = p.Surface((box_size,box_size),p.SRCALPHA)
    p.draw.rect(s, p.Color('black'), (0, 0, box_size, box_size), border_radius=15)
    p.draw.rect(s, [50,50,50], (0, 0, box_size, header_height),
                border_top_left_radius=15,
                border_top_right_radius= 15,
                border_bottom_left_radius=0,
                border_bottom_right_radius=0)
    
    #Add textobject
    text_surface_won = font_won.render(line1_text, True, p.Color('white'))
    text_surface_endtype = font_endtype.render(line2_text, True, [150,150,150])
    text_rect_won = text_surface_won.get_rect()
    text_rect_endtype = text_surface_endtype.get_rect()
    
    # Position the text at the top center of the box
    # Padding pushes the text down slightly from the very edge (e.g., 15 pixels)
    top_padding = 15 
    text_rect_won.midtop = (box_size // 2, top_padding)
    text_rect_endtype.midtop = (box_size//2,(header_height//2)+15)
    
    s.blit(text_surface_won, text_rect_won)
    s.blit(text_surface_endtype, text_rect_endtype)
    
    # --- TOP-RIGHT "X" CLOSE BUTTON ---
    close_padding = 15
    close_size = 25
    close_x = box_size - close_size - close_padding
    close_y = close_padding
    
    # Draw a small rounded box for the X button
    p.draw.rect(s, [70, 70, 70], (close_x, close_y, close_size, close_size), border_radius=5)
    close_surf = font_close.render("X", True, [150,150,150])
    close_rect = close_surf.get_rect(center=(close_x + close_size // 2, close_y + close_size // 2))
    s.blit(close_surf, close_rect)
    
    # --- BUTTONS GENERATION (Bottom Half) ---
    btn1_text="Game Review"
    btn2_text="Save" 
    btn3_text="Rematch"
    
    padding = 15
    btn_height = 40
    
    # 1. Full-width Green Button (Game Review)
    btn1_x = padding
    btn1_y = box_size - (2 * btn_height) - (2 * padding)
    btn1_w = box_size - (2 * padding)
    p.draw.rect(s, p.Color('darkgreen'), (btn1_x, btn1_y, btn1_w, btn_height), border_radius=8)
    
    btn1_surf = font_btn.render(btn1_text, True, p.Color('white'))
    btn1_rect = btn1_surf.get_rect(center=(btn1_x + btn1_w // 2, btn1_y + btn_height // 2))
    s.blit(btn1_surf, btn1_rect)
    
    # 2. Left and Right Half-Width Buttons
    btn23_y = box_size - btn_height - padding
    btn23_w = (box_size - (3 * padding)) // 2 # Calculate width to fit perfectly with gaps
    
    # Left Button
    btn2_x = padding
    p.draw.rect(s, [50,50,50], (btn2_x, btn23_y, btn23_w, btn_height), border_radius=8)
    btn2_surf = font_btn.render(btn2_text, True, [150,150,150])
    btn2_rect = btn2_surf.get_rect(center=(btn2_x + btn23_w // 2, btn23_y + btn_height // 2))
    s.blit(btn2_surf, btn2_rect)
    
    # Right Button
    btn3_x = (2 * padding) + btn23_w
    p.draw.rect(s, [50,50,50], (btn3_x, btn23_y, btn23_w, btn_height), border_radius=8)
    btn3_surf = font_btn.render(btn3_text, True, [150,150,150])
    btn3_rect = btn3_surf.get_rect(center=(btn3_x + btn23_w // 2, btn23_y + btn_height // 2))
    s.blit(btn3_surf, btn3_rect)
    
    
    # Convert button coordinates to global screen dimensions for collision detection
    screen_close = p.Rect(surface_x + close_x, surface_y + close_y, close_size, close_size)
    screen_btn1 = p.Rect(surface_x + btn1_x, surface_y + btn1_y, btn1_w, btn_height)
    screen_btn2 = p.Rect(surface_x + btn2_x, surface_y + btn23_y, btn23_w, btn_height)
    screen_btn3 = p.Rect(surface_x + btn3_x, surface_y + btn23_y, btn23_w, btn_height)
    
    screen.blit(s, (surface_x, surface_y))
    return [screen_close,screen_btn1, screen_btn2, screen_btn3]

"""
 Calculates if the mouse clicked on one of the 4 choice boundaries.
 It returns the choice as one of the following character "Q","N","B","R"
"""
def get_promotion_choice_click(mouse_pos,gs,promotion_move):
    color = 'w' if gs.whiteToMove else 'b'
    options = ['Q', 'R', 'B', 'N']
    
    col = promotion_move.endcol
    
    panel_x = col*SQ_SIZE
    panel_y = 0 if color=='w' else 4*SQ_SIZE
    
    
    for i, opt in enumerate(options):
        global_rect = p.Rect(panel_x, panel_y + (i * SQ_SIZE), SQ_SIZE, SQ_SIZE)
        if global_rect.collidepoint(mouse_pos):
            return opt
    return None


"""
Creates a menu with images of pieces that can be chosen as the promoted piece
"""
def pawn_promotion_ui(screen,gs,promotion_move):
    color = 'w' if gs.whiteToMove else 'b'
    options = ['Q', 'R', 'B', 'N']
    
    #size of the panel
    panel_w = SQ_SIZE
    panel_h = 4*SQ_SIZE
    
    #postion of the panel on board
    col = promotion_move.endcol
    panel_x = col*SQ_SIZE
    panel_y = 0 if color == 'w' else 4*SQ_SIZE
    
    s = p.Surface((panel_w, panel_h), p.SRCALPHA)
    p.draw.rect(s, p.Color('white'), (0, 0, panel_w, panel_h), border_radius=15)
    p.draw.rect(s, [100, 100, 100], (0, 0, panel_w, panel_h), width=3, border_radius=15)
    
    # Draw pieces vertically down the menu panel
    for i, opt in enumerate(options):
        s.blit(IMAGES[f"{color}{opt}"], (0, i * SQ_SIZE))
        
    screen.blit(s, (panel_x, panel_y))

if __name__=="__main__":
    main()