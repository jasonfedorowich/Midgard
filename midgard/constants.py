from datetime import time, datetime

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
HERO_SCALE_SIZE = 2.679
MAX_HERO_SPEED = 7.0
LEVEL_SCALE_WIDTH = 3.7
LEVEL_SCALE_HEIGHT = 3.7
HERO_HEIGHT_CORRECTION = 21.5
LEVEL_WIDTH_CORRECTION = 70.0

#Hero constants


def get_time_millis():
    return round(datetime.utcnow().timestamp() * 1000)


class HeroConstants:

    def __init__(self):
        self.jump_speed = 7.0
        self.PLAYER_SPRITE_SHEET_LOCATION = '../images/hero_spritesheet.bmp'
        self.HERO_SCALE_SIZE = 2.679
        self.MAX_JUMP_HEIGHT = 150
        self.right_idle_list = [(2, 10, 30, 30), (35, 10, 30, 24), (132, 10, 28, 24)]
        self.right_walking_list = [(2, 41, 30, 24), (132, 41, 28, 24), (229, 41, 30, 24)]
        self.right_jump_list = [(2, 106, 30, 24), (67, 101, 30, 30), (99, 106, 30, 24)]
        self.right_attack_list = [(2, 73, 30, 24), (35, 67, 22, 28), (70, 65, 20, 30), (100, 66, 30, 29), (163, 69, 26, 28), (196, 76, 28, 22)]
        self.right_damage_list = [(2, 295, 24, 23), (31, 295, 30, 23), (62, 291, 32, 27)]
        self.right_dead_list = [(95, 298, 30, 18), (126, 303, 29, 14), (160, 303, 29, 14), (191, 303, 30, 14)]
        self.right_idle = (2, 8, 30, 28, 5, 3)
        self.right_walking = (2, 40, 30, 28, 8, 3)
        self.right_attacking = (2, 66, 30, 28, 7, 3)
        self.right_hit = (2, 130, 30, 28, 4, 3)
        self.right_dead = (2, 135, 30, 29, 7, 3)
        self.left_idle = (1, 165, 30, 28, 5, 3)
        self.left_walking = (1, 196, 30, 28, 8, 3)
        self.left_attacking = (2, 223, 30, 28, 7, 3)
        self.left_hit = (2, 260, 30, 28, 4, 3)
        self.left_dead = (2, 292, 30, 28, 7, 3)


class EnemyConstants:

    def __init__(self):
        self.SOILDER_FILE_LOCATION = '../images/Gladiator-Sprite Sheet.bmp'
