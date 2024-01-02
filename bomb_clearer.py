from random import *
from math import *
import os
import time


VERSION = "1.0.0"


class Tile():
    def __init__(self, is_bomb):
        """
        Creates a Board Tile.
        
        Args:
            (bool) is_bomb: Determines if Tile holds a bomb.
        """
        self.is_bomb = is_bomb
        self.covered = True
        self.flagged = False
        self.adj_tiles = []
        self.adj_bombs = 0
        self.coords = ()


class Board():
    def __init__(self, x_dim=10, y_dim=10, bomb_prop=0.1):
        """
        Creates a BombClearer Board.
        
        Args:
            (int) x_dim: Width of the board, dim < 100.
            (int) y_dim: Height of the board, dim < 100.
            (float) bomb_prop: Proportion of tiles that are bombs.
        """
        self.x_axis = x_dim
        self.y_axis = y_dim
        self.gamestate = 0
        self.recursed = False
        
        # Create a randomly ordered array of bomb locations.
        tile_count = self.x_axis*self.y_axis
        self.covered_count = tile_count
        
        self.bomb_count = floor(tile_count*bomb_prop) 
        safe_count = tile_count-self.bomb_count
        
        bomb_array = [True] * self.bomb_count + [False] * safe_count
        shuffle(bomb_array)

        # Initialise each Tile within the board.
        self.tile_matrix = []
        for y in range(self.y_axis):
            self.tile_matrix.append([])
            for x in range(self.x_axis):
                self.tile_matrix[y].append(Tile(is_bomb=bomb_array[y*x_dim+x]))

        # Get coordinates, store all adjacent Tiles and calcualte adjacent bombs for each Tile.
        for y in range(self.y_axis):
            for x in range(self.x_axis):
                target_tile = self.tile_matrix[y][x]

                target_tile.coords = (x, y)

                # Skip Tile if bomb.
                if target_tile.is_bomb:
                    continue

                for row in range(-1, 2):
                    for column in range(-1, 2):
                        # Don't include target_tile.
                        if not (row == 0 and column == 0):
                            # Don't include imaginary tiles.
                            if not (y+row < 0 or y+row > self.y_axis-1 or x+column < 0 or x+column > self.x_axis-1):
                                target_tile.adj_tiles.append(self.tile_matrix[y+row][x+column])
                
                for tile in target_tile.adj_tiles:
                    if tile.is_bomb:
                        target_tile.adj_bombs += 1


    def render(self):
        """
        Visualises all tiles on board.
        
        Covered Tiles:
            P = Flagged Tile.
            # = Non-flagged Tile.
        
        Uncovered Tiles:
            * = Bomb Tiles.
            0-8 = Non-bomb Tiles.
        """
        out_string = "yx"
        for x in range(self.x_axis):
            if x < 10:
                out_string += f'{x} '
            else:
                out_string += f'{x}'
        out_string += '\n'
            
        for y in range(self.y_axis):
            if y < 10:
                out_string += f'{y} '
            else:
                out_string += f'{y}'
            for x in range(self.x_axis):
                if self.tile_matrix[y][x].covered:
                    if self.tile_matrix[y][x].flagged:
                        out_string += 'F '
                    else:
                        out_string += '? '
                else:
                    if self.tile_matrix[y][x].is_bomb:
                        out_string += '* '
                    else:
                        if self.tile_matrix[y][x].adj_bombs == 0:
                            out_string += '  '
                        else:
                            out_string += str(self.tile_matrix[y][x].adj_bombs) + ' '
            out_string += '\n'
        print(out_string)


    def flag(self, x, y):
        """
        Toggles flag state of Tile at self.tile_matrix[y][x].
        
        Args:
            (int) x: Coordinate along horizon.
            (int) y: Coordinate along verticalis.
        """
        target_tile = self.tile_matrix[y][x]
        
        if target_tile.covered:
            if target_tile.flagged:
                target_tile.flagged = False
            else:
                target_tile.flagged = True
        else:
            print("Tile is covered! Tile cannot be flagged.")
            time.sleep(2)


    def uncover(self, x, y):
        """
        Uncovers Tile at self.tile_matrix[y][x].
        
        Args:
            (int) x: Coordinate along horizon.
            (int) y: Coordinate along verticalis.
        """
        target_tile = self.tile_matrix[y][x]
        
        # Allow user to uncover flagged Tiles given confirmation.
        if target_tile.flagged:
            print("Tile is flagged! Are you sure you want to uncover it? (y/n)")
            
            while True:
                choice = input("> ").lower()
                if choice == 'y':
                    break
                elif choice == 'n':
                    return
                else:
                    print("Choice must be 'y' or 'n'.")
        
        if target_tile.covered:
            target_tile.covered = False
            
            self.covered_count -= 1

            # If Tile has 0 adjacent bombs, uncover() recursively until all adjacent safe unflagged Tiles discovered.
            if target_tile.adj_bombs == 0:
                for tile in target_tile.adj_tiles:
                    if not tile.is_bomb and not tile.flagged:
                        x, y = tile.coords
                        self.recursed = True
                        self.uncover(x, y)
                        self.recursed = False
            
            # Loss condition.
            if target_tile.is_bomb:
                
                # Allow all bombs to be displayed.
                for y in range(self.y_axis):
                    for x in range(self.x_axis):
                        target_tile = self.tile_matrix[y][x]
                        
                        if target_tile.is_bomb:
                            target_tile.covered = False
                            
                board.gamestate = -1
            
            # Win condition.
            if board.covered_count == board.bomb_count:
                board.gamestate = 1

        elif not target_tile.covered and not self.recursed:
            print("Tile is already uncovered! Tile cannot be uncovered.")
            self.recursed = False
            time.sleep(2)


    def extract_coords(self, coords_str):
        """
        Converts user input into integers representing Board coordinates.
        
        Args:
            (string) coords_str: A string in form 'x,y' which denotes a location on a Board, e.g '10,4'. Passed in from game loop.
        Returns:
            (int) x: X-coordinate.
            (int) y: Y-coordinate.
        """
        # Ensure coords_str has one ','. 
        comma_idx = 0
        comma_count = 0
        
        for char_idx in range(len(coords_str)):
            if coords_str[char_idx] == ',':
                comma_idx = char_idx
                comma_count += 1
                if comma_count > 1:
                    raise ValueError(f"Coordinates must have only 1 ',' between coordinates, got '{coords_str}' ({comma_count} commas).")

        if comma_count == 0:
            raise ValueError(f"Coordinates string must include 1 ',' between coordinates, got '{coords_str}'.")
        
        before_comma = coords_str[:comma_idx]
        after_comma = coords_str[comma_idx+1:]
        
        # Ensure coords_str only digits and ','.
        if not all(char.isdigit() for char in before_comma + after_comma):
            raise ValueError(f"Coordinates string must only include digits and ',', got '{coords_str}'.")
        
        x = int(before_comma)
        y = int(after_comma)
        
        # Ensure coordinates indexable.
        if x < self.x_axis and y < self.y_axis:
            target_tile = self.tile_matrix[y][x]
        else:
            raise IndexError(f"Coordinates out of bounds. X-index must be < {self.x_axis}, Y-index must be < {self.y_axis}, got {x},{y}")
        
        return x, y


def clear():
    """
    Clears console.
    """
    os.system('cls' if os.name=='nt' else 'clear')


if __name__ == "__main__":
    while True:
        clear()
        print(f"BombClearer v{VERSION} by NORXONDOR\n")
        print("Select difficulty:")
        print("0 : Easy - 9x9 / 10 bombs")
        print("1 : Medium - 16x16 / 40 bombs")
        print("2 : Hard - 30x16 / 99 bombs")
        print("q : Quit game")

        match input("> "):
            case '0':
                board = Board(x_dim=9, y_dim=9, bomb_prop=0.12346)
                break
            
            case '1':
                board = Board(x_dim=16, y_dim=16, bomb_prop=0.15625)
                break
            
            case '2':
                board = Board(x_dim=30, y_dim=16, bomb_prop=0.20625)
                break
            
            case 'q':
                quit()
                
            case _:
                print("Error: Choice invalid.")
                time.sleep(1.5)
                continue
    
    # Gameplay loop.
    while True:
        clear()
        print(f"BombClearer v{VERSION} by NORXONDOR\n")
        board.render()
        print("u : Uncover a tile")
        print("f : Flag a tile")
        print("q : Quit game")
        
        match input("> ").lower():
            case 'f':
                print("Specify coordinates to flag 'x,y', e.g '10,4'.")
                coords_str = input("> ")

                # Sanitise input.
                try:
                    x, y = board.extract_coords(coords_str)
                except (ValueError, IndexError) as e:
                    print("Command failed:", e)
                    time.sleep(3)
                    clear()
                    continue
                
                board.flag(x, y)

            case 'u':            
                print("Specify coordinates to uncover 'x,y', e.g '10,4'.")
                coords_str = input("> ")

                # Sanitise input.
                try:
                    x, y = board.extract_coords(coords_str)
                except (ValueError, IndexError) as e:
                    print("Command failed:", e)
                    time.sleep(3)
                    clear()
                    continue
                
                board.uncover(x, y)

            case 'q':
                quit()

            case _:
                print("Error: Choice invalid.")
                time.sleep(1.5)
                continue

        # Display consequence.
        clear()
        print(f"BombClearer v{VERSION} by NORXONDOR\n")
        board.render()
        
        if board.gamestate == -1:
            # Loss condition met.
            print("  X X")
            print("  -u-\n")
            print(f"Bomb found at ({x},{y}). You lose!")
            break
        elif board.gamestate == 1:
            # Win condition met.
            print("  O O")
            print("   U \n")
            print(f"All bombs located. You win!")
            break