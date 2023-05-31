import random

import pygame


# 定义球员类,继承自pygame.sprite.Sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, image, position, direction=(1, 0), auto_control=False, player_type=None, group_id=None):
        pygame.sprite.Sprite.__init__(self)
        self.direction = None
        self.images = None
        self.image = None
        self.rect = None  # 人物区域
        self.mask = None
        # 图像切片
        # 通过将原始图像切割为不同方向下的小矩形区域，然后将这些区域组合成动画帧序列，
        #   可以在游戏中实现精灵的动画效果。
        # 这些图像切片存储在 images_dict 字典中，以方便在后续的操作中使用
        self.images_dict = {
            'down': [
                image.subsurface((0, 0, 32, 48)), image.subsurface((32, 0, 32, 48)),
                image.subsurface((64, 0, 32, 48)), image.subsurface((96, 0, 32, 48))
            ],
            'left': [
                image.subsurface((0, 48, 32, 48)), image.subsurface((32, 48, 32, 48)),
                image.subsurface((64, 48, 32, 48)), image.subsurface((96, 48, 32, 48))
            ],
            'right': [
                image.subsurface((0, 96, 32, 48)), image.subsurface((32, 96, 32, 48)),
                image.subsurface((64, 96, 32, 48)), image.subsurface((96, 96, 32, 48))
            ],
            'up': [
                image.subsurface((0, 144, 32, 48)), image.subsurface((32, 144, 32, 48)),
                image.subsurface((64, 144, 32, 48)), image.subsurface((96, 144, 32, 48))
            ],
        }
        self.po = position
        self.position = list(position)
        self.auto_control = auto_control
        self.player_type = player_type
        self.group_id = group_id
        # 用于切换人物动作的变量
        self.action_pointer = 0
        self.count = 0
        self.switch_frequency = 3
        # 设置方向
        self.setdirection(direction)
        # 人物速度
        self.speed = 2
        # 是否在运动状态
        self.is_moving = False
        # 准备踢球动作的变量
        self.prepare_for_kicking = False
        self.prepare_for_kicking_count = 0
        self.prepare_for_kicking_freq = 20
        # 保持运动方向的变量
        self.keep_direction_freq = 50
        self.keep_direction_count = 50

    '''更新'''

    def update(self, screen_size, ball):
        # 电脑自动控制
        if self.auto_control:
            self.autoupdate(screen_size, ball)
            return
        # 静止状态
        if not self.is_moving:
            return
        # 切换人物动作实现动画效果
        self.switch()
        # 根据方向移动人物
        ori_position = self.position.copy()
        speed = self.speed * self.direction[0], self.speed * self.direction[1]
        self.position[0] = min(max(0, self.position[0] + speed[0]), screen_size[0] - 48)
        self.position[1] = min(max(0, self.position[1] + speed[1]), screen_size[1] - 48)
        self.rect.left, self.rect.top = self.position
        if self.rect.bottom > 305 and self.rect.top < 505 and (self.rect.right > 1121 or self.rect.left < 75):
            self.position = ori_position
            self.rect.left, self.rect.top = self.position
        # 设置为静止状态
        self.is_moving = False

    '''自动更新'''

    def autoupdate(self, screen_size, ball):
        # 守门员
        if self.player_type == 'goalkeeper':
            self.speed = 1

            # 沿着门漫步
            def wondering(self):
                self.switch()
                # 大于305，小于459 85,390
                self.position[0] = min(max(self.po[0], self.position[0] + self.direction[0] * self.speed),
                                       self.po[0] + 40)
                self.position[1] = min(max(305, self.position[1] + self.direction[1] * self.speed), 459)

                self.rect.left, self.rect.top = self.position
                if self.rect.top == 305 or self.rect.top == 459:  # 反向走
                    self.direction = self.direction[0], -self.direction[1]
                    self.setdirection(self.direction)
                if self.rect.left == self.po[0] or self.rect.left == self.po[0] + 40:
                    self.direction = -self.direction[0], self.direction[1]
                    self.setdirection(self.direction)

            # 有球就随机射球
            if ball.taken_by_player == self:
                if self.group_id == 1:
                    if random.random() > 0.8 or self.prepare_for_kicking:
                        self.prepare_for_kicking = True
                        self.setdirection((1, 0))
                        if self.prepare_for_kicking:
                            self.prepare_for_kicking_count += 1
                            if self.prepare_for_kicking_count > self.prepare_for_kicking_freq:
                                self.prepare_for_kicking_count = 0
                                self.prepare_for_kicking = False
                                ball.kick(self.direction)
                                self.setdirection(random.choice([(0, 1), (0, -1)]))
                    else:
                        wondering(self)
                else:
                    if random.random() > 0.8 or self.prepare_for_kicking:
                        self.prepare_for_kicking = True
                        self.setdirection((-1, 0))
                        if self.prepare_for_kicking:
                            self.prepare_for_kicking_count += 1
                            if self.prepare_for_kicking_count > self.prepare_for_kicking_freq:
                                self.prepare_for_kicking_count = 0
                                self.prepare_for_kicking = False
                                ball.kick(self.direction)
                                self.setdirection(random.choice([(0, 1), (0, -1)]))
                    else:
                        wondering(self)
            # 没球来回走
            else:
                wondering(self)
        # 其他球员跟着球走
        else:
            # 球在自己的脚上
            if ball.taken_by_player == self:
                self.switch()
                if self.group_id == 1:
                    # 跑的方向
                    self.direction = min(max(1150 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                else:
                    self.direction = min(max(350 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                self.setdirection(self.direction)
                # 准备射门
                if (random.random() > 0.9 and 200 < self.position[0] < 1150) or self.prepare_for_kicking:
                    if self.group_id == 1:
                        # 射门方向
                        self.direction = min(max(1190 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                    else:
                        self.direction = min(max(150 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                    self.setdirection(self.direction)
                    self.prepare_for_kicking = True
                    if self.prepare_for_kicking:
                        self.prepare_for_kicking_count += 1
                        if self.prepare_for_kicking_count > self.prepare_for_kicking_freq:
                            self.prepare_for_kicking_count = 0
                            self.prepare_for_kicking = False
                            ball.kick(self.direction)
                # 单独带球
                else:
                    speed = self.speed * self.direction[0], self.speed * self.direction[1]
                    ori_position = self.position.copy()
                    self.position[0] = min(max(0, self.position[0] + speed[0]), screen_size[0] - 48)
                    self.position[1] = min(max(0, self.position[1] + speed[1]), screen_size[1] - 48)
                    self.rect.left, self.rect.top = self.position
                    if self.rect.bottom > 305 and self.rect.top < 505 and (
                            self.rect.right > 1121 or self.rect.left < 75):
                        self.position = ori_position
                        self.rect.left, self.rect.top = self.position
            # 球没在自己的脚下
            else:
                self.switch()
                if (10 < ball.rect.centerx < 600 and self.player_type == 'defender1') or (600 <= ball.rect.centerx < 1180 and self.player_type == 'defender2') or (
                        ball.rect.centery <= 400 and self.player_type == 'forwardleft') or (
                        ball.rect.centery > 400 and self.player_type == 'forwardright')  or self.player_type == 'common':
                    # （1，1）球在上左方，（-1，1）球在下左方
                    # （1，-1）球在上右方，（-1，-1）球在下右方
                    self.direction = min(max(ball.rect.left - self.rect.left, -1), 1), min(
                        max(ball.rect.top - self.rect.top, -1), 1)
                    # 增加方向的随机性
                    self.direction = self.direction[0] * random.random(), self.direction[1] * random.random()
                else:
                    if self.keep_direction_count >= self.keep_direction_freq:
                        self.direction = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
                        self.keep_direction_count = 0
                    else:
                        self.keep_direction_count += 1
                # 设置球员的移动方向
                self.setdirection(self.direction)
                # 计算球员的移动速度
                speed = self.speed * self.direction[0], self.speed * self.direction[1]
                # 备份当前位置
                ori_position = self.position.copy()
                # 将球员的位置限制在屏幕范围内
                self.position[0] = min(max(0, self.position[0] + speed[0]), screen_size[0] - 48)
                self.position[1] = min(max(0, self.position[1] + speed[1]), screen_size[1] - 48)
                # 更新人物位置
                self.rect.left, self.rect.top = self.position
                if self.rect.bottom > 305 and self.rect.top < 505 and (self.rect.right > 1121 or self.rect.left < 75):
                    self.position = ori_position
                    self.rect.left, self.rect.top = self.position

    # 实现人物上下左右的动画效果
    def switch(self):
        self.count += 1
        if self.count == self.switch_frequency:
            self.count = 0
            self.action_pointer = (self.action_pointer + 1) % len(self.images)
            self.image = self.images[self.action_pointer]

    # 设置方向

    def setdirection(self, direction):
        self.direction = direction
        self.is_moving = True
        self.images = self.fetchimages(direction)
        self.image = self.images[self.action_pointer]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.position
        self.mask = pygame.mask.from_surface(self.image)

    # 根据不同方向加载不同rect

    def fetchimages(self, direction):
        if direction[0] > 0:
            return self.images_dict['right']
        elif direction[0] < 0:
            return self.images_dict['left']
        elif direction[1] > 0:
            return self.images_dict['down']
        elif direction[1] < 0:
            return self.images_dict['up']
        else:
            return self.images

    def draw(self, screen):
        screen.blit(self.image, self.rect)
