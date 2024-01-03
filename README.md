# Bomb Clearer by NORXONDOR
A CLI Minesweeper clone implemented in Python. Includes all the important functionality of the original Microsoft Minesweeper (1990). 

## How to play
1. First, an action is selected (u - Uncover tile, f - Flag tile).
2. Then, the coordinates of the desired tile are given in form 'x,y' (e.g 10,4).

- To unflag a tile, you can attempt to flag it again.
- The player wins when the amount of remaining tiles is equal to the number of bombs on the board.
- The player loses when a tile with a bomb is cleared.

## Running the program
To run bomb-clearer:
```
cd "path/to/folder"
python bomb_clearer.py
```
## Sample board

![sample_board](https://github.com/NORXONDOR/bomb-clearer/assets/100261200/f732d242-50a4-4b35-a351-af7a4ab23596)

X and Y coordinates are represented along the X-axis (horizontal numbers) and y-axis (vertical numbers).

- '‎ ‎ ' tiles represent uncovered safe tiles with no adjacent bombs.
- '0-8‎ ' tiles represent uncovered safe tiles with adjacent bombs.
- '?‎ ' tiles represent covered tiles.
- 'F‎ ' tiles represent flagged tiles (which can only be covered).
- '*‎ ' tiles represent bombs. Only seen when uncovered.
