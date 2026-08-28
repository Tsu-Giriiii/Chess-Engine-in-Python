# GiriChess

A chess engine and interactive chess application built from scratch in Python using Pygame. The project focuses on implementing chess rules, legal move generation, game-state management, and efficient check detection, with search and evaluation algorithms planned for a future AI opponent.


<p align="center">
  <img src="assets/demo_v3.gif" alt="Chess Engine Demo" width="600">
</p>

---

## Tech Stack

- **Language:** Python
- **GUI:** Pygame
- **Concepts:** Object-Oriented Programming, Game State Management, Move Generation, Rule Validation, Algorithimic Optimization

---

## Features

### Chess Engine

- Implemented an 8×8 board representation using a 2D Python list.
- Implemented piece-wise move generation for all six chess pieces.
- Implemented legal move validation to prevent moves that leave the king in check.
- Implemented detection and handling of:
  - Pins
  - Single check
  - Double check
  - Checkmate
  - Stalemate
- Implemented special chess rules:
  - Castling
  - En passant
  - Pawn promotion
- Implemented move history and undo functionality.
- Generated coordinate notation for executed moves.

### Check Detection

Implemented two approaches to check detection during development:

**Naive approach**
- Generates opponent moves to determine whether the king is under attack.
- Preserved as a separate reference implementation.

**Optimized approach**
- Directly analyzes attacking pieces, pins, and attack directions.
- Avoids generating the complete opponent move list during check evaluation.
- Used by the main engine for more efficient legal-move generation.


### Graphical User Interface

- Built an interactive chessboard using Pygame.
- Implemented mouse-based piece selection and move execution.
- Added visual highlighting for:
  - Legal moves
  - The most recently played move
  - King in check
- Added animated piece movement.
- Added graphical pawn promotion selection.
- Added game-over screen for checkmate and stalemate.
- Added rematch/reset functionality.
- Added custom application title and icon.

![Board](assets/Board.png)

---

## Current Status

### Completed

✔ Complete board and piece rendering  
✔ Legal move generation for all pieces  
✔ Legal move validation  
✔ Check detection  
✔ Pin and double-check handling  
✔ Checkmate and stalemate detection  
✔ Castling  
✔ En passant  
✔ Pawn promotion  
✔ Move history and undo  
✔ Legal move highlighting  
✔ Check highlighting  
✔ Previous-move highlighting  
✔ Move animations  
✔ Pawn promotion UI  
✔ Game-over screen  
✔ Board reset / rematch functionality  

### In Development

🚧 Board evaluation  
🚧 Minimax search with Alpha-Beta pruning  
🚧 AI opponent  

---

## Planned Features

- Move ordering and search optimizations
- PGN/FEN support
- Game review and analysis
- Persistent game storage
- Standalone offline executable
