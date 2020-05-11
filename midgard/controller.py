import pygame

buttons = {
    'a': 0,
    'b': 1,
    'x': 2,
    'y': 3,
    'start': 7
}

buttons_to_keys = {
    
    'a': pygame.K_SPACE,
    'b': pygame.K_a
}

hat_motions = {
    (1, 0): pygame.K_RIGHT,
    (-1, 0): pygame.K_LEFT,
    (0, 1): pygame.K_UP,
    (0, -1): pygame.K_DOWN,
    (0, 0): pygame.K_PLUS,
    (1, 1): None,
    (-1, 1): None,
    (1, -1): None,
    (-1, -1): None
}


class Controller:

    def __init__(self):
        self.is_initialized = False

    def __destroy__(self):
        pygame.joystick.quit()
        self.is_initialized = False

    def get_button(self, name_of_button):
        return self.remote_control.get_button(buttons[name_of_button])

    def get_hat(self):
        hat = self.remote_control.get_hat(0)

        return hat, hat_motions[hat]

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
       