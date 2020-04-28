import sys
from random import randint
import pygame

from camera import Camera
from constants import LEVEL_SCALE_HEIGHT, LEVEL_SCALE_WIDTH
from level import Level, Level1
from player import Player, Direction, WalkState, MoveUpState, MoveDownState, IdleState
from settings import Settings


class Game:

    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption('Midgard')
        self.color = self.settings.bg_color
        self.camera = Camera(self.settings.screen_width, self.settings.screen_height)
        # self.camera.update_viewport(self.camera.vector.x + 2000, self.camera.vector.y)
        self.level = Level1(self, self.camera, 'images/level1.bmp')
        self.player = Player(self)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)

    # pygame.display.set_caption("{}".format(clock.get_fps()))

    def run_game(self):
        while True:
            self._check_events()
            self.player.update()
            self.update_fps()
            self._update_screen()

            self.clock.tick(60)

    def _update_screen(self):
        self.screen.fill(self.color)
        self.level.blitme()
        self.player.blitme()
        pygame.draw.line(self.screen, pygame.Color('red'), (0, 165 * LEVEL_SCALE_HEIGHT), (184 * LEVEL_SCALE_WIDTH, 165 * LEVEL_SCALE_HEIGHT))

        self.screen.blit(self.update_fps(), (10, 0))
        pygame.display.flip()

    def _check_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.player.change_state(pygame.K_RIGHT, True)
        elif event.key == pygame.K_LEFT:
            self.player.change_state(pygame.K_LEFT, True)
        elif event.key == pygame.K_SPACE:
            self.player.change_state(pygame.K_SPACE, True)
        elif event.key == pygame.K_a:
            self.player.change_state(pygame.K_a, True)


    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.player.change_state(pygame.K_RIGHT, False)
        elif event.key == pygame.K_LEFT:
            self.player.change_state(pygame.K_LEFT, False)

        return

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color('black'))
        return fps_text


if __name__ == '__main__':
    ai = Game()
    ai.run_game()
