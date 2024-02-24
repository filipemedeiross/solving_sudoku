import numpy as np
from ..solvers import solver_exhaustive
from ..utils import N, STEP, flatten_position, \
                    available_nums, objective_grid


def generator(clues=41):
    grid = np.zeros((N, N), dtype='int8')
    acts = [0 for _ in range(N**2)]

    s = 0
    while not objective_grid(grid):
        x, y = flatten_position(s)
        nums = available_nums(grid, x, y)

        if nums:
            rmve = np.random.randint(len(nums))
            num  = nums.pop(rmve)

            acts[s] = nums
        else:
            s -= 1

            while not acts[s]:
                x, y = flatten_position(s)
                grid[y, x] = 0
                s -= 1

            x, y = flatten_position(s)
            rmve = np.random.randint(len(acts[s]))
            num  = acts[s].pop(rmve)

        grid[y, x] = num
        s += 1

    positions = [(y, x)
                 for y in range(N)
                 for x in range(N)]

    while np.count_nonzero(grid) > clues:
        idx = np.random.randint(len(positions))
        pos = positions.pop(idx)        

        v = grid[pos]

        grid[pos] = 0
        if not np.all(solver_exhaustive(grid)):
            positions.append(pos)
            grid[pos] = v

    return grid
