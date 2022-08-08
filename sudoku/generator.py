import numpy as np
from .problem_formulation import N, objective_grid, flatten_position, available_nums
from .solver_backtracking import solver_backtracking


# Returns a new sudoku game grid
def generator(difficulty=41):
    grid = np.zeros((N, N))

    actions = [None] * 81
    size = 0  # represents the grid fill level and the current position to be inserted
    while not objective_grid(grid):
        # Getting the next available position and fill options
        pos = flatten_position(size)
        nums = available_nums(grid, *pos)

        if not nums:
            size -= 1

            while not actions[size]:
                grid[flatten_position(size)] = 0
                size -= 1

            num = actions[size].pop(np.random.randint(len(actions[size])))
        else:
            num = nums.pop(np.random.randint(len(nums)))
            actions[size] = nums

        grid[flatten_position(size)] = num
        size += 1

    while np.count_nonzero(grid) > difficulty:
        position = flatten_position(np.random.randint(N * N))

        if grid[position]:
            grid_copy = grid.copy()
            grid_copy[position] = 0

            if np.all(solver_backtracking(grid_copy)):  # single solution
                grid[position] = 0

    return grid
