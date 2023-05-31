from bloodfootball import BloodFootballGame
import pygame


def main():
    pygame.init()
    game = BloodFootballGame()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
