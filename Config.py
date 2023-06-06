import os


class Config:
    # 根目录
    root = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 60
    # 开始界面大小
    START_SCREENSIZE = (512, 512)
    GAME_SCREENSIZE = (1200, 800)
    # 标题
    TITLE = 'Futsal'
    # 颜色
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    LIGHTGREEN = (0, 100, 0)
    # 模式选择
    IS_TWO_PLAYERS = False
    # 背景音乐
    BGM_PATH = os.path.join(root, 'resources/audios/bgm.flac')
    # 游戏图片
    IMAGE_PATHS_DICT = {
        'players': [
            os.path.join(root, 'resources/images/player1.png'),
            os.path.join(root, 'resources/images/player2.png'),
            os.path.join(root, 'resources/images/player3.png'),
            os.path.join(root, 'resources/images/player4.png'),
        ],
        'balls': [
            os.path.join(root, 'resources/images/ball1.png'),
            os.path.join(root, 'resources/images/ball2.png'),
            os.path.join(root, 'resources/images/ball3.png'),
        ],
        'doors': [
            os.path.join(root, 'resources/images/door1.bmp'),
            os.path.join(root, 'resources/images/door2.bmp'),
        ],
    }
