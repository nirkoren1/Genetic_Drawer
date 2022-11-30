import vector_sprite
import numpy as np


class Genome:
    def __init__(self, vectors: list, drawing: set, fitness=0):
        self.fitness = 0
        self.drawing = drawing
        self.vectors = vectors

    def mutate(self):
        pass

    def fitness_eval(self, target_drawing: set):
        pass

    @staticmethod
    def cross_over(genome1, genome2):
        pass

    @staticmethod
    def random_genome(min_r, max_r, min_freq, max_freq, middle_point):
        pass
