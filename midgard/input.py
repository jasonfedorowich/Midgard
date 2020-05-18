import sys

import pygame

from midgard.player import IdleState, Direction, WalkState, MoveUpState, AttackState, JumpUpWalkState, \
    MovingAttackState, JumpDownWalkState, MoveDownState

buttons = {
    0: ('a', pygame.K_SPACE),
    1: ('b', pygame.K_a),
    2: ('x', None),
    3: ('y', None),
    7: ('start', pygame.K_RETURN)
}

buttons_to_keys = {
    
    'a': pygame.K_SPACE,
    'b': pygame.K_a
}

hat_motions = {
    (1, 0): ("right", pygame.K_RIGHT),
    (-1, 0): ("left", pygame.K_LEFT),
    (0, 1): ("up", pygame.K_UP),
    (0, -1): ("down", pygame.K_DOWN),
    (0, 0): ("middle", pygame.K_PLUS),
    (1, 1): ("up_right", pygame.K_RIGHT),
    (-1, 1): ("up_left", pygame.K_LEFT),
    (1, -1): ("down_right", pygame.K_RIGHT),
    (-1, -1): ("down_left", pygame.K_LEFT)
}


class InputManager:

    def __init__(self, game):
        self.controller = Controller()
        try:
            self.controller.init()
        except Exception:
            pass

        self.game = game
        self.player = game.player

    def process_events(self):
        if self.game.game_active:
            self._handle_player_events()
        else:
            self._check_events()
        self._check_events()

    def _check_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.controller.__destroy__()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event.key)

            elif event.type == pygame.KEYUP:
                self._handle_keyup_events(event.key)

            if self.controller.is_initialized:

                if event.type == pygame.JOYBUTTONDOWN:
                    self._handle_controller_down()
                elif event.type == pygame.JOYBUTTONUP:
                    self._handle_controller_up()
                elif event.type == pygame.JOYHATMOTION:
                    self._handle_hat_motion()
                elif event.type == pygame.JOYAXISMOTION:
                    self._handle_axis_motion()

    def _handle_controller_up(self):
        pass

    def _handle_hat_motion(self):
        hat_motion = self.controller.get_hat(0)

        if hat_motion[0][0] == 0:
            self._handle_keyup_events(self.hat_motion[1][1])
        else:
            self._handle_keydown_events(hat_motion[1][1])

        self.hat_motion = hat_motion

    def _handle_controller_down(self):

        down_buttons = self.controller.get_down_buttons()
        for button in down_buttons:
            self._handle_keydown_events(button[1])

    def _handle_keydown_events(self, key):
        self._change_player_state(key, True)

    def _handle_keyup_events(self, key):
        self._change_player_state(key, False)
        return

    def _handle_player_events(self):
        self._check_events()

    def _handle_axis_motion(self):
        axes = self.controller.get_axis()
        x_val = axes[0]
        y_val = axes[1]
        print(x_val)
        print('--------')

        if x_val > 0.1:
            self._change_player_state(pygame.K_RIGHT, True)
        elif x_val < -0.1:
            self._change_player_state(pygame.K_LEFT, True)

        elif 0 <= x_val <= 0.1:
            self._change_player_state(pygame.K_RIGHT, False)
        elif -0.1 <= x_val <= 0:
            self._change_player_state(pygame.K_LEFT, False)

    def _change_player_state(self, key, down):
        self.player.state.change_state(key, down)


class Controller:

    def __init__(self):
        self.is_initialized = False

    def init(self):
        # TODO need to effectively use state of controller
        pygame.joystick.init()
        if not pygame.joystick.get_init() or pygame.joystick.get_count() <= 0:
            raise Exception('Failed to init controller')

        self.remote_control = pygame.joystick.Joystick(0)
        self.remote_control.init()

        if not self.remote_control.get_init():
            raise Exception('Failed to init controller')

        self.is_initialized = True
        pass

    def __destroy__(self):
        pygame.joystick.quit()
        self.is_initialized = False

    def get_buttons_state(self):
        button_state = {True: [], False: []}
        for button_number in range(self.remote_control.get_numbuttons()):
            if button_number in buttons.keys():
                state = self.remote_control.get_button(button_number)
                arr = button_state[state]
                arr.append(buttons[button_number])

        return button_state

    def get_down_buttons(self):
        return self.get_buttons_state()[True]

    def get_up_buttons(self):
        return self.get_buttons_state()[False]

    def get_hat(self, number):
        hat = self.remote_control.get_hat(number)
        return hat, hat_motions[hat]

    def get_axis(self):
        axes = {}
        for axis in range(self.remote_control.get_numaxes()):
            axes[axis] = self.remote_control.get_axis(axis)

        return axes



