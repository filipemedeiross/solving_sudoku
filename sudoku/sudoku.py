import pygame
from .constants import *
from webbrowser import open
from .utils import N, flatten_position
from .logic_game import SudokuLogic


class Sudoku:
    def __init__(self):
        self.__sudoku = SudokuLogic()
        self.__solution = None  # initialized by clicking the solve button

        pygame.init()  # initializing pygame

        # Screen is initialized with init_game method
        self.screen = None

        # Create a Font object
        self.font = pygame.font.SysFont('tlwgtypo', size=font_size, bold=True)

        # Create an object to help update the grid
        self.clock = pygame.time.Clock()

        # Defining the Rects that will place the blocks on the screen
        self.rects = [pygame.Rect(grid_left + (block_size + spacing_blocks) * i,
                                  grid_top + (block_size + spacing_blocks) * j,
                                  block_size, block_size)
                      for j in range(N)
                      for i in range(N)]

        # Loading images used in the game
        self.background = pygame.transform.scale(pygame.image.load('sudoku/media/background.jpg'), size)

        self.grid = [pygame.transform.scale(pygame.image.load(f'sudoku/media/number_0{i}.png'),
                                            (block_size, block_size))
                     for i in range(1, N+1)]
        self.grid_alpha = [pygame.transform.scale(pygame.image.load(f'sudoku/media/number_alpha_0{i}.png'),
                                                  (block_size, block_size))
                           for i in range(1, N + 1)]

        self.button_play = pygame.transform.scale(pygame.image.load('sudoku/media/play.png'), button_size)
        self.button_play_rect = self.button_play.get_rect(topleft=(2 * grid_left,
                                                                   self.rects[-1].bottom + 1.5 * spacing_buttons))

        self.button_info = pygame.transform.scale(pygame.image.load('sudoku/media/info.png'),
                                                  (button_height, button_height))
        self.button_info_rect = self.button_info.get_rect(bottomright=(width - grid_left,
                                                                       grid_top - 0.5 * spacing_buttons))

        self.button_return = pygame.transform.scale(pygame.image.load('sudoku/media/return.png'),
                                                    (button_height, button_height))
        self.button_return_rect = self.button_return.get_rect(bottomleft=(grid_left,
                                                                          grid_top - spacing_buttons))

        self.button_refresh = pygame.transform.scale(pygame.image.load('sudoku/media/refresh.png'),
                                                     (button_height, button_height))
        self.button_refresh_rect = self.button_refresh.get_rect(topleft=(self.button_return_rect.right + spacing_blocks,
                                                                         self.button_return_rect.top))

        self.button_rewind = pygame.transform.scale(pygame.image.load('sudoku/media/rewind.png'),
                                                    (button_height, button_height))
        self.button_rewind_rect = self.button_rewind.get_rect(topleft=(self.button_refresh_rect.right + spacing_blocks,
                                                                       self.button_refresh_rect.top))

        self.button_unmake = pygame.transform.scale(pygame.image.load('sudoku/media/unmake.png'),
                                                    (button_height, button_height))
        self.button_unmake_rect = self.button_unmake.get_rect(topleft=(self.button_rewind_rect.right + spacing_blocks,
                                                                       self.button_rewind_rect.top))

        self.button_solve = pygame.transform.scale(pygame.image.load('sudoku/media/solve.png'),
                                                   (button_height, button_height))
        self.button_solve_rect = self.button_solve.get_rect(topleft=(self.button_unmake_rect.right + spacing_blocks,
                                                                     self.button_unmake_rect.top))

        self.button_win = pygame.transform.scale(pygame.image.load('sudoku/media/win.png'),
                                                 (N * block_size + (N-1) * spacing_blocks,
                                                  N * block_size + (N-1) * spacing_blocks))
        self.button_win.set_alpha(180)
        self.button_win_rect = self.button_win.get_rect(topleft=self.rects[0].topleft)

    def init_game(self):  # method that start the game
        # Creating a display Surface
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Sudoku")

        while True:
            self.main_screen()
            self.play()

    def main_screen(self):
        # Preparing the main screen
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.button_info, self.button_info_rect)
        self.display_grid()
        self.screen.blit(self.button_play, self.button_play_rect)

        pygame.display.flip()  # displaying the screen

        while True:
            # Getting input from user
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)  # leaving the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_play_rect.collidepoint(event.pos):
                        return
                    if self.button_info_rect.collidepoint(event.pos):
                        open('https://github.com/filipemedeiross/', new=2)

    def play(self):
        # Auxiliary variables
        time = 0
        selected = 0

        self.clock.tick()  # update the clock

        # Displaying fixed screen elements
        self.screen.blit(self.background, (0, 0))  # overriding home screen buttons

        self.screen.blit(self.button_return, self.button_return_rect)
        self.screen.blit(self.button_refresh, self.button_refresh_rect)
        self.screen.blit(self.button_rewind, self.button_rewind_rect)
        self.screen.blit(self.button_unmake, self.button_unmake_rect)
        self.screen.blit(self.button_solve, self.button_solve_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_return_rect.collidepoint(event.pos):
                        self.update()  # update the grid
                        return

                    elif self.button_refresh_rect.collidepoint(event.pos):
                        self.update()

                        time = 0  # auxiliary variables
                        self.clock.tick()  # update the clock

                        continue

                if not self.sudoku.won:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.button_rewind_rect.collidepoint(event.pos):
                            self.sudoku.clear_grid()  # clear the grid

                        elif self.button_unmake_rect.collidepoint(event.pos):
                            self.sudoku.unmake()

                        elif self.button_solve_rect.collidepoint(event.pos):
                            pass

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and selected > 8:
                            selected -= 9
                        elif event.key == pygame.K_DOWN and selected < 72:
                            selected += 9
                        elif event.key == pygame.K_RIGHT and (selected + 1) % N:
                            selected += 1
                        elif event.key == pygame.K_LEFT and selected % N:
                            selected -= 1
                        elif event.key == pygame.K_BACKSPACE:
                            self.sudoku.clear(*flatten_position(selected))
                        elif self.actions(event.key):
                            self.sudoku.insert(*flatten_position(selected), self.actions(event.key))

                            if self.sudoku.won:  # verified win only after valid input
                                self.display_grid()
                                self.screen.blit(self.button_win, self.button_win_rect)

            if not self.sudoku.won:
                self.display_grid()
                self.display_selected(selected)

                # Game time
                time += self.clock.tick(10)
                self.display_time(time)

            pygame.display.flip()

    def display_grid(self):
        # Clearing the area of the Rect self.button_win_rect that corresponds to the entire area filled with the grid
        self.screen.blit(self.background, self.rects[0].topleft, area=self.button_win_rect)

        # Displaying 3x3 square separators
        pygame.draw.line(self.screen, COLOR_LINE, self.rects[2].topright, self.rects[74].bottomright, spacing_blocks)
        pygame.draw.line(self.screen, COLOR_LINE, self.rects[5].topright, self.rects[77].bottomright, spacing_blocks)
        pygame.draw.line(self.screen, COLOR_LINE, self.rects[18].bottomleft, self.rects[26].bottomright, spacing_blocks)
        pygame.draw.line(self.screen, COLOR_LINE, self.rects[45].bottomleft, self.rects[53].bottomright, spacing_blocks)

        # Displaying fixed screen elements
        for num, clue, rect in zip(*zip(*self.sudoku.grid_clues), self.rects):
            if num:
                self.screen.blit(self.grid[num - 1] if clue else self.grid_alpha[num - 1], rect)

    def display_selected(self, selected):
        pygame.draw.rect(self.screen, COLOR_SELECT, self.rects[selected],
                         2 if self.sudoku.grid[flatten_position(selected, inverted=True)] else 0,
                         border_radius=3)

    def display_time(self, time):
        time_text = self.font.render(f'{time // 1000 // 60}:{time // 1000 % 60}', True, COLOR_FONT)

        left = width / 2 - time_text.get_width() / 2
        top = self.rects[-1].bottom + spacing_buttons

        self.screen.blit(self.background, (left - slip_font, top - slip_font),
                         area=(left - slip_font, top - slip_font,
                               time_text.get_width() + 2 * slip_font,
                               time_text.get_height() + 2 * slip_font))
        self.screen.blit(time_text, (left, top))

    def update(self):
        self.sudoku.update()  # update the grid

        self.__solution = None  # reset solution

    @staticmethod
    def actions(event):
        return {pygame.K_KP1: 1,
                pygame.K_KP2: 2,
                pygame.K_KP3: 3,
                pygame.K_KP4: 4,
                pygame.K_KP5: 5,
                pygame.K_KP6: 6,
                pygame.K_KP7: 7,
                pygame.K_KP8: 8,
                pygame.K_KP9: 9}.get(event)

    @property
    def sudoku(self):
        return self.__sudoku
