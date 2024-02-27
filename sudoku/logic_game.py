import numpy as np
from .generators import generator
from .utils import N, objective_grid


class SudokuLogic:
    # Creates a new valid sudoku and saves the initially filled positions
    def __init__(self):
        self.__grid  = generator()
        self.__clues = self.identify_clues()
        self.__moves = []

    def __getitem__(self, args):
        if isinstance(args, tuple) and len(args) == 2:
            y, x = args

            return self.grid_clue(x, y)

    def update(self):
        self.__init__()

    def identify_clues(self):
        return [(x, y)
                for y, x in zip(*np.where(self.grid))]

    def insert(self, x, y, number):
        if self.is_valid_attr(x, y, number):
            self.__grid[y, x] = number

            if self.is_move(x, y):
                self.__moves.remove((x, y))
            self.__moves.append((x, y))

            return x, y

    def unmake(self):
        if self.__moves:
            return self.clear(*self.__moves.pop())

    def clear(self, x, y):
        if not self.is_clue(x, y):
            self.__grid[y, x] = 0

            if self.is_move(x, y):
                self.__moves.remove((x, y))

            return x, y

    def clear_grid(self):
        pos = np.where(self.grid)

        for y, x in zip(*pos):
            self.clear(x, y)

    def is_clue(self, x, y):
        return (x, y) in self.clues

    def is_valid_attr(self, x, y, n):
        return not self.is_clue(x, y) and \
               0 <= x <= N-1 and \
               0 <= y <= N-1 and \
               1 <= n <= N

    def is_move(self, x, y):
        return (x, y) in self.moves
    
    def grid_clue(self, x, y):
        return self.grid[y, x], self.is_clue(x, y)

    @property
    def grid(self):
        return self.__grid

    @property
    def clues(self):
        return self.__clues

    @property
    def grid_clues(self):
        return [self.grid_clue(x, y)
                for y in range(N)
                for x in range(N)]

    @property
    def moves(self):
        return self.__moves

    @property
    def won(self):
        return objective_grid(self.grid)
