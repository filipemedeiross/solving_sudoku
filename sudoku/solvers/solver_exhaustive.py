import numpy as np
from ..utils import objective_grid, first_available_pos, available_nums


def solver_exhaustive(sudoku_grid):
    grid = sudoku_grid.copy()
    step = np.count_nonzero(grid == 0)

    sol = None
    moves = [None] * step
    actns = [None] * step

    size = 0
    while True:
        if objective_grid(grid):
            # If no one has been found so far:
            #  -> Defines the solution
            # Otherwise, there is more than one solution:
            #  -> Return None
            if not np.all(sol):
                sol = grid.copy()
            else:
                return None

        move = first_available_pos(grid)
        if move:
            nums = available_nums(grid, move[1], move[0])

        if move and nums:
            grid[move] = nums.pop()
            moves[size] = move
            actns[size] = nums
            size += 1
        else:
            size -= 1
            
            while not actns[size]:   
                if size == 0:
                    return sol

                grid[moves[size]] = 0
                size -= 1

            move = moves[size]
            num  = actns[size].pop()

            grid[move] = num
            size += 1
