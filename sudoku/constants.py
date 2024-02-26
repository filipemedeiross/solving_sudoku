# Defining game constants


# Settings
N = 9

FONT_TYPE = 'tlwgtypo'

BG_PATH      = 'sudoku/media/background.jpg'
WIN_PATH     = 'sudoku/media/win.png'
PLAY_PATH    = 'sudoku/media/play.png'
INFO_PATH    = 'sudoku/media/info.png'
SOLVE_PATH   = 'sudoku/media/solve.png'
RETURN_PATH  = 'sudoku/media/return.png'
REWIND_PATH  = 'sudoku/media/rewind.png'
UNMAKE_PATH  = 'sudoku/media/unmake.png'
REFRESH_PATH = 'sudoku/media/refresh.png'

NUMBER_PATH = [f'sudoku/media/number_0{i}.png'
               for i in range(1, N + 1)]
ALPHAS_PATH = [f'sudoku/media/number_alpha_0{i}.png'
               for i in range(1, N + 1)]

# Colors in RGB
COLOR_FONT   = 255, 255, 255
COLOR_LINE   = 218, 112, 214
COLOR_SELECT = 200, 200,  255
COLOR_GREEN  = 0, 255, 0
COLOR_RED    = 255, 0, 0

# Display dimensions
SIZE = WDTH, HGHT = 320, 480

# Indent
G_TOP    = HGHT // 5.5
G_LEFT   = 20
BP_TOP   = 400
BP_LEFT  = 2 * G_LEFT
BI_BOTT  = G_TOP - 15
BI_RIGHT = WDTH - G_LEFT

# Spacing
SPC_BU = 30
SPC_BL = 2
SLIP_FONT = 5

# Dimensions of screen elements
FONT_SIZE = 20
BL_SIZE   = (WDTH - 2 * G_LEFT - 8 * SPC_BL) / N
BU_SIZE   = BU_WDTH, BU_HGHT = WDTH - 4 * G_LEFT, SPC_BU
BH_SIZE   = BU_HGHT, BU_HGHT
WIN_SIZE  = N * BL_SIZE + (N - 1) * SPC_BL, \
            N * BL_SIZE + (N - 1) * SPC_BL
