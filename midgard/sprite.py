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


class RenderState:
    def __init__(self, enemy):
        self.enemy = enemy
        pass


class Renderable(RenderState):
    def __init__(self, enemy):
        super().__init__(enemy)


class NonRenderable(RenderState):
    def __init__(self, enemy):
        super().__init__(enemy)


class EnemyType(Enum):
    SOILDER = (1, 2.00, 100)

    def __init__(self, number, scale, health):
        self.number = number
        self.scale = scale
        self.health = health


class Direction(Enum):
    LEFT = 1
    RIGHT = 2


class FrameState(Enum):
    IDLE = 1
    DAMAGED = 2
    DEAD = 3


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
        self.scale = type.value[1]
        self.image = self.animation.current_animation_with_scale(self.scale)
        self.rect = self.image.get_rect()
        self.rect.left = self.vector.x
        self.rect.bottom = self.vector.y
        self.type = type
        self.health = type.value[2]
        #TODO move out
        self.damage = 10
        self.direction = Direction.LEFT
        self.framestate = FrameState.IDLE

    def blitme(self):
        self.rect.x = self.vector.x - self.level.camera.vector.x + self.rect.width
        self.level.game.screen.blit(self.animation.current_animation_with_scale(self.scale), self.rect)
        #pygame.draw.rect(self.level.game.screen, pygame.Color('red'), self.rect)

    def update(self):
        if self.framestate == FrameState.DAMAGED:
            if self.animation.run_current_frames():
                if self.direction == Direction.LEFT:
                    self.animation.set_frames('left_idle')
                else:
                    self.animation.set_frames('right_idle')

        elif self.framestate == FrameState.DEAD:
            if self.animation.run_current_frames():
                self.kill()
        else:
            self.animation.run_current_frames()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            if self.direction == Direction.LEFT:
                self.animation.set_frames('left_dead')
            else:
                self.animation.set_frames('right_dead')

            self.framestate = FrameState.DEAD

        else:
            if self.direction == Direction.LEFT:
                self.animation.set_frames('left_damage')

            else:
                self.animation.set_frames('right_damage')

            self.framestate = FrameState.DAMAGED


    @classmethod
    def init(cls):
        enemy_constants = EnemyConstants()
        soilder_spritesheet = SpriteSheet(enemy_constants.SOILDER_FILE_LOCATION)
        soilder_map = {
            'left_idle': soilder_spritesheet.get_images([(4, 6, 22, 26), (36, 5, 23, 32), (133, 6, 20, 24)], True),
            'right_idle': soilder_spritesheet.get_images([(4, 6, 22, 26), (36, 5, 23, 32), (133, 6, 20, 24)], False),
            'left_damage': soilder_spritesheet.get_images([(4, 102, 22, 26), (35, 103, 25, 26), (66, 99, 32, 30)], True),
            'right_damage': soilder_spritesheet.get_images([(4, 102, 22, 26), (35, 103, 25, 26), (66, 99, 32, 30)], False),
            'left_dead': soilder_spritesheet.get_images([(4, 134, 22, 24), (36, 134, 24, 24), (66, 134, 30, 24), (100, 134, 25, 24), (161, 134, 29, 24), (193, 134, 31, 24)], True),
            'right_dead': soilder_spritesheet.get_images(
                [(4, 134, 22, 24), (36, 134, 24, 24), (66, 134, 30, 24), (100, 134, 25, 24), (161, 134, 29, 24),
                 (193, 134, 31, 24)], False)

        }

        Enemy.sprite_sheet_dictionaries[EnemyType.SOILDER] = soilder_map

    @classmethod
    def create_enemy(cls, type, x, y, level):
        return Enemy(x, y, type, level)
