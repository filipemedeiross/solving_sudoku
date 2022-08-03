import numpy as np
from .problem_formulation import N, objective_grid, flatten_position, available_nums


# Returns a new sudoku game grid:
# 41 of the elements filled
# possibility that there is no single solution
def generator():
    grid = np.zeros((N, N))

    moves = [None] * 81
    size = 0
    while True:
        if objective_grid(grid):
            while np.count_nonzero(grid) > 41:
                pos = flatten_position(np.random.randint(81))
                grid[pos] = 0

            return grid

        # Getting the next available position and fill options
        pos = flatten_position(size)
        nums = available_nums(grid, *pos)

        if nums:
            num = nums.pop(np.random.randint(len(nums)))

            grid[pos] = num
            moves[size] = nums
            size += 1

            continue

        size -= 1
        while not moves[size]:
            pos = flatten_position(size)

            grid[pos] = 0
            size -= 1

        pos = flatten_position(size)
        num = moves[size].pop(np.random.randint(len(moves[size])))

        grid[pos] = num
        size += 1
