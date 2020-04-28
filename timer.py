import pygame


class Timer:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.time_from_ticks = 0

    def tick(self):
        self.clock.tick()
        self.time_from_ticks += self.clock.get_time()

    def get_time(self):
        return self.time_from_ticks

    def reset(self):
        self.time_from_ticks = 0



