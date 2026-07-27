# Chess-Engine-in-Python

Building a chess engine from scratch in Python using Pygame. The goal of this project is to understand how a chess engine works internally—from board representation and move generation to game rules, search algorithms, and AI.

<p align="center">
  <img src="assets/demo_v1.gif" alt="Chess Engine Demo" width="600">
</p>

---

## Features Completed

###  Project Setup
- Created a dedicated Python package for the chess engine.
- Organized the project into:
  - `ChessMain.py` – Handles the game loop, user input, rendering, and interaction.
  - `ChessEngine.py` – Maintains the game state, board representation, move execution, and move history.
  - `Pieces/` – Stores chess piece sprites used by the GUI.

---

###  Board Representation
- Implemented an 8×8 board using a 2D Python list.
- Represented each piece using two-character strings:
  - First character → Piece color (`w` / `b`)
  - Second character → Piece type (`K`, `Q`, `R`, `B`, `N`, `p`)
- Empty squares are represented as `--`.

Example:

```python
[
    ["bR","bN","bB","bQ","bK","bB","bN","bR"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    ...
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]
```

---

###  Graphical User Interface
- Built the chessboard using the **Pygame** library.
- Implemented alternating light and dark squares.
- Loaded and scaled chess piece sprites dynamically.
- Rendered the complete board every frame.

### ![Board](assets/Board.png)
---

###  User Interaction
- Added mouse-based piece selection.
- Implemented two-click move input:
  1. Select the piece.
  2. Select the destination square.
- Clicking the same square twice deselects the piece.

---

###  Move Execution
- Created a `Move` class to represent every chess move.
- Implemented move execution by updating the board state.
- Added move history to support undo functionality.
- Implemented undo by restoring the previous board state.
- Generated standard coordinate notation (e.g., `e2e4`) for every move.

---

### Legal Move Generation

- Implemented piece-wise move generation for all six chess pieces:
  - Pawn
  - Knight
  - Bishop
  - Rook
  - Queen
  - King
- Generated legal moves based on the current board state and the side to move.
- Used a dispatch-table (`moveFunctions`) to dynamically call the appropriate move generator for each piece.
- Added move validation so only generated legal moves can be executed.
- Optimized move generation by recalculating legal moves only after a move is made or undone.

---

## Current Status

✔ Board rendering complete

✔ Piece rendering complete

✔ Mouse interaction complete

✔ Move execution

✔ Undo functionality

✔ Move notation generation

✔ Legal move generation for all pieces

✔ Move validation framework

🚧 Check detection

🚧 Checkmate / Stalemate

🚧 Castling

🚧 En Passant

🚧 Pawn Promotion

---

## Planned Features

- Check and checkmate detection
- Castling
- En passant
- Pawn promotion
- Undo move functionality
- Move validation
- Minimax search with Alpha-Beta pruning
- Board evaluation function
- AI opponent
- Move ordering and search optimizations
- PGN/FEN support

