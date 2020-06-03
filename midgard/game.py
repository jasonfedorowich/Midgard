import sys
import pygame

from midgard.camera import Camera
from midgard.input import InputManager
from midgard.level import Level1
from midgard.player import Player
from midgard.settings import Settings
from midgard.sprite import Enemy


class Game:

    def __init__(self):

        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        #TODO need to move some of these calls around create a game menu and some will be moved as part of game objects vs essentials objects
        self._init()
        pygame.display.set_caption('Midgard')
        self.color = self.settings.bg_color
        self.camera = Camera(self.settings.screen_width, self.settings.screen_height)
        # self.camera.update_viewport(self.camera.vector.x + 2000, self.camera.vector.y)
        self.level = Level1(self, self.camera, '../images/level1.bmp')
        self.player = Player(self)
        self.level.start()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        self.game_running = True
        self.game_active = True
        self.input = InputManager(self)

    # pygame.display.set_caption("{}".format(clock.get_fps()))
    def _init(self):
        Enemy.init()
        pass

    def run_game(self):

        while self.game_running:

            if self.game_active:
                self.input.process_events()
                self.player.update()
                self.update_fps()
                self.level.update()
                self._update_screen()


            self.clock.tick(60)


    def _update_screen(self):
        self.screen.fill(self.color)
        self.level.blitme()
        self.player.blitme()
        # pygame.draw.line(self.screen, pygame.Color('red'), (0, 165 * LEVEL_SCALE_HEIGHT), (184 * LEVEL_SCALE_WIDTH, 165 * LEVEL_SCALE_HEIGHT))

        self.screen.blit(self.update_fps(), (10, 0))
        pygame.display.flip()



    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color('black'))
        return fps_text


if __name__ == '__main__':
    ai = Game()
    ai.run_game()
