import os
import pygame
from config import Config
from ball import Ball
from player import Player
from misc import InitPygame
from misc import QuitGame
from startscreen import StartScreen
from misc import playbgm


class FootballGame:

    def __init__(self, **kwargs):
        self.screen = None
        self.config = Config()
        self.cfg = self.config
        self.root = os.path.split(os.path.abspath(__file__))[0]
        # 初始化
        self.screensize = self.config.START_SCREENSIZE
        self.title = self.config.TITLE
        self.screen = InitPygame(self.screensize, self.title)
        # 界面优化设置
        self.bgm_path = self.config.BGM_PATH

        self.image_paths_dict = self.config.IMAGE_PATHS_DICT

    def run(self):
        # 初始化
        screen = self.screen

        cfg = self.cfg
        playbgm(self)
        # 游戏开始界面
        StartScreen(screen, cfg)
        # 游戏主循环
        screen = pygame.display.set_mode(cfg.GAME_SCREENSIZE)
        score_group1 = 0
        score_group2 = 0
        font = pygame.font.Font(os.path.join(self.root, 'resources/fonts/simkai.ttf'), 50)
        while True:
            win_group = self.playonegame(screen,  cfg,
                                         font.render(f'{score_group1}   {score_group2}', True, cfg.WHITE))
            # 断言限制只能返回1或2
            assert win_group in [1, 2]

            if win_group == 1:
                score_group1 += 1
            else:
                score_group2 += 1

    # 进球一次
    def playonegame(self, screen, cfg, score_board):
        # 初始化双方球员
        players_group1 = pygame.sprite.Group()
        players_group2 = pygame.sprite.Group()
        # --第一组
        player_controlled = Player(pygame.image.load(os.path.join(self.root, 'resources/images/player1.png')),
                                   (510, 400), (1, 0), False, 'commom', 1)
        players_group1.add(player_controlled)
        players_group1.add(
            Player(pygame.image.load(cfg.IMAGE_PATHS_DICT['players'][1]), (510, 250), (1, 0), True, 'forwardleft', 1))
        players_group1.add(
            Player(pygame.image.load(cfg.IMAGE_PATHS_DICT['players'][1]), (510, 550), (1, 0), True, 'forwardright', 1))
        players_group1.add(
            Player(pygame.image.load(cfg.IMAGE_PATHS_DICT['players'][1]), (250, 400), (1, 0), True, 'defender1', 1))
        # 守门员
        players_group1.add(
            Player(pygame.image.load(cfg.IMAGE_PATHS_DICT['players'][3]), (85, 390), (0, 1), True, 'goalkeeper', 1))

        # --第二组
        players_group2.add(
            Player(pygame.image.load(cfg.IMAGE_PATHS_DICT['players'][2]), (690, 400), (-1, 0), True, 'common', 2))
        players_group2.add(
            Player(pygame.image.load(cfg.IMAGE_PATHS_DICT['players'][2]), (700, 250), (-1, 0), True, 'forwardleft', 2))
        players_group2.add(
            Player(pygame.image.load(cfg.IMAGE_PATHS_DICT['players'][2]), (700, 550), (-1, 0), True, 'forwardright', 2))
        players_group2.add(
            Player(pygame.image.load(cfg.IMAGE_PATHS_DICT['players'][2]), (950, 400), (-1, 0), True, 'defender2', 2))
        # 守门员
        players_group2.add(
            Player(pygame.image.load(cfg.IMAGE_PATHS_DICT['players'][3]), (1070, 390), (0, 1), True, 'goalkeeper', 2))

        # 初始化足球

        ball = Ball(cfg.IMAGE_PATHS_DICT['balls'], (600, 400))
        # 游戏主循环
        # 在给定的代码中，clock = pygame.time.Clock() 创建了一个时钟对象，
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
            screen.blit(pygame.image.load(cfg.IMAGE_PATHS_DICT['doors'][1]).convert(), (8, 305))
            screen.blit(pygame.image.load(cfg.IMAGE_PATHS_DICT['doors'][0]).convert(), (1121, 305))
            screen.blit(score_board, (565, 15))
            # --事件监听，完成英雄的控制
            for event in pygame.event.get():  # pygame.event.get()获取当前的事件列表
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    QuitGame()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = not paused
            if paused:
                continue

            pressed_keys = pygame.key.get_pressed()  # 获取当前按键值
            direction = [0, 0]  # 存储球员移动位置
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
                    ball.ismoving = True
                    ball.taken_by_player = item
            for item in players_group2:
                if pygame.sprite.collide_mask(item, ball) and ball.taken_by_player != item:
                    ball.ismoving = True
                    ball.taken_by_player = item
            for item in players_group1:
                item.update(cfg.GAME_SCREENSIZE, ball)
            for item in players_group2:
                item.update(cfg.GAME_SCREENSIZE, ball)
            # --更新球
            ball.update(cfg.GAME_SCREENSIZE)
            # --更新屏幕
            ball.draw(screen)
            players_group1.draw(screen)
            players_group2.draw(screen)
            clock.tick(cfg.FPS)  # 每秒更新的次数
            pygame.display.update()
            # --计算得分
            if ball.rect.bottom > 305 and ball.rect.top < 505:
                if ball.rect.right > 1125:
                    return 1
                elif ball.rect.left < 73:
                    return 2
