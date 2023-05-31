import os


class Config:
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 50
    # 屏幕大小
    SCREENSIZE = (769, 563)
    SCREENSIZE_GAMING = (1200, 800)
    # 标题
    TITLE = '热血足球'
    # 一些颜色
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    LIGHTGREEN = (0, 100, 0)
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.flac')
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'players': [
            os.path.join(rootdir, 'resources/images/player1.png'),
            os.path.join(rootdir, 'resources/images/player2.png'),
            os.path.join(rootdir, 'resources/images/player3.png'),
            os.path.join(rootdir, 'resources/images/player4.png'),
        ],
        'balls': [
            os.path.join(rootdir, 'resources/images/ball1.png'),
            os.path.join(rootdir, 'resources/images/ball2.png'),
            os.path.join(rootdir, 'resources/images/ball3.png'),
        ],
        'doors': [
            os.path.join(rootdir, 'resources/images/door1.bmp'),
            os.path.join(rootdir, 'resources/images/door2.bmp'),
        ],
        'background_start': os.path.join(rootdir, 'resources/images/background_start.jpg'),
    }
    # 字体路径
    FONT_PATHS_DICT = {
        'default20': {'name': os.path.join(rootdir.replace('bloodfootball', 'base'), 'resources/fonts/simkai.ttf'),
                      'size': 20},
        'default30': {'name': os.path.join(rootdir.replace('bloodfootball', 'base'), 'resources/fonts/simkai.ttf'),
                      'size': 30},
        'default50': {'name': os.path.join(rootdir.replace('bloodfootball', 'base'), 'resources/fonts/simkai.ttf'),
                      'size': 50},
    }
