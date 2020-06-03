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


class Timeout:

    def __init__(self, timeout_in_millis):
        self.timer = Timer()
        self.timeout_in_mills = timeout_in_millis

    def has_timed_out(self):
        self.timer.tick()
        if self.timer.get_time() >= self.timeout_in_mills:
            return True
        return False


class QuietTimeout:

    def __init__(self, timeout_in_millis, object):
        self.timer = Timeout(timeout_in_millis)
        self.object = object

    def tick(self):
        if self.timer.has_timed_out():
            self.object.remove_timeout()
        else:
            pass






