from itertools import product
from mip import Model, MINIMIZE, CBC, BINARY, xsum
from ..utils import N, STEP, process_grid


def create_model(grid):
    model = Model(sense=MINIMIZE, solver_name=CBC)

    V = set(range(N))
    S = set(range(0, N, STEP))

    x = [[[model.add_var(var_type=BINARY, name=f'x_{i}{j}{k}')
           for k in range(1, N+1)]
           for j in range(N)]
           for i in range(N)]

    # Game clues must be strictly followed
    for i, j, k in grid:
        if k:
            model += x[i][j][k-1] == 1, f'CLUE_x_{i}{j}{k}'

    # All cells must be filled in necessarily once
    for i, j in product(V, V):
        model += xsum(x[i][j][k] for k in range(N)) == 1, f'FILL_x_{i}{j}'

    # AllDiff constraints on rows
    for i, k in product(V, V):
        model += xsum(x[i][j][k] for j in range(N)) == 1, f'ALLDIFF_row_{i}{k}'

    # AllDiff constraints on cols
    for j, k in product(V, V):
        model += xsum(x[i][j][k] for i in range(N)) == 1, f'ALLDIFF_col_{j}{k}'

    # AllDiff constraints on squares
    for m, n, k in product(S, S, V):
        model += xsum(x[i][j][k]
                      for i in range(m, m+STEP)
                      for j in range(n, n+STEP)) == 1, f'ALLDIFF_square_{m}{n}{k}'

    return model, x, V

def solver_ip(sudoku_grid):
    grid  = sudoku_grid.copy()
    entry = process_grid(grid)

    model, var, V = create_model(entry)
    model.verbose = 0
    model.optimize()

    for i, j, k in product(V, V, V):
        if var[i][j][k].x and not grid[i, j]:
            grid[i, j] = k + 1

    return grid
