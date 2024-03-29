# Chess Board

A simple chess board I've build during the summer of 2021 to practice with Python.

Inspired by [Creating a Chess Engine in Python](https://youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_)

<p float="left">
  <img src="https://user-images.githubusercontent.com/69045457/230572687-a8bd1f78-9512-4b14-82d1-fa5a1a9b891b.png" width=40% /> 
  <img src="https://user-images.githubusercontent.com/69045457/230572668-7d99e8c9-475e-4d56-b5ba-63c755366b15.png" width=40% />
</p>

## Features
- Show valid moves (including en passant, castling, checks, and pins)
- Promote pawns to any piece by pressing the corresponding letter
- Print moves to console in standard chess notation (missing `+` and `#` notation for checks)
- End the game at checkmate announcing the winner
- Undo last move by pressing `left arrow`


## How to run

```bash
git clone https://github.com/GBergatto/chess-board.git
cd chess-board
pip install pygame
python main.py
```
