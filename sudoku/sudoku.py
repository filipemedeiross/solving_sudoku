import pygame
from pygame.locals import *
from webbrowser import open

from .constants import *
from .logic_game import SudokuLogic
from .utils import flatten_position
from .solvers import solver_backtracking_for_csp


class Sudoku:
    def __init__(self):
        self.update('init_var')

        # Instantiating the font, clock and screen
        pygame.init()

        self.font   = pygame.font.SysFont(FONT_TYPE, size=FONT_SIZE, bold=True)
        self.clock  = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SIZE)

        pygame.display.set_caption('Sudoku')

        # Defining the rects and images used in the game
        self.rects = self.load_rects()
        self.grid_rect = pygame.Rect((self.rects[0].left - 4 * SPC_BL,
                                      self.rects[0].top  - 4 * SPC_BL,
                                      self.rects[8].right   - self.rects[0].left + 8 * SPC_BL,
                                      self.rects[72].bottom - self.rects[0].top  + 8 * SPC_BL))

        self.grid = [self.load_image(p, (BL_SIZE, BL_SIZE)) for p in NUMBER_PATH]
        self.grid_alpha = [self.load_image(p, (BL_SIZE, BL_SIZE)) for p in ALPHAS_PATH]

        self.background = self.load_image(BG_PATH, SIZE)

        self.button_play = self.load_image(PLAY_PATH, BU_SIZE)
        self.button_play_rect = self.button_play.get_rect(topleft=(BP_LEFT, BP_TOP))

        self.button_info = self.load_image(INFO_PATH, BH_SIZE)
        self.button_info_rect = self.button_info.get_rect(bottomright=(BI_RIGHT, G_TOP - SPC_BU))

        self.button_return = self.load_image(RETURN_PATH, BH_SIZE)
        self.button_return_rect = self.button_return.get_rect(bottomleft=(G_LEFT, G_TOP - SPC_BU))

        self.button_refresh = self.load_image(REFRESH_PATH, BH_SIZE)
        self.button_refresh_rect = self.button_refresh.get_rect(topleft=(self.button_return_rect.right + SPC_BL,
                                                                         self.button_return_rect.top))

        self.button_rewind = self.load_image(REWIND_PATH, BH_SIZE)
        self.button_rewind_rect = self.button_rewind.get_rect(topleft=(self.button_refresh_rect.right + SPC_BL,
                                                                       self.button_refresh_rect.top))

        self.button_unmake = self.load_image(UNMAKE_PATH, BH_SIZE)
        self.button_unmake_rect = self.button_unmake.get_rect(topleft=(self.button_rewind_rect.right + SPC_BL,
                                                                       self.button_rewind_rect.top))

        self.button_solve = self.load_image(SOLVE_PATH, BH_SIZE)
        self.button_solve_rect = self.button_solve.get_rect(topleft=(self.button_unmake_rect.right + SPC_BL,
                                                                     self.button_unmake_rect.top))

        self.button_time = self.load_image(EMPTY_PATH, EMPT_SIZE)
        self.button_time.set_alpha(160)
        self.button_time_rect = self.button_time.get_rect(center=self.button_play_rect.center)

        self.button_win = self.load_image(WIN_PATH, WIN_SIZE)
        self.button_win.set_alpha(180)
        self.button_win_rect = self.button_win.get_rect(topleft=self.rects[0].topleft)

    def init_game(self):
        while True:
            self.main_screen()
            self.play()

    def main_screen(self):
        self.display_main_screen()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(0)
                if event.type == MOUSEBUTTONDOWN:
                    if self.button_play_rect.collidepoint(event.pos):
                        return
                    if self.button_info_rect.collidepoint(event.pos):
                        open('https://github.com/filipemedeiross/', new=2)

    def play(self):
        self.display_play_screen()

        sel  = 0
        time = 0

        self.clock.tick()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(0)
                if event.type == MOUSEBUTTONDOWN:
                    if self.button_return_rect.collidepoint(event.pos):
                        self.update()
                        return
                    elif self.button_refresh_rect.collidepoint(event.pos):
                        self.update()
                        time = 0
                        self.clock.tick()
                if not self.sudoku.won:
                    sel, action = self.interact_event(event, sel)

                    if action:
                        # Verified win only after valid input
                        if self.sudoku.won:
                            self.display_grid()
                            self.display_win()

            if not self.sudoku.won:
                time += self.clock.tick(10)

                self.display_grid()
                self.display_selected(sel)
                self.display_time(time)

    def display_main_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.button_info, self.button_info_rect)
        self.screen.blit(self.button_play, self.button_play_rect)

        self.display_grid()

        pygame.display.flip()

    def display_play_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.button_return, self.button_return_rect)
        self.screen.blit(self.button_refresh, self.button_refresh_rect)
        self.screen.blit(self.button_rewind, self.button_rewind_rect)
        self.screen.blit(self.button_unmake, self.button_unmake_rect)
        self.screen.blit(self.button_solve, self.button_solve_rect)

        pygame.display.flip()

    def display_grid(self):
        # Clearing the area that corresponds to the grid
        self.screen.blit(self.background, self.rects[0].topleft, area=self.button_win_rect)

        # Displaying the separators
        pygame.draw.rect(self.screen, COLOR_LINE, self.grid_rect, width=4 * SPC_BL, border_radius=10)
        pygame.draw.line(self.screen, COLOR_LINE, self.rects[2].topright, self.rects[74].bottomright, SPC_BL)
        pygame.draw.line(self.screen, COLOR_LINE, self.rects[5].topright, self.rects[77].bottomright, SPC_BL)
        pygame.draw.line(self.screen, COLOR_LINE, self.rects[18].bottomleft, self.rects[26].bottomright, SPC_BL)
        pygame.draw.line(self.screen, COLOR_LINE, self.rects[45].bottomleft, self.rects[53].bottomright, SPC_BL)

        # Displaying fixed screen elements
        for num, clue, rect in zip(*zip(*self.sudoku.grid_clues), self.rects):
            if num:
                self.screen.blit(self.grid[num - 1] if clue else self.grid_alpha[num - 1], rect)

        pygame.display.update(self.grid_rect)

    def display_selected(self, sel):
        color = self.color_block(sel)
        rect  = self.rects[sel]
        width = self.sudoku.grid[flatten_position(sel, inv=True)] and 2

        pygame.draw.rect(self.screen, color, rect, width, border_radius=3)

        pygame.display.update(rect)

    def display_time(self, time):
        secs = time // 1000

        time_text = self.font.render(f'{secs // 60}:{secs % 60}', True, COLOR_FONT)
        time_rect = time_text.get_rect(center=self.button_time_rect.center)

        self.screen.blit(self.button_time, self.button_time_rect)
        self.screen.blit(time_text, time_rect)

        pygame.display.update(self.button_time_rect)

    def display_win(self):
        self.screen.blit(self.button_win, self.button_win_rect)

        pygame.display.update(self.button_win_rect)

    def color_block(self, sel):
        if self.show_sol:
            coord = flatten_position(sel, inv=True)
            c_sol = self.sudoku.grid[coord]

            if c_sol:
                if c_sol == self.solution[coord]:
                    return COLOR_GREEN
                else:
                    return COLOR_RED

        return COLOR_SELECT

    def update(self, flag=None):
        if flag:
            self.sudoku = SudokuLogic()
        else:
            self.sudoku.update()

        self.solution = solver_backtracking_for_csp(self.sudoku.grid)
        self.show_sol = False

    def interact_event(self, event, sel):
        act = None

        # Mouse events
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.button_rewind_rect.collidepoint(mouse_pos):
                self.clear_grid()
            elif self.button_unmake_rect.collidepoint(mouse_pos):
                self.unmake()
            elif self.button_solve_rect.collidepoint(mouse_pos):
                self.show_solution()

        # Keyboard events
        elif event.type == KEYDOWN:
            key = event.key

            if key in MOVES.keys():
                sel = self.move(sel, *MOVES[key](sel))
            elif key == K_BACKSPACE:
                self.clear(sel)
            else:
                act = self.actions(key)
                self.insert(sel, act)

        return sel, act

    def clear_grid(self):
        self.sudoku.clear_grid()

    def unmake(self):
        self.sudoku.unmake()

    def show_solution(self):
        self.show_sol = not self.show_sol

    def move(self, sel, test, move):
        if test:
            sel += move

        return sel

    def clear(self, sel):
        self.sudoku.clear(*flatten_position(sel))

    def insert(self, sel, act):
        if act:
            self.sudoku.insert(*flatten_position(sel), act)

    def load_rects(self):
        spc = BL_SIZE + SPC_BL

        rects = []
        for j in range(N):
            for i in range(N):
                rects.append(pygame.Rect(G_LEFT + spc * i,
                                         G_TOP  + spc * j,
                                         BL_SIZE, BL_SIZE))

        return rects

    @staticmethod
    def load_image(path, size):
        return pygame.transform.scale(pygame.image.load(path), size)

    @staticmethod
    def actions(event):
        return ACTIONS.get(event)
