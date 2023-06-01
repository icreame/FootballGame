from football_game import FootballGame
import pygame


def main():
    pygame.init()
    game = FootballGame()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
