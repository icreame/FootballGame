import math
import pygame


# 定义足球类

class Ball(pygame.sprite.Sprite):
    def __init__(self, images, position):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = pygame.image.load(self.images[0])
        # 返回球的矩形对象，方便地获取图像的位置和大小信息
        # 以便在游戏中进行碰撞检测、位置调整等操作
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = position
        self.mask = pygame.mask.from_surface(self.image)
        # 球的速度
        self.speed = 0
        # 球的方向
        self.direction = [0, 0]
        # 控制球的队员
        self.taken_by_player = None
        # 用于切换球的动作
        self.pointer = 0
        self.count = 0
        self.change_frequency = 3  # 多少帧后切换动作
        # 状态
        self.ismoving = False

    def update(self, screen_size) :
        # 球静止则不做任何操作
        if not self.ismoving:
            return
        # 当球在动的时候，实现球的滚动效果
        self.count += 1
        if self.count == self.change_frequency:
            self.count = 0
            self.pointer = (self.pointer + 1) % len(self.images)
            self.image = pygame.image.load(self.images[self.pointer])
        # 球在队员脚下,让球跟随队员的移动
        if self.taken_by_player is not None:
            self.setdirection(self.taken_by_player.direction)
            if self.taken_by_player.direction[0] < 0:
                self.rect.left, self.rect.top = self.taken_by_player.rect.left - 15, self.taken_by_player.rect.top + 30
            elif self.taken_by_player.direction[0] > 0:
                self.rect.left, self.rect.top = self.taken_by_player.rect.left + 30, self.taken_by_player.rect.top + 30
            elif self.taken_by_player.direction[1] < 0:
                self.rect.left, self.rect.top = self.taken_by_player.rect.left + 15, self.taken_by_player.rect.top - 15
            elif self.taken_by_player.direction[1] > 0:
                self.rect.left, self.rect.top = self.taken_by_player.rect.left + 10, self.taken_by_player.rect.top + 50
            return
        # 球被射出去，没在队员的脚下
        ori_position = self.rect.left, self.rect.right, self.rect.top, self.rect.bottom
        # 球会逐渐减速
        self.speed = max(self.speed - 1.7 * 0.05, 0.0)
        if self.speed == 0.0:
            self.ismoving = False
        # 确定球运动的方向和距离
        vector = [self.speed * self.direction[0], self.speed * self.direction[1]]
        vector[0] = vector[0] / math.pow(self.direction[0] ** 2 + self.direction[1] ** 2, 0.5)
        vector[1] = vector[1] / math.pow(self.direction[0] ** 2 + self.direction[1] ** 2, 0.5)

        # 球的边界问题设置
        self.rect.left = min(max(0, self.rect.left + vector[0]), screen_size[0] - 48)
        self.rect.top = min(max(0, self.rect.top + vector[1]), screen_size[1] - 20)
        if self.rect.left == 0 or self.rect.left == screen_size[0] - 48:
            self.direction = self.direction[0] * -0.8, self.direction[1]
            self.speed = max(self.speed-1.7*0.75 , 0.0)
        # 撞门框
        if ori_position[1] > 1121 or ori_position[0] < 75:
            if self.rect.bottom > 305 and self.rect.top < 505:
                if self.direction[1] > 0:
                    self.rect.bottom = 305
                    self.direction = self.direction[0], self.direction[1] * -0.8
                elif self.direction[1] < 0:
                    self.rect.top = 505
                    self.direction = self.direction[0], self.direction[1] * -0.8
        if self.rect.top == 0 or self.rect.top == screen_size[1] - 20:
            self.direction = self.direction[0], self.direction[1] * -0.8
            self.speed = 0

    # 方向设置函数
    def setdirection(self, direction):
        self.ismoving = True
        self.direction = direction

    # 踢球
    def kick(self, direction):
        self.speed = 12
        self.direction = direction
        self.taken_by_player = None
        self.ismoving = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
