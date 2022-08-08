import numpy as np
from .problem_formulation import N, objective_grid
from .generator import generator


class Sudoku:
    def __init__(self):  # creates a new valid sudoku and saves the initially filled positions
        self.grid = generator()
        self.home = [(y_fill, x_fill) for y_fill, x_fill in zip(*np.where(self.grid != 0))]

    def insert_num(self, x, y, number):
        if (y, x) not in self.home and 0 <= y < N and 0 <= x < N and 0 < num <= N:
            self.grid[y, x] = number
            return y, x  # if the operation is successful returns the changed position

        return None

    def clear_elem(self, x, y):
        if (y, x) not in self.home:
            self.grid[y, x] = 0
            return y, x  # if the operation is successful returns the changed position

        return None

    def clear_grid(self):
        for i in range(N):
            for j in range(N):
                self.clear_elem(j, i)

    @property
    def won(self):
        return objective_grid(self.grid)


if __name__ == '__main__':
    sudoku = Sudoku()

    print(sudoku.grid)

    while not sudoku.won:
        y_input = int(input('Insert the line [0-8]:'))
        x_input = int(input('Insert the column [0-8]:'))
        num = input('Insert the number [enter to delete cell]:') or None

        if num:
            num = int(num)
            sudoku.insert_num(x_input, y_input, num)
        else:
            sudoku.clear_elem(x_input, y_input)

        print(sudoku.grid)

        clear = input('Clear the grid [s/n]: ')

        if clear in 'Ss':
            sudoku.clear_grid()

    print('Parabéns! Você ganhou.')
