import pygame
import numpy as np


class VectorSprite:
    def __init__(self, r, freq, start):
        self.r = r
        self.freq = freq
        self.teta = 90
        self.color = (100, 100, 100)
        self.start = start
        self.end = (0, 0)

    def calc_end_point(self):
        self.end = (self.start[0] + self.r * np.cos(np.pi * self.teta / 180),
                    self.start[1] - self.r * np.sin(np.pi * self.teta / 180))
        return self.end

    def get_round_end_point(self, max_x, max_y):
        return np.rint(self.end[0]), np.rint(self.end[1])

    def draw_on_surface(self, surface):
        pygame.draw.line(surface, self.color, self.start, self.end, width=2)

    def step(self):
        self.teta += self.freq

    @staticmethod
    def get_random_vector(max_r, min_freq, max_freq, middle_point):
        return VectorSprite(np.random.uniform(0, max_r), np.random.uniform(min_freq, max_freq), middle_point)
