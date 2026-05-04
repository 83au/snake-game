from constants import (
    GRID_COLS, GRID_ROWS,
    RIGHT, OPPOSITES,
)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        # Start in the middle of the grid, 3 segments long, moving right
        mid_x = GRID_COLS // 2
        mid_y = GRID_ROWS // 2
        self.body = [
            (mid_x,     mid_y),
            (mid_x - 1, mid_y),
            (mid_x - 2, mid_y),
        ]
        self.direction = RIGHT
        self._pending_direction = RIGHT
        self._grow_pending = False

    # ------------------------------------------------------------------
    # Direction
    # ------------------------------------------------------------------

    def change_direction(self, new_dir):
        """Queue a direction change, ignoring 180° reversals."""
        if new_dir != OPPOSITES.get(self.direction):
            self._pending_direction = new_dir

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------

    def move(self):
        """Advance the snake one step. Returns True if the move was valid
        (no self-collision), False if the snake hit itself."""
        self.direction = self._pending_direction

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (
            (head_x + dx) % GRID_COLS,
            (head_y + dy) % GRID_ROWS,
        )

        # Insert new head
        self.body.insert(0, new_head)

        if self._grow_pending:
            self._grow_pending = False   # keep the tail (snake grew)
        else:
            self.body.pop()              # remove tail (normal move)

        return not self.check_self_collision()

    def grow(self):
        """Signal that the snake should grow on the next move."""
        self._grow_pending = True

    # ------------------------------------------------------------------
    # Collision
    # ------------------------------------------------------------------

    def check_self_collision(self):
        """Return True if the head overlaps any body segment."""
        return self.body[0] in self.body[1:]

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def head(self):
        return self.body[0]
