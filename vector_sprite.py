import pygame
import numpy as np


class VectorSprite:
    def __init__(self, c, freq):
        self.c = c
        self.freq = freq
        self.color = (100, 100, 100)

    def calc_end_point(self, teta):
        return self.c * pow(np.e, self.freq * 2 * np.pi * teta)

    def get_end_point_no_complex(self, teta):
        end_point = self.calc_end_point(teta)
        end_point_x = end_point.real
        end_point_y = end_point.imag
        return end_point_x, end_point_y

    def draw_on_surface(self, start, end, surface):
        pygame.draw.line(surface, self.color, (start.real, start.imag), (end.real, end.imag), width=2)
