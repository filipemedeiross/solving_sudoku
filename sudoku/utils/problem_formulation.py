# For better documentation see tests/sudoku_generator.ipynb


import numpy as np


N = 9  # number of grid rows and columns
STEP = 3  # defines the side of the quadrant


def flatten_position(flat_pos, inverted=False):
    if inverted:  # facilitates ndarray manipulation
        return flat_pos // N, flat_pos % N  # return (y, x)
    else:
        return flat_pos % N, flat_pos // N  # return (x, y)


def square_loc(pos):  # pos corresponds to x or y
    pos_square = pos // STEP * STEP

    return pos_square, pos_square + STEP


def satisfies_constraints(grid_slice):  # the slice is flattened before sorting
    return np.array_equal(np.sort(grid_slice, axis=None), np.arange(1, N + 1))


def check_rows(grid):
    for row in grid:
        if not satisfies_constraints(row):
            return False

    return True


def check_columns(grid):
    for column in grid.T:
        if not satisfies_constraints(column):
            return False

    return True


def check_quadrants(grid):
    for x in range(0, N, STEP):
        for y in range(0, N, STEP):
            if not satisfies_constraints(grid[y: y + STEP, x: x + STEP]):
                return False

    return True


def objective_grid(grid):
    return check_rows(grid) and check_columns(grid) and check_quadrants(grid)


def number_constraint(grid, x, y, num):
    return num not in np.concatenate((grid[y],
                                      grid[:, x],
                                      grid[slice(*square_loc(y)), slice(*square_loc(x))].flatten()))


def available_pos(grid):
    return [(x, y) for y, x in zip(*np.where(grid == 0))]


def available_nums(grid, x, y):
    return [num for num in range(1, N + 1) if number_constraint(grid, x, y, num)]
