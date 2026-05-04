import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, TITLE
from game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    game = Game(screen)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
