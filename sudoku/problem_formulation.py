import numpy as np


# Defining the constants
N = 9  # number of grid rows and columns
STEP = 3  # defines the side of the quadrant


# Functions for checking the satisfaction of constraints
def sudoku_constraint(grid_slice):
    return np.array_equal(np.unique(grid_slice), np.arange(1, N + 1))


def check_rows(grid):
    for row in grid:
        if not sudoku_constraint(row):
            return False

    return True


def check_columns(grid):
    for column in grid.T:
        if not sudoku_constraint(column):
            return False

    return True


def check_quadrants(grid):
    for i in range(0, grid.shape[0], STEP):
        for j in range(0, grid.shape[1], STEP):
            if not sudoku_constraint(grid[i: i+STEP, j: j+STEP]):
                return False

    return True


def objective_grid(grid):
    return check_rows(grid) and check_columns(grid) and check_quadrants(grid)


# Functions for checking available actions for a given grid
def number_constraint(grid, y, x, num):
    yy = y // STEP * 3
    xx = x // STEP * 3

    return num not in np.concatenate((grid[y], grid[:, x], grid[yy: yy+STEP, xx: xx+STEP].flatten()))


def flatten_position(pos):  # returns a tuple with the element's position in the grid
    return pos // N, pos % N


def available_pos(grid):
    return [(y, x) for y, x in zip(*np.where(grid == 0))]


def available_nums(grid, y, x):
    return [num for num in range(1, N + 1) if not grid[y, x] and number_constraint(grid, y, x, num)]


def available_actions(grid):
    return [((y, x), num) for y, x in available_pos(grid) for num in available_nums(grid, y, x)]
