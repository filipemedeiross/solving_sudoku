<h1>SOLVING SUDOKU USING CSP SEARCH</h1>

## Introduction

This project is the second in a series of projects in which simple games will be developed using the pygame library, and these games will be conquered using machine learning algorithms and artificial intelligence in general.

The motivation behind this approach lies in frequent situations where certain evaluation metrics, when applied to specific algorithms, prove to be inaccurate and obscure their true practical significance. In extreme cases, algorithms with poor performance may be inaccurately assessed positively by specific metrics that, in practice, do not reflect their true effectiveness and distort their evaluation. When developing algorithms to win games, we have two main evaluation metrics that are simple and have empirical significance:

1. Whether the algorithm won or not.
2. If it won, how efficient its performance was.

## Implementing the Sudoku

The sudoku implementation utilizes the numpy library for game logic and the pygame library for the interface. The sudoku grid is dynamically generated through a search strategy with backtracking and randomization. Initially, the grid is fully populated, after which positions are iteratively cleared using a solver (this solver employs an exhaustive search with backtracking, ensuring that the sudoku puzzle maintains a unique solution).

This search strategy employs a trial-and-error approach, akin to brute force. When encountering unresolved configurations with no further valid movement options, the search backtracks until it discovers a valid path, avoiding revisitation of previously explored paths. By default, 41 clues are displayed, and the initial grid class does not contain the game instance response.

The game features three distinct screens:

<p align="center"> 
    <img src="https://github.com/filipemedeiross/solving_sudoku_by_search_for_csp/blob/main/examples/home_screen.png?raw=true" width="250" height="400">
</p>

The home screen showcases the initial sudoku grid and a prominent **Play** button to commence the game. Additionally, it includes an information (**i**) button, directing users to the creator's github profile.

<p align="center"> 
    <img src="https://github.com/filipemedeiross/solving_sudoku_by_search_for_csp/blob/main/examples/game_screen.png?raw=true" width="250" height="400">
</p>

Upon game initiation, the screen displays a timer while enabling users to solve the sudoku puzzle. An array of buttons positioned above the grid facilitates various functions, including navigation back to the home screen, loading a new game, restarting the current game, undoing moves in reverse order, and marking moves as correct or incorrect.

<p align="center"> 
    <img src="https://github.com/filipemedeiross/solving_sudoku_by_search_for_csp/blob/main/examples/winner_screen.png?raw=true" width="250" height="400">
</p>

Upon successfully completing the puzzle, the timer halts, and interaction with the sudoku grid and associated functions ceases. However, users can still access options to return to the home screen and load a new game.

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

Objective Function: is omitted as it is irrelevant to the problem, since sudoku has a unique solution.

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

The solvers benchmark can be accessed through notebooks/solvers_benchmarks.ipynb, where we evaluated regular backtracking, search for constraint satisfaction problems, and integer linear programming. These solvers were assessed by calculating the average execution time across 20 different instances for each difficulty level. Additionally, we tested them on a puzzle created by finnish mathematician Arto Inkala, renowned as one of the most challenging sudoku puzzles worldwide.

> **Nota:** On a difficulty scale of 1 to 5 stars, the Inkala instance stands out as exceptionally challenging, earning an impressive 11 stars!

<p align="center"> 
    <img src="https://github.com/filipemedeiross/solving_sudoku_by_search_for_csp/blob/main/examples/benchmarks.png?raw=true" width="500" height="400">
</p>

By examining the data, we notice that the conventional search approach with backtracking proves highly efficient for simpler sudoku puzzles. However, it becomes impractical for tackling more intricate puzzles as the execution time significantly escalates.

While solving sudoku via integer linear programming presents a viable alternative, the search method tailored for constraint satisfaction problems emerges as the optimal choice. Under this strategy, the resolution time consistently stays below one tenths of a second even for the most challenging puzzle instances.

## Resolution Strategy Implemented in the Game

The game interface offers the option to mark filled cells as correct or incorrect. Upon initiating each new game instance, a separate solver is employed, distinct from the one used in the sudoku generator. This solver undergoes a preprocessing phase utilizing inference propagation through simple node consistency. Subsequently, it executes the AC-3 algorithm followed by a search with backtracking to solve the constraint satisfaction problem (CSP), encapsulated within the **solver_backtracking_for_csp.py** submodule of the **solvers** package.

To facilitate the application of the AC-3 algorithm, AllDifferent constraints are converted into binary constraints. This conversion enables the AC-3 algorithm to effectively reduce the domains of the variables, often leading to the discovery of a solution solely through inference propagation (consequently, the backtracking search for CSP only assigns values to the NxN variables once).

Upon successfully finding the solution, it is stored in a dedicated attribute of the game grid.

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
              generator.py                   Implements the sudoku generator
      solvers/                               Collect sudoku solvers        
              __init__.py
              solver_ip.py                   Solver using integer programming
              solver_exhaustive.py           Solver that performs an exhaustive search, used in the instance generator
              solver_backtracking.py         Solver using regular search strategy with backtracking
              solver_backtracking_for_csp.py Solver using backtracking search strategy for csp
      utils/                                 Too many features that do not fit in the above subpackages
              __init__.py
              constants.py
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

Stuart Russell and Peter Norvig. **Artificial Intelligence: A Modern Approach**. 3rd ed., Pearson, 2009.

Ana Flávia Uzeda dos Santos Macambira. **Programação Linear**. João Pessoa: Editora da UFPB, 2016.

Numpy: <https://numpy.org/doc/stable/>

Python-MIP: <https://docs.python-mip.com/en/latest/index.html>

Pygame: <https://www.pygame.org/docs/>

Images used: <https://opengameart.org/>
