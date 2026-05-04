# Window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TITLE = "Snake"

# Grid
GRID_SIZE = 20                          # pixels per cell
GRID_COLS = WINDOW_WIDTH // GRID_SIZE   # 30
GRID_ROWS = WINDOW_HEIGHT // GRID_SIZE  # 30

# Speed (moves per second)
INITIAL_SPEED = 8
MAX_SPEED = 20
SPEED_INCREMENT_EVERY = 5  # points gained before each +1 FPS

# Colors (R, G, B)
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
DARK_GRAY  = ( 30,  30,  30)
GRID_COLOR = ( 40,  40,  40)

SNAKE_HEAD  = ( 50, 205,  50)   # lime green
SNAKE_BODY  = ( 34, 139,  34)   # forest green
FOOD_COLOR  = (220,  20,  60)   # crimson

TEXT_COLOR       = (255, 255, 255)
SCORE_COLOR      = (200, 200, 200)
OVERLAY_COLOR    = (  0,   0,   0, 160)  # semi-transparent (used with surface alpha)

# Directions (dx, dy in grid units)
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
