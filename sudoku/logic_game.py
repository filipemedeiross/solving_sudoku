import numpy as np
from .utils import N, objective_grid, generator


class SudokuLogic:
    def __init__(self):  # creates a new valid sudoku and saves the initially filled positions
        self.__grid = generator()
        self.__clues = self.identify_clues()  # clue positions in (x, y) coordinates

    def update(self):
        self.__grid = generator()
        self.__clues = self.identify_clues()

    def identify_clues(self):
        return [(x_clue, y_clue) for y_clue, x_clue in zip(*np.where(self.grid != 0))]

    def insert(self, x, y, number):
        if not self.is_clue(x, y) and 0 <= x < N and 0 <= y < N and 0 < number <= N:
            self.__grid[y, x] = number
            return x, y  # if the operation is successful returns the changed position

        return None

    def clear(self, x, y):
        if not self.is_clue(x, y):
            self.__grid[y, x] = 0
            return x, y  # if the operation is successful returns the changed position

        return None

    def clear_grid(self):
        for y, x in zip(*np.where(self.grid)):
            self.clear(x, y)

    def is_clue(self, x, y):
        return (x, y) in self.clues

    @property
    def grid(self):
        return self.__grid

    @property
    def clues(self):
        return self.__clues

    @property
    def won(self):
        return objective_grid(self.grid)
