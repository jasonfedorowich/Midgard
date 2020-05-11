import sys
import pygame

from midgard.camera import Camera
from midgard.constants import LEVEL_SCALE_HEIGHT, LEVEL_SCALE_WIDTH
from midgard.controller import Controller, buttons_to_keys
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
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        self.controller = Controller()
        try:
            self.controller.init()
        except Exception:
            pass

    # pygame.display.set_caption("{}".format(clock.get_fps()))
    def _init(self):
        Enemy.init()
        pass

    def run_game(self):

        while True:
            self._check_events()
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

    def _check_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event.key)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event.key)

            if self.controller.is_initialized:

                if event.type == pygame.JOYBUTTONDOWN:
                    self._check_controller_down()
                elif event.type == pygame.JOYBUTTONUP:
                    self._check_controller_up()
                elif event.type == pygame.JOYHATMOTION:
                    self._check_hat_motion()




    def _check_controller_up(self):
        pass

    def _check_hat_motion(self):
        hat_motion = self.controller.get_hat()
        print(hat_motion[0])

        if hat_motion[0] == (0, 0):
            self._check_keyup_events(self.hat_motion[1])
        else:
            self._check_keydown_events(hat_motion[1])

        self.hat_motion = hat_motion

    def _check_controller_down(self):
        if self.controller.get_button('a'):
            self._check_keydown_events(buttons_to_keys['a'])
        elif self.controller.get_button('b'):
            self._check_keydown_events(buttons_to_keys['b'])

    def _check_keydown_events(self, key):
        # TODO change these to accept ints

        if key is None:
            pass

        if key == pygame.K_RIGHT:
            self.player.change_state(pygame.K_RIGHT, True)
        elif key == pygame.K_LEFT:
            self.player.change_state(pygame.K_LEFT, True)
        elif key == pygame.K_SPACE:
            self.player.change_state(pygame.K_SPACE, True)
        elif key == pygame.K_a:
            self.player.change_state(pygame.K_a, True)

    def _check_keyup_events(self, key):
        if key == pygame.K_RIGHT:
            self.player.change_state(pygame.K_RIGHT, False)
        elif key == pygame.K_LEFT:
            self.player.change_state(pygame.K_LEFT, False)

        return

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color('black'))
        return fps_text


if __name__ == '__main__':
    ai = Game()
    ai.run_game()
