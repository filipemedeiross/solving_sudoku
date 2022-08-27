<h1>SOLVING SUDOKU BY SEARCH FOR CSP</h1>

## Implementing the Sudoku

The sudoku was implemented using the numpy library for the game logic and the pygame library for the interface. The sudoku grid is generated in an automated way through the search strategy with backtracking that initially fills it completely and later clears the positions checking through a solver, which also uses regular search with backtracking, if the sudoku remains with a unique solution (by default 41 clues are displayed and the class with the initial grid does not contain the game instance response).

The game has three screens explained below:

![Home Screen](https://github.com/filipemedeiross/solving_sudoku_by_search_for_csp/blob/main/examples/home_screen.jpeg?raw=true)

The home screen displays the sudoku initial grid and the **Play** button that launches the game when clicked. It also has an **i** button that takes you to the creator's github profile.

![Game Screen](https://github.com/filipemedeiross/solving_sudoku_by_search_for_csp/blob/main/examples/game_screen.jpeg?raw=true)

When starting the game, it displays the time count while allowing the user to complete the sudoku. The buttons above, from left to right respectively, allow the user to return to the home screen, load a new game, restart the current game, undo moves in the most recent order, and mark moves as right or wrong.

![Winner Screen](https://github.com/filipemedeiross/solving_sudoku_by_search_for_csp/blob/main/examples/winner_screen.jpeg?raw=true)

When you win the game, time is paused and interaction with the sudoku grid and related functions is disabled. The function to return to the home screen and load a new game remains active.

## Modeling Sudoku with Integer Programming

Entry:

$$
I=\set{0, 1, \ldots, 8}
$$

$$
J=\set{0, 1, \ldots, 8}
$$

$$
K=\set{1, 2, \ldots, 9}
$$

$$
C= \set{(i, j, k), \ldots },   i \in I, j \in J, k \in K
$$

Decision Variables: represents whether row i column j is filled with the value k.

$$
x_{ijk},   i \in I, j \in J, k \in K
$$

Objective Function:

$$
Min \space {Z=0}
$$

Subject to:

$$
\sum\limits_{k=1}^{9}x_{ijk}=1,   \forall i \in I, \forall j \in J
$$

$$
x_{ijk} = 1,   \forall (i, j, k) \in C, k>0
$$

$$
\sum\limits_{j=0}^{8}x_{ijk}=1,   \forall i \in I, \forall k \in K
$$

$$
\sum\limits_{i=0}^{8}x_{ijk}=1,   \forall j \in J, \forall k \in K
$$

$$
\sum\limits_{i=m}^{m+2}\sum\limits_{j=n}^{n+2}x_{ijk}=1,   m \in \set{0, 3, 6}, n \in \set{0, 3, 6}, \forall k \in K
$$

$$
x_{ijk} \in \set{0, 1}, \forall i \in I, \forall j \in J, \forall k \in K
$$

## Solvers Benchmark

The solvers benchmark can be seen from `tests/solvers_benchmarks.ipynb` and tested regular backtracking, search for constraint satisfaction problems, and integer linear programming. It was observed that the regular search method with backtracking is very efficient for easier sudoku instances, however it becomes unfeasible to solve more complex instances because the execution time increases considerably.

Besides solving sudoku through integer linear programming has shown to be a good option, the search method for constraint satisfaction problems proves to be the most suitable. In this search strategy, the resolution time remains below two tenths of a second for the most difficult instance in the game.

## Resolution Strategy Implemented in the Game

The game interface has the option to mark the fillings performed as right or wrong. The solution is loaded with each new instance of the game through a different solver than the one used in the sudoku generator, which performs a pre-processing that uses the propagation of inferences through a simple node consistency and the AC-3 algorithm and the search with backtracking to csp (contained in the `solver_backtracking_for_csp.py` submodule of the `solvers` subpackage).

The AllDifferent constraints are transformed into binary constraints to allow the application of the AC-3 algorithm, which in most cases is sufficient to reduce the domains of the variables to 1 and find the solution, in which case the backtracking search for csp only assigns the NxN variables once (with N=9).

When finding the solution, it is stored in a distinct attribute of the game grid.

## Sudoku Pack Organization
```
sudoku/                                      Top-level package
      __init__.py
      constants.py
      logic_game.py
      sudoku.py                              It brings together the functionalities of the modules to implement the sudoku
      media/                                 Folder with the .png files used in the game's interface
              ...
      generators/                            Can be extended with different sudoku generators
              __init__.py
              generator.py                   Implements de sudoku generator
      solvers/                               Collect sudoku solvers        
              __init__.py
              solver_backtracking.py         Solver using regular search strategy with backtracking
              solver_backtracking_for_csp.py Solver using backtracking search strategy for csp
              solver_ip.py                   Solver using integer programming
      utils/                                 Too many features that do not fit in the above subpackages
              __init__.py
              problem_formulation.py         Auxiliary functions to implement game logic
              heuristics.py                  Implementing the functions that apply the heuristics
              csp_formulation.py             Implementing sudoku formulation as a csp
              utils.py                       Too many features that do not fit in the above submodules
```
## Running the Game

Using some Linux distro and make sure you have [Python 3](https://www.python.org/) installed.

Clone the project:

```bash
  git clone https://github.com/filipemedeiross/solving_sudoku_by_search_for_csp.git
```

Access the project directory:

```bash
  cd solving_sudoku_by_search_for_csp
```

Creating a virtual environment (for the example we use the location directory parameter as `.venv`):

```bash
  python3 -m venv .venv
```

Activating the virtual environment:

```bash
  source .venv/bin/activate
```

Install all required packages specified in requirements.txt:

```bash
  pip install -r requirements.txt
```

Use the following command to run the game:

```bash
  python3 main.py
```
## References

Norvig, Peter. Inteligência Artificial. Grupo GEN, 2013.

Images used: <https://opengameart.org/>

Numpy: <https://numpy.org/doc/stable/>

Pygame: <https://www.pygame.org/docs/>
