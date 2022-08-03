import numpy as np
from .problem_formulation import N, objective_grid
from .generator import generator


class Sudoku:
    def __init__(self):
        self.grid = generator()
        self.home = [(y, x) for y, x in zip(*np.where(self.grid != 0))]

    def insert_num(self, x, y, num):
        if (y, x) in self.home:
            print('Filled position in the source grid!')
            return
        elif y >= N or y < 0:
            print('y value out of range!')
            return
        elif x >= N or x < 0:
            print('x value out of range!')
            return
        elif num > N or num <= 0:
            print('Value entered out of range!')
            return

        self.grid[y, x] = num

    def clear_elem(self, y, x):
        if (y, x) in self.home:
            print('Filled position in the source grid!')
            return

        self.grid[y, x] = 0

    def clear_grid(self):
        for y in self.grid.shape[0]:
            for x in self.grid.shape[1]:
                if (y, x) not in self.home:
                    self.grid[y, x] = 0

    @property
    def won(self):
        return objective_grid(self.grid)


if __name__ == '__main__':
    sudoku = Sudoku()

    print(sudoku.grid)

    while not sudoku.won:
        y = int(input('Insert the line [0-8]:'))
        x = int(input('Insert the column [0-8]:'))
        num = int(input('Insert the number [enter to delete cell]:'))

        if num:
            sudoku.insert_num(x, y, num)
        else:
            sudoku.clear_elem(x, y)

        print(sudoku.grid)

    print('Parabéns! Você ganhou.')
