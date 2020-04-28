import pygame

from constants import get_time_millis
from timer import Timer


class Animation:

    def __init__(self, animation_dictionary):
        self.dictionary = animation_dictionary
        self.current_frame = 0
        self.last_frame_updated = 0
        self.time_of_last_update = 0
        self.current_frames = None
        self.animation_refresh_rate = 100
        self.clock = Timer()

    def set_frames(self, frame_name):
        self.clock.tick()
        completed_cycle = False
        if self.dictionary[frame_name] != self.current_frames or self.current_frames is None:
            self.current_frames = self.dictionary[frame_name]
            self.current_frame = 0
            self.clock.reset()
        else:

            if self.clock.get_time() >= 100:
                self.current_frame += 1
                self.clock.reset()

        if self.current_frame >= len(self.current_frames):
            self.current_frame = 0
            self.clock.reset()
            completed_cycle = True

        return completed_cycle

    def current_animation_with_scale(self, scale):
        image = self.current_frames[self.current_frame]
        rect = image.get_rect()

        scaled_image = pygame.transform.scale(image,
                                              (int(rect.width * scale),
                                               int(rect.height * scale)))
        return scaled_image
