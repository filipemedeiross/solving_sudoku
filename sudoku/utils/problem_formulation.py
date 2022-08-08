import numpy as np


N = 9  # number of grid rows and columns
STEP = N // 3  # defines the side of the quadrant


def satisfies_constraints(grid_slice):
    return np.array_equal(np.unique(grid_slice), np.arange(1, N + 1))


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
    for i in range(0, N, STEP):
        for j in range(0, N, STEP):
            if not satisfies_constraints(grid[j: j + STEP, i: i + STEP]):
                return False

    return True


def objective_grid(grid):
    return check_rows(grid) and check_columns(grid) and check_quadrants(grid)


def number_constraint(grid, y, x, num):
    yy = y // STEP * STEP
    xx = x // STEP * STEP

    return num not in np.concatenate((grid[y], grid[:, x], grid[yy: yy + STEP, xx: xx + STEP].flatten()))


def available_pos(grid):
    return [(y, x) for y, x in zip(*np.where(grid == 0))]


def available_nums(grid, y, x):
    return [num for num in range(1, N + 1) if number_constraint(grid, y, x, num)]


def flatten_position(flat_pos):
    return flat_pos // N, flat_pos % N
