import numpy as np
from .utils import N, objective_grid
from .generators import generator


class SudokuLogic:
    def __init__(self):  # creates a new valid sudoku and saves the initially filled positions
        self.__grid = generator()
        self.__clues = self.identify_clues()  # clue positions in (x, y) coordinates
        self.__moves = []

    def __getitem__(self, args):
        if isinstance(args, tuple) and len(args) == 2:
            y, x = args  # coordinates must be passed as for a ndarray

            return self.grid[y, x], self.is_clue(x, y)

        return None

    def update(self):
        self.__init__()

    def identify_clues(self):
        return [(x_clue, y_clue) for y_clue, x_clue in zip(*np.where(self.grid != 0))]

    def insert(self, x, y, number):
        if not self.is_clue(x, y) and 0 <= x < N and 0 <= y < N and 0 < number <= N:
            self.__grid[y, x] = number

            if (x, y) in self.__moves:
                self.__moves.remove((x, y))
            self.__moves.append((x, y))  # recording movement performed

            return x, y  # if the operation is successful returns the changed position

        return None

    def clear(self, x, y):
        if not self.is_clue(x, y):
            self.__grid[y, x] = 0

            if (x, y) in self.__moves:
                self.__moves.remove((x, y))

            return x, y  # if the operation is successful returns the changed position

        return None

    def clear_grid(self):
        for y, x in zip(*np.where(self.grid)):
            self.clear(x, y)

    def unmake(self):
        if self.__moves:
            unmake_move = self.__moves[-1]

            self.clear(*unmake_move)

            return unmake_move

        return None

    def is_clue(self, x, y):
        return (x, y) in self.clues

    @property
    def grid(self):
        return self.__grid

    @property
    def clues(self):
        return self.__clues

    @property
    def grid_clues(self):
        return [self.__getitem__((y, x)) for y in range(N) for x in range(N)]

    @property
    def won(self):
        return objective_grid(self.grid)
