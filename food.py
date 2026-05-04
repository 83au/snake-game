import random
from constants import GRID_COLS, GRID_ROWS


class Food:
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.randomize(snake_body)

    def randomize(self, snake_body):
        """Place food on a random cell not occupied by the snake."""
        snake_set = set(snake_body)
        all_cells = [
            (x, y)
            for x in range(GRID_COLS)
            for y in range(GRID_ROWS)
            if (x, y) not in snake_set
        ]
        if all_cells:
            self.position = random.choice(all_cells)
