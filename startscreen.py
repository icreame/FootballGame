import pygame
from misc import QuitGame
import os


# 游戏的开始界面
def StartScreen(screen, cfg):
    # 创建始终对象，控制帧率
    clock = pygame.time.Clock()
    root = os.path.split(os.path.abspath(__file__))[0]
    font = pygame.font.Font(os.path.join(root, 'resources/fonts/simkai.ttf'), 30)
    flag = True
    count = 0
    font_render1 = font.render("模式选择（O：单人模式/T:双人模式）", True, cfg.RED)
    font_render2 = font.render("按p键暂停游戏", True, cfg.RED)
    font_render3 = font.render("按R键重新开始游戏", True, cfg.RED)
    while True:
        count = count + 1
        if count > 20:
            count = 0
            flag = not flag
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                cfg.IS_TWO_PLAYERS = True
                return True
        image = pygame.image.load(os.path.join(root, 'resources/images/R1.png'))
        screen.blit(image, (0, 0))
        if flag:
            screen.blit(font_render1, (22, 300))
            screen.blit(font_render2, (150, 350))
            screen.blit(font_render3, (150, 400))
        clock.tick(cfg.FPS)
        pygame.display.update()
