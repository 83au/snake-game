import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TITLE,
    GRID_SIZE, GRID_COLS, GRID_ROWS,
    INITIAL_SPEED, MAX_SPEED, SPEED_INCREMENT_EVERY,
    BLACK, DARK_GRAY, GRID_COLOR,
    SNAKE_HEAD, SNAKE_BODY, FOOD_COLOR,
    TEXT_COLOR, SCORE_COLOR,
    UP, DOWN, LEFT, RIGHT,
)
from snake import Snake
from food import Food

# Game states
START     = "start"
PLAYING   = "playing"
PAUSED    = "paused"
GAME_OVER = "game_over"


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self._load_fonts()
        self._new_game()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _load_fonts(self):
        self.font_large  = pygame.font.SysFont("monospace", 48, bold=True)
        self.font_medium = pygame.font.SysFont("monospace", 28)
        self.font_small  = pygame.font.SysFont("monospace", 20)

    def _new_game(self):
        self.snake = Snake()
        self.food  = Food(self.snake.body)
        self.score = 0
        self.state = START

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self):
        running = True
        while running:
            running = self._handle_events()
            if self.state == PLAYING:
                self._update()
            self._draw()
            fps = self._current_fps()
            self.clock.tick(fps)

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def _handle_events(self):
        """Process events. Returns False when the game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                key = event.key

                # Universal quit
                if key in (pygame.K_q, pygame.K_ESCAPE):
                    return False

                # Direction keys (only in PLAYING state)
                if self.state == PLAYING:
                    if key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                    elif key == pygame.K_p:
                        self.state = PAUSED

                elif self.state == PAUSED:
                    if key == pygame.K_p:
                        self.state = PLAYING

                elif self.state == START:
                    if key == pygame.K_RETURN:
                        self.state = PLAYING

                elif self.state == GAME_OVER:
                    if key == pygame.K_RETURN:
                        self._new_game()
                        self.state = PLAYING

        return True

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def _update(self):
        alive = self.snake.move()
        if not alive:
            self.state = GAME_OVER
            return

        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score += 1
            self.food.randomize(self.snake.body)

    # ------------------------------------------------------------------
    # Speed
    # ------------------------------------------------------------------

    def _current_fps(self):
        if self.state != PLAYING:
            return 30  # UI frames when not animating snake
        speed = INITIAL_SPEED + self.score // SPEED_INCREMENT_EVERY
        return min(speed, MAX_SPEED)

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def _draw(self):
        self.screen.fill(DARK_GRAY)
        self._draw_grid()

        if self.state == START:
            self._draw_start()
        elif self.state == PLAYING:
            self._draw_playing()
        elif self.state == PAUSED:
            self._draw_playing()
            self._draw_overlay("PAUSED", "Press P to resume")
        elif self.state == GAME_OVER:
            self._draw_playing()
            self._draw_overlay("GAME OVER", f"Score: {self.score}  |  Press ENTER to restart")

        pygame.display.flip()

    def _draw_grid(self):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

    def _draw_playing(self):
        # Food
        fx, fy = self.food.position
        food_rect = pygame.Rect(fx * GRID_SIZE + 2, fy * GRID_SIZE + 2,
                                GRID_SIZE - 4, GRID_SIZE - 4)
        pygame.draw.ellipse(self.screen, FOOD_COLOR, food_rect)

        # Snake
        for i, (sx, sy) in enumerate(self.snake.body):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            seg_rect = pygame.Rect(sx * GRID_SIZE + 1, sy * GRID_SIZE + 1,
                                   GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(self.screen, color, seg_rect, border_radius=4)

        # Score HUD
        score_surf = self.font_small.render(f"Score: {self.score}", True, SCORE_COLOR)
        self.screen.blit(score_surf, (8, 8))

    def _draw_start(self):
        self._draw_centered_text(
            WINDOW_HEIGHT // 2 - 60, "SNAKE", self.font_large, TEXT_COLOR
        )
        self._draw_centered_text(
            WINDOW_HEIGHT // 2 + 10, "Press ENTER to play", self.font_medium, SCORE_COLOR
        )
        self._draw_centered_text(
            WINDOW_HEIGHT // 2 + 50, "Arrow keys to move  |  P to pause  |  Q to quit",
            self.font_small, SCORE_COLOR
        )

    def _draw_overlay(self, headline, subtext):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        self._draw_centered_text(
            WINDOW_HEIGHT // 2 - 40, headline, self.font_large, TEXT_COLOR
        )
        self._draw_centered_text(
            WINDOW_HEIGHT // 2 + 20, subtext, self.font_medium, SCORE_COLOR
        )

    def _draw_centered_text(self, y, text, font, color):
        surf = font.render(text, True, color)
        rect = surf.get_rect(centerx=WINDOW_WIDTH // 2, top=y)
        self.screen.blit(surf, rect)
