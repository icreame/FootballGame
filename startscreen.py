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
    font_render = font.render("按任意键开始游戏", True, cfg.RED)
    while True:
        count = count + 1
        if count > 20:
            count = 0
            flag = not flag
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            elif event.type == pygame.KEYDOWN:
                return True
        image=pygame.image.load(os.path.join(root, 'resources/images/R1.png'))
        screen.blit(image, (0, 0))
        if flag:
            screen.blit(font_render, (150,400))
        clock.tick(cfg.FPS)
        pygame.display.update()
