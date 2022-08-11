# Defining game constants


# Colors in RGB
COLOR_LINE = 0, 0, 0  # black color
COLOR_FONT = 255, 255, 255  # white color
COLOR_SELECT = 200, 200,  255

# Display dimensions
size = width, height = 320, 480

# Indent
grid_top = height // 5
grid_left = 20

# Spacing
spacing_buttons = 30
spacing_blocks = 2
slip_font = 5

# Dimensions of screen elements
font_size = 20
block_size = (width - 2 * grid_left - 8 * spacing_blocks) / 9
button_size = button_width, button_height = width - 4 * grid_left, spacing_buttons
