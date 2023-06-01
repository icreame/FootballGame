import pygame
import random


# 定义球员类
class Player(pygame.sprite.Sprite):
    def __init__(self, image, position, direction=(1, 0), autocontrol=False, playerType=None, groupId=None):
        pygame.sprite.Sprite.__init__(self)
        self.direction = None
        self.images = None
        self.image = None
        self.rect = None
        self.mask = None
        self.image_dict = {
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
        self.po = position  # 位置备份
        self.position = list(position)
        self.autocontrol = autocontrol
        self.playerType = playerType
        self.grounpId = groupId
        # 人物动画的实现
        self.pointer = 0
        self.count = 0
        self.change_frequency = 3
        # 方向的设置
        self.setdirection(direction)
        # 人物速度
        self.speed = 2
        # 是否在运动状态
        self.ismoving = False
        # 人物踢球动作的实现
        self.prepare_kicking = False
        self.prepare_kicking_count = 0
        self.prepare_kicking_freq = 20
        # 保持运动方向
        self.keep_direction_freq = 50
        self.keep_direction_count = 0

    def update(self, screensize, ball):
        # 电脑自动操控的人物
        if self.autocontrol:
            self.autoupdate(screensize, ball)
            return
        if not self.ismoving:
            return
        # 切换人物动作，实现动画效果
        self.switch()
        # 根据方向移动人物
        speed = self.speed * self.direction[0], self.speed * self.direction[1]
        self.position[0] = min(max(0, self.position[0] + speed[0]), screensize[0] - 48)
        self.position[1] = min(max(0, self.position[1] + speed[1]), screensize[1] - 48)
        self.rect.left, self.rect.top = self.position
        # 判断人物是否在球门区域
        if self.rect.top > 310 and self.rect.bottom < 650:
            # 判断球员s是否靠近球门边界
            if self.rect.right > 885:  # 离球门的右边界很近
                self.position[0] = min(self.position[0], 884)
            elif self.rect.left < 75:  # 离球门左边界很近
                self.position[0] = max(self.position[0], 76)
        # 更新图像位置
        self.rect.left, self.rect.top = self.position
        # 设置为静止状态
        self.ismoving = False

    def autoupdate(self, screensize, ball):
        # 守门员
        if self.playerType == 'goalkeeper':
            self.speed = 1

            # 守门
            def goalkeep(self):
                self.switch()
                # 大于305，小于460
                self.position[0] = min(max(self.po[0], self.position[0] + self.direction[0] * self.speed),
                                       self.po[0] + 40)
                self.position[1] = min(max(305, self.position[1] + self.direction[1] * self.speed), 460)
                self.rect.left, self.rect.top = self.position
                if self.rect.top == 305 or self.rect.top == 460:  # 反向走
                    self.direction = self.direction[0], -self.direction[1]
                    self.setdirection(self.direction)
                if self.rect.left == self.po[0] or self.rect.left == self.po[0] + 40:
                    self.direction = -self.direction[0], self.direction[1]
                    self.setdirection(self.direction)

            # 守门员拿球就随机射球
            if ball.taken_by_player == self:
                if self.grounpId == 1:
                    if random.random() > 0.8 or self.prepare_kicking:
                        self.prepare_kicking = True
                        self.setdirection((1, 0))
                        self.prepare_kicking_count += 1
                        # 通过计数机制，可以控制球员准备踢球的频率，以避免过于频繁地执行该动作。
                        # 这可能是为了增加游戏的难度或使球员的行为更加真实和可预测。
                        # 计数机制可以在一定程度上限制特定动作的使用次数，
                        # 并为游戏提供更好的平衡和可玩性。
                        if self.prepare_kicking_count > self.prepare_kicking_freq:
                            self.prepare_kicking_count = 0
                            self.prepare_kicking = False
                            ball.kick(self.direction)
                            self.setdirection(random.choice([(0, 1), (0, -1)]))
                    else:
                        goalkeep(self)
                else:
                    if random.random() > 0.8 or self.prepare_kicking:
                        self.prepare_kicking = True
                        self.setdirection((-1, 0))
                        if self.prepare_kicking:
                            self.prepare_kicking_count += 1
                            if self.prepare_kicking_count > self.prepare_kicking_freq:
                                self.prepare_kicking_count = 0
                                self.prepare_kicking = False
                                ball.kick(self.direction)
                                self.setdirection(random.choice([(0, 1), (0, -1)]))
                    else:
                        goalkeep(self)
            # 没球来回走
            else:
                goalkeep(self)
        # 其他球员的行为
        else:
            self.switch()
            # 球在自己的脚下
            if ball.taken_by_player == self:
                if self.grounpId == 1:
                    # 球员跑的方向为右边的球门
                    self.direction = min(max(1150 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                else:
                    self.direction = min(max(350 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                self.setdirection(self.direction)
                # 射门
                if (random.random() > 0.96 and 150 < self.position[0] < 1150) or self.prepare_kicking:
                    if self.grounpId == 1:
                        # 射门方向
                        self.direction = min(max(1190 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                    else:
                        self.direction = min(max(150 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                    self.setdirection(self.direction)
                    self.prepare_kicking = True
                    self.prepare_kicking_count += 1
                    if self.prepare_kicking_count > self.prepare_kicking_freq:
                        self.prepare_kicking_count = 0
                        self.prepare_kicking = False
                        ball.kick(self.direction)
                # 单独带球
                else:
                    speed = self.speed * self.direction[0], self.speed * self.direction[1]
                    ori_position = self.position.copy()
                    # 保证人物不出边线
                    self.position[0] = min(max(0, self.position[0] + speed[0]), screensize[0] - 48)
                    self.position[1] = min(max(0, self.position[1] + speed[1]), screensize[1] - 48)
                    self.rect.left, self.rect.top = self.position
                    # 保证人物不进入门框
                    if self.rect.top > 305 and self.rect.bottom < 460 and (
                            self.rect.right > 1121 or self.rect.left < 75):
                        self.position = ori_position
                        self.rect.left, self.rect.top = self.position
            # 球没在自己的脚下
            else:
                # 各司其职
                if (10 < ball.rect.centerx < 600 and self.playerType == 'defender1') or (
                        600 <= ball.rect.centerx < 1180 and self.playerType == 'defender2') or (
                        ball.rect.centery <= 400 and self.playerType == 'forwardleft') or (
                        ball.rect.centery > 400 and self.playerType == 'forwardright') or self.playerType == 'common':
                    # （1，1）球在上左方，（-1，1）球在下左方
                    # （1，-1）球在上右方，（-1，-1）球在下右方
                    self.direction = min(max(ball.rect.left - self.rect.left, -1), 1), min(
                        max(ball.rect.top - self.rect.top, -1), 1)
                    # 在确保往球的方向跑的同时，增加方向的随机性
                    self.direction = self.direction[0] * random.random(), self.direction[1] * random.random()
                else:
                    # 在一个方向上保持运动一段距离，再随机换向
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
                self.position[0] = min(max(0, self.position[0] + speed[0]), screensize[0] - 48)
                self.position[1] = min(max(0, self.position[1] + speed[1]), screensize[1] - 48)
                # 更新人物位置
                self.rect.left, self.rect.top = self.position
                if self.rect.top > 305 and self.rect.bottom < 460 and (
                        self.rect.right > 1121 or self.rect.left < 75):
                    self.position = ori_position
                    self.rect.left, self.rect.top = self.position

    def switch(self):
        self.count = self.count + 1
        if self.count == self.change_frequency:
            self.count = 0
            self.pointer = (self.pointer + 1) % len(self.images)
            self.image = self.images[self.pointer]

    def setdirection(self, direction):
        self.direction = direction
        self.ismoving = True
        self.images = self.fetchimages(direction)
        self.image = self.images[self.pointer]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.position
        self.mask = pygame.mask.from_surface(self.image)

    def fetchimages(self, direction):
        if direction[0] > 0:
            return self.image_dict['right']
        elif direction[0] < 0:
            return self.image_dict['left']
        elif direction[1] > 0:
            return self.image_dict['down']
        elif direction[1] < 0:
            return self.image_dict['up']
        else:
            return self.images

    def draw(self, screen):
        screen.blit(self.image, self.rect)
