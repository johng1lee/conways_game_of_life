"""
The playing field for Conway's game of life consists of a two dimensional grid of cells.
Each cell is identified as either alive or dead. For this exercise, let's assume the playing field is an 8x6 grid of cells (i.e. 8 columns, 6 rows).
The challenge is to calculate the next state of the playing field given any initial grid state. To find the next state, follow these rules:
1. Any live cell with fewer than two live neighbors dies, as if caused by under- population.
2. Any live cell with more than three live neighbors dies, as if by overcrowding.
3. Any live cell with two or three live neighbors lives on to the next generation.
4. Any dead cell with exactly three live neighbors becomes a live cell.
5. A cell's neighbors are those cells which are horizontally, vertically or
diagonally adjacent. Most cells will have eight neighbors. Cells placed on the edge of the grid will have fewer.

Design your program to accept an initial 8x6 grid state where each cell is identified as alive or dead.
Your program should output a new state by following Conway's game of life rules.
Your program should display the new state of the playing field.
You may choose the data model for representing your grid and how to display the state of the grid.
Here is a very simple command line output example:
......O.   .O......
OOO...O.   .O...OOO
......O.   .O......
........   ........
...OO...   ...OO...
...OO...   ...OO...
"""
from abc import ABCMeta, abstractmethod
from sys import stdout
import operator
import sys
import time


class Status(object):
    ALIVE = 1
    DEAD = 0

class ConwaysGame(object):

    def __init__(self, iterations=None, display_strat=None, input_strategy=None, delay=0):
        self.iterations = iterations
        self.board = Board(
            display_strat=display_strat,
            input_strategy=input_strategy
        )
        self.delay = delay
        
    def start_game(self):
        self.board.display_board()
        if self.iterations:
            for i in xrange(self.iterations):
                self.board.update_board()
                time.sleep(self.delay)
                self.board.display_board()
        else:
            while True:
                self.board.update_board()
                time.sleep(self.delay)
                self.board.display_board()

class InputStrategy(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_num_cols_and_rows(self):
        pass

    @abstractmethod
    def is_live(self):
        pass

class StringInput(InputStrategy):

    def __init__(self, input_str=None, live_state=None, delimiter=None):
        self.input_str = input_str
        self.delimiter = delimiter
        self.live_state = live_state

    def get_num_cols_and_rows(self):
        self.rows = self.input_str.strip().split(self.delimiter)
        self.nrows = len(self.rows)
        self.ncols = len(self.rows[0]) if self.rows else 0
        return (self.ncols, self.nrows)

    def is_live(self, char):
        return self.live_state == char
    
class Board(object):

    def __init__(self, display_strat=None, input_strategy=None):
        self.board = {}
        self.display_strat = display_strat
        self.input_strategy = input_strategy
        self._initialize_board()

    def _initialize_board(self):
        self.ncols, self.nrows = self.input_strategy.get_num_cols_and_rows()
        live_state = self.input_strategy.live_state
        self.board = {
            (r,c):None
            for r in xrange(self.nrows)
            for c in xrange(self.ncols)
        }
        for r, row in enumerate(self.input_strategy.rows):
            for c, state in enumerate(row):
                cell = Cell(
                    board=self.board,
                    position=(r,c),
                    initial_state=state,
                    live_state=live_state
                )
                cell.generate_adjacent_positions()
                self.board[(r,c)] = cell

    def update_board(self):
        self._update_board_states()

    def _update_board_states(self):
        cells = self.board.values()
        for cell in cells:
            cell.check_neighbors()
        for cell in cells:
            cell.update_status()

    def display_board(self):
        output = ''
        for i in xrange(self.nrows):
            row_output = ''
            for j in xrange(self.ncols):
                row_output += 'O' if self.board[(i,j)].status else '.'
            output += row_output + '\n'
        sys.stdout.write('\n' + output + '\n')
        return output


class Cell(object):
    def __init__(self, board=None, position=None, initial_state=None, live_state=None):
        self.board = board
        self.status = Status.DEAD if not initial_state or initial_state != live_state else Status.ALIVE
        self.previous_status = self.status
        self.neighbors_alive = 0
        self.position = position
        self.adjacent_positions = []

    def __str__(self):
        return str(self.status)

    def generate_adjacent_positions(self):
        for horiz_incr in range(-1,2):
            for vert_incr in range(-1,2):
                adj_coord = tuple(
                    map(
                        operator.add, self.position, (horiz_incr, vert_incr)
                    ))
                if adj_coord in self.board and adj_coord != self.position:
                    self.adjacent_positions.append(adj_coord)

    def check_neighbors(self):
        self.neighbors_alive = 0
        for adjacent_position in self.adjacent_positions:
            self.neighbors_alive += self.board[adjacent_position].status

    def update_status(self):
        if (self.status and self.neighbors_alive == 2) or self.neighbors_alive == 3:
            self.status = Status.ALIVE
        else:
            self.status = Status.DEAD

if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c','--cycles',
        default=None,
        type=int,
        help="Number of iterations to execute. Default is infinite. Press ctrl+c or equivalent keyboard interrupt to stop.")
    parser.add_argument(
        '-f','--inputfile',
        help="Local file to pull initial configuration.")
    parser.add_argument(
        '-s','--inputstr',
        help="User input initial state. Please use '\\n' to separate rows.")
    parser.add_argument(
        '-d','--delay',
        type=float,
        default=0,
        help="Delay between updated states.")
    args = parser.parse_args()
    input_str = ''
    if args.inputfile:
        with open(args.inputfile, 'r') as f:
            input_str = "".join(f.readlines())
    else:
        input_str = args.inputstr
    str_input = StringInput(input_str=input_str, live_state='O')
    try:
        test_game = ConwaysGame(iterations=args.cycles, input_strategy=str_input, delay=args.delay)
        test_game.start_game()
    except KeyboardInterrupt:
        sys.stdout.write("User Interrupt Encountered")
        sys.exit(0)
    except Exception:
        sys.exit(0)



    
