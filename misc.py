import pygame
import sys


# 窗口创建
def InitPygame(screensize, title='Futsal', init_mixer=True):
    pygame.init()
    if init_mixer:
        pygame.mixer.init()
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption(title)
    return screen


def QuitGame(use_pygame=True):
    if use_pygame:
        pygame.quit()
    sys.exit()


def play_bgm(self):
    pygame.mixer.music.load(self.bgm_path)
    pygame.mixer.music.play(-1, 0, 0)
