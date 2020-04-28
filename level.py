from abc import abstractmethod

import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite

from constants import LEVEL_SCALE_WIDTH, LEVEL_SCALE_HEIGHT, LEVEL_WIDTH_CORRECTION
from vector2d import Vector2D


class Level:

    def __init__(self, game, camera, image_file):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.file_image = image_file
        self.image = pygame.image.load(self.file_image)
        self.rect = self.image.get_rect()
        self.rect.top = self.screen_rect.top
        self.camera = camera
        self.image = pygame.transform.scale(self.image, (
            int(self.rect.width * LEVEL_SCALE_WIDTH), int(self.rect.height * LEVEL_SCALE_HEIGHT)))
        self.rect.x = - self.camera.vector.x
        self.vector = Vector2D()
        self.vector.x = float(self.rect.x)
        self.vector.y = float(self.rect.y)
        self.camera_position = self.camera.vector.x
        self.platforms = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

    def blitme(self):
        """
        could use area for camera or change the rect
        the way ive positioned the camera is that it takes the camera rect and subtracts it off to position the rect
        :return:
        """
        self.vector.x = - self.camera.vector.x
        self.rect.x = self.vector.x
        self.screen.blit(self.image, self.rect)

    def _update_position(self):
        self.vector.x = - self.camera.vector.x
        self.rect.x = self.vector.x
        self.camera_position = self.camera.vector.x

    def is_platform(self, vector):
        return vector.y >= self.screen_rect.midleft[1]

    def collide_with_platform(self, player):
        sprites = pygame.sprite.spritecollide(player, self.platforms, False, platform_player_collision)
        if sprites:
            for sprite in sprites:
                player.rect.bottom = sprite.vector_end.y
                player.vector.y = sprite.vector_end.y

                return True
        return False

    def collide_with_wall(self, player):
        collisions = pygame.sprite.spritecollideany(player, self.walls, wall_player_collision)
        if collisions:
            return True
        return False

    @abstractmethod
    def _construct_platforms(self):
        pass

    @abstractmethod
    def _construct_walls(self):
        pass

    def _add_platform(self, start, end):
        platform = Platform(start, end)
        self.platforms.add(platform)

    def _add_wall(self, start, end):
        wall = Wall(start, end)
        self.walls.add(wall)


# TODO add rect to platform and wall do we need two classes? """
"""
change so that we use sprite.collisionany to check if hit a platform on jump on hit a wall on movement

"""


def platform_player_collision(player, platform):
    print('-------')
    print(player.vector.x)
    print(platform.vector_start.x)
    print(platform.vector_end.x)
    print('-------')
    if platform.vector_start.x <= player.vector.x <= platform.vector_end.x or platform.vector_start.x <= abs(player.vector.x - player.rect.width) <= platform.vector_end.x:
        if player.vector.y == platform.vector_start.y or 0.001 <= abs(player.vector.y - platform.vector_start.y) <= 6.0:
            return True

    return False


def wall_player_collision(player, wall):
    pygame.draw.line(player.game.screen, pygame.Color('red'), (wall.vector_start.x, wall.vector_start.y),
                     (wall.vector_end.x, wall.vector_end.y))

    if wall.vector_end.y <= player.vector.y <= wall.vector_start.y:
        print('-------')
        print(player.vector.x)
        print(player.rect.right)
        print(player.rect.left)
        print(wall.vector_start.x)
        print(player.vector.x - wall.vector_start.x)
        print('-------')
        if player.vector.x == wall.vector_start.x or 0.001 <= abs(player.vector.x - wall.vector_start.x) <= 6.0:
            return True

    return False


class Platform(Sprite):

    def __init__(self, start, end):
        super().__init__()
        self.vector_start = Vector2D()
        self.vector_start.x = start[0]
        self.vector_start.y = start[1]

        self.vector_end = Vector2D()
        self.vector_end.x = end[0]
        self.vector_end.y = end[1]


class Wall(Sprite):

    def __init__(self, start, end):
        super().__init__()
        self.vector_start = Vector2D()
        self.vector_start.x = start[0]
        self.vector_start.y = start[1]

        self.vector_end = Vector2D()
        self.vector_end.x = end[0]
        self.vector_end.y = end[1]


class Level1(Level):

    def __init__(self, game, camera, image_file):
        super().__init__(game, camera, image_file)
        self._construct_platforms()
        self._construct_walls()

    def _construct_platforms(self):
        self._add_platform((0, 165 * LEVEL_SCALE_HEIGHT), (184 * LEVEL_SCALE_WIDTH - LEVEL_WIDTH_CORRECTION, 165 * LEVEL_SCALE_HEIGHT))
        pass

    def _construct_walls(self):
        self._add_wall((184 * LEVEL_SCALE_WIDTH - LEVEL_WIDTH_CORRECTION, 165 * LEVEL_SCALE_HEIGHT), (184 * LEVEL_SCALE_WIDTH - LEVEL_WIDTH_CORRECTION, 145 * LEVEL_SCALE_HEIGHT))
        pass






