import os
import random
import pygame
from Config import Config
from modules.ball import Ball
from modules.player import Player
from modules.startinterface import StartInterface
from utils.misc import QuitGame
from utils.initialize import InitPygame
from utils.io import PygameResourceLoader

class BloodFootballGame:

    def __init__(self, **kwargs):
        self.screen = None
        self.resource_loader = None
        self.config = Config()
        self.cfg=self.config
        # 初始化
        self.initialize()
        # 用户可以覆盖默认参数
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def initialize(self):
            # 界面的大小和title设置
            screensize = self.config.SCREENSIZE
            title = self.config.TITLE
            self.screen = InitPygame(screensize, title)
            # 界面优化设置
            bgm_path = self.config.BGM_PATH
            font_paths_dict = self.config.FONT_PATHS_DICT
            image_paths_dict = self.config.IMAGE_PATHS_DICT
            self.resource_loader = PygameResourceLoader(image_paths_dict,font_paths_dict, bgm_path)

    def run(self):
        # 初始化
        screen=self.screen
        resource_loader=self.resource_loader
        cfg=self.cfg
        resource_loader.playbgm()
        # 游戏开始界面
        StartInterface(screen, resource_loader, cfg)
        # 游戏主循环
        screen = pygame.display.set_mode(cfg.SCREENSIZE_GAMING)
        score_group1=0
        score_group2 = 0
        font = resource_loader.fonts['default30']
        while True:
            win_group = self.playonegame(screen, resource_loader, cfg,
                                         font.render(f'{score_group1}   {score_group2}', False, cfg.WHITE))
            assert win_group in [1, 2]  # assert 语句用于在代码中进行断言检查，如果断言条件为假（False），
            # 则会引发 AssertionError 异常。如果断言条件为真（True），则程序会继续执行。
            if win_group == 1:
                score_group1 += 1
            else:
                score_group2 += 1

    # 进球一次
    def playonegame(self, screen, resource_loader, cfg, score_board):
        # 初始化双方球员
        players_group1 = pygame.sprite.Group()
        players_group2=pygame.sprite.Group()
        # --第一组
        position = random.randint(400, 500), random.randint(350 - 25, 450 - 25)
        player_controlled = Player(resource_loader.images['players'][0], position, (1, 0), False,'commom', 1)
        players_group1.add(player_controlled)

        position = random.randint(400, 500), random.randint(50 - 25, 350 - 25)
        players_group1.add(Player(resource_loader.images['players'][3], position, (1, 0), True, 'forwardleft', 1))

        position = random.randint(150, 225), random.randint(350 - 25, 450 - 25)
        players_group1.add(Player(resource_loader.images['players'][3], position, (1, 0), True, 'forwardright', 1))

        position = random.randint(400, 500), random.randint(450 - 25, 750 - 25)
        players_group1.add(Player(resource_loader.images['players'][3], position, (1, 0), True, 'defender1', 1))
        #守门员
        position = (85, 390)
        players_group1.add(Player(resource_loader.images['players'][1], position, (0, 1), True, 'goalkeeper', 1))


        # --第二组
        position = random.randint(600, 950), random.randint(350 - 25, 450 - 25)
        players_group2.add(Player(resource_loader.images['players'][2], position, (-1, 0), True, 'common', 2))

        position = random.randint(800, 1000), random.randint(350 - 25, 450 - 25)
        players_group2.add(Player(resource_loader.images['players'][2], position, (-1, 0), True, 'forwardleft', 2))

        position = random.randint(700, 950), random.randint(50 - 25, 350 - 25)
        players_group2.add(Player(resource_loader.images['players'][2], position, (-1, 0), True, 'forwardright', 2))

        position = random.randint(700, 950), random.randint(450 - 25, 750 - 25)
        players_group2.add(Player(resource_loader.images['players'][2], position, (-1, 0), True, 'defender2', 2))
        # 守门员
        position = (1070, 390)
        players_group2.add(Player(resource_loader.images['players'][1], position, (0, 1), True, 'goalkeeper', 2))
        # 初始化足球
        ball = Ball(resource_loader.images['balls'], (600, 400))
        # 游戏主循环
        #在给定的代码中，clock = pygame.time.Clock() 创建了一个时钟对象，
        # 并将其赋值给变量 clock。这样，在游戏主循环中可以使用 clock 对象来控制游戏的帧率。
        clock = pygame.time.Clock()
        paused = False
        while True:
            # --基础背景绘制
            screen.fill(cfg.LIGHTGREEN)
            pygame.draw.circle(screen, cfg.WHITE, (600, 400), 80, 5)
            pygame.draw.rect(screen, cfg.WHITE, (10, 10, 600, 790), 5)
            pygame.draw.rect(screen, cfg.WHITE, (600, 10, 590, 790), 5)
            pygame.draw.rect(screen, cfg.WHITE, (10, 150, 300, 500), 5)
            pygame.draw.rect(screen, cfg.WHITE, (890, 150, 300, 500), 5)
            screen.blit(resource_loader.images['doors'][1].convert(), (8, 305))
            screen.blit(resource_loader.images['doors'][0].convert(), (1121, 305))
            screen.blit(score_board, (565, 15))
            # --事件监听，完成英雄的控制
            for event in pygame.event.get():    #pygame.event.get()获取当前的事件列表
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    QuitGame()
                elif event.type== pygame.KEYDOWN and event.key == pygame.K_p:
                    paused=not paused
            if paused:
                continue


            pressed_keys = pygame.key.get_pressed() #获取当前按键值
            direction = [0, 0]      #存储球员移动位置
            if pressed_keys[pygame.K_w]:
                direction[1] -= 1
            if pressed_keys[pygame.K_d]:
                direction[0] += 1
            if pressed_keys[pygame.K_s]:
                direction[1] += 1
            if pressed_keys[pygame.K_a]:
                direction[0] -= 1
            if direction != [0, 0]:
                player_controlled.setdirection(direction)
            if pressed_keys[pygame.K_SPACE] and player_controlled == ball.taken_by_player:
                ball.kick(player_controlled.direction)
            # --更新玩家
            for item in players_group1:
                if pygame.sprite.collide_mask(item, ball) and ball.taken_by_player != item:
                    ball.is_moving = True
                    ball.taken_by_player = item
            for item in players_group2:
                if pygame.sprite.collide_mask(item, ball) and ball.taken_by_player != item:
                    ball.is_moving = True
                    ball.taken_by_player = item
            for item in players_group1:
                item.update(cfg.SCREENSIZE_GAMING, ball)
            for item in players_group2:
                item.update(cfg.SCREENSIZE_GAMING, ball)
            # --更新球
            ball.update(cfg.SCREENSIZE_GAMING)
            # --更新屏幕
            ball.draw(screen)
            players_group1.draw(screen)
            players_group2.draw(screen)
            clock.tick(cfg.FPS)
            pygame.display.update()
            # --计算得分
            if ball.rect.bottom > 305 and ball.rect.top < 505:
                if ball.rect.right > 1121:
                    return 1
                elif ball.rect.left < 75:
                    return 2
