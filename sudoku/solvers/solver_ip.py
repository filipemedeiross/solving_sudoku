# To access the modeling documentation see tests/sudoku_IP.ipynb


from mip import *
from ..utils import N, STEP


# Auxiliary functions
def preprocess_grid(grid):
    return [(ij // N, ij % N, k) for ij, k in enumerate(grid.flatten())]


def create_model(C):  # set C represents the clues given by the game
    model = Model(sense=MINIMIZE, solver_name=CBC)
    x = [[[model.add_var(var_type=BINARY, name="x" + str(i) + str(j) + str(k))
           for k in range(1, N+1)]  # range of names between {1,..., 9} != range of positions between {0,...,8}
          for j in range(N)]
         for i in range(N)]

    # Game clues must be strictly followed
    for i, j, k in C:
        if k:  # 0 represents that it is not filled
            model += x[i][j][k-1] == 1, "CLUE_x" + str(i) + str(j) + str(k)

    # All cells must be filled in necessarily once
    for i in range(N):
        for j in range(N):
            model += xsum(x[i][j][k] for k in range(N)) == 1, "FILL_x" + str(i) + str(j)

    # AllDiff constraints on lines
    for i in range(N):
        for k in range(N):
            model += xsum(x[i][j][k] for j in range(N)) == 1, "ALLDIFF_line" + str(i) + str(k)

    # AllDiff constraints on columns
    for j in range(N):
        for k in range(N):
            model += xsum(x[i][j][k] for i in range(N)) == 1, "ALLDIFF_column" + str(j) + str(k)

    # AllDiff constraints on 3x3 squares
    for m, n in zip([yy//STEP*STEP for yy in range(N)], [xx for xx in range(0, N, STEP)]*STEP):
        for k in range(N):
            model += xsum(x[i][j][k] for i in range(m, m+STEP)
                          for j in range(n, n+STEP)) == 1, "ALLDIFF_square" + str(m//STEP + n//STEP) + str(k)

    return model


# Implementing the solver
def solver_ip(grid):
    goal_grid = grid.copy()  # does not change the grid passed as a parameter

    model = create_model(preprocess_grid(goal_grid))
    model.optimize()

    for v in model.vars:
        if v.x:  # was assigned with 1
            i, j, k = map(int, v.name[1:])  # ignore the character 'x'

            if not goal_grid[i, j]:
                goal_grid[i, j] = k

    return goal_grid
