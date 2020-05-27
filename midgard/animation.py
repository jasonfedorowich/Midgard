import pygame

from midgard.timer import Timer


class Animation:

    def __init__(self, animation_dictionary, refresh_rate):
        self.dictionary = animation_dictionary
        self.current_frame = 0
        self.last_frame_updated = 0
        self.time_of_last_update = 0
        self.current_frames = None
        self.animation_refresh_rate = refresh_rate
        self.clock = Timer()
        self.frame_name = None

    def set_frames(self, frame_name):
        self.frame_name = frame_name
        self.clock.tick()
        completed_cycle = False
        if self.dictionary[frame_name] != self.current_frames or self.current_frames is None:
            self.current_frames = self.dictionary[frame_name]
            self.current_frame = 0
            self.clock.reset()
        else:

            if self.clock.get_time() >= self.animation_refresh_rate:
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

    def run_current_frames(self):
        return self.set_frames(self.frame_name)
