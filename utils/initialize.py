import pygame

'''基于pygame的游戏初始化'''


def InitPygame(screensize, title='热血足球', init_mixer=True):
    pygame.init()
    if init_mixer:
        # 调用pygame.mixer.init()函数将初始化音频混合器，准备开始使用Pygame的音频功能。
        # 通常，你可以在程序的开头调用这个函数，并在之后的代码中使用pygame.mixer模块来操作音频。
        pygame.mixer.init()
    # 创建一个新的可视窗口，并返回一个代表该窗口的Surface对象。
    # 这个Surface对象可以用于在窗口上进行绘图和显示图像。
    screen = pygame.display.set_mode(screensize)
    # 用于设置窗口的标题栏文本。
    pygame.display.set_caption(title)
    return screen
