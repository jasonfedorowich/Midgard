from enum import Enum

import pygame
from pygame.sprite import Sprite

from midgard.animation import Animation
from midgard.constants import EnemyConstants
from midgard.vector2d import Vector2D


class SpriteSheet:

    def __init__(self, file):
        self.sprite_sheet = pygame.image.load(file).convert()

    def get_image(self, x, y, width, height):
        sprite_sheet_copy = self.sprite_sheet.copy()
        image = pygame.Surface([width, height]).convert()
        image.blit(sprite_sheet_copy, (0, 0), (x, y, width, height))
        image.set_colorkey((255, 255, 255))
        return image

    def _get_image_row(self, x, y, width, height, number_of_images, seperation):
        images = []

        for image_number in range(number_of_images - 1):
            image = self.get_image(x, y, width, height)
            images.append(image)
            x += width
            x += seperation

        return images

    def get_image_row(self, row_info):
        return self._get_image_row(row_info[0], row_info[1], row_info[2], row_info[3], row_info[4], row_info[5])

    def get_images(self, locations, flip):
        images = []
        for location in locations:
            image = self.get_image(location[0], location[1], location[2], location[3])
            if flip:
                image = pygame.transform.flip(image, True, False)
            images.append(image)

        return images


class SpriteState:
    def __init__(self, enemy):
        self.enemy = enemy
        pass


class Renderable(SpriteState):
    def __init__(self, enemy):
        super().__init__(enemy)


class NonRenderable(SpriteState):
    def __init__(self, enemy):
        super().__init__(enemy)


class EnemyType(Enum):
    SOILDER = (1, 2.00)

    def __init__(self, number, scale):
        self.number = number
        self.scale = scale


class Enemy(Sprite):
    sprite_sheet_dictionaries = {}

    def __init__(self, x, y, type, level):
        super().__init__()
        self.level = level
        self.vector = Vector2D()
        self.vector.x = x
        self.vector.y = y
        self.type = type
        self.sprite_sheet_dictionary = Enemy.sprite_sheet_dictionaries[type]
        self.animation = Animation(self.sprite_sheet_dictionary, 100)
        self.state = NonRenderable(self)
        self.animation.set_frames('left_idle')

        self.image = self.animation.current_animation_with_scale(type.value[1])
        self.rect = self.image.get_rect()
        self.rect.left = self.vector.x
        self.rect.bottom = self.vector.y
        self.type = type

        #TODO move out
        self.damage = 10

    def blitme(self):
        self.rect.x = self.vector.x - self.level.camera.vector.x + self.rect.width
        self.level.game.screen.blit(self.animation.current_animation_with_scale(self.type.value[1]), self.rect)
        #pygame.draw.rect(self.level.game.screen, pygame.Color('red'), self.rect)

    def update(self):
        self.animation.set_frames('left_idle')

    def take_damage(self, damage):
        pass

    @classmethod
    def init(cls):
        enemy_constants = EnemyConstants()
        soilder_spritesheet = SpriteSheet(enemy_constants.SOILDER_FILE_LOCATION)
        soilder_map = {
            'left_idle': soilder_spritesheet.get_images([(4, 6, 22, 26), (36, 5, 23, 32), (133, 6, 20, 24)], True)}

        Enemy.sprite_sheet_dictionaries[EnemyType.SOILDER] = soilder_map

    @classmethod
    def create_enemy(cls, type, x, y, level):
        return Enemy(x, y, type, level)
