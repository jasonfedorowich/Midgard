import pygame
from pygame.sprite import Sprite


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


class Enemy(Sprite):

    def __init__(self):
        super().__init__()
