from vector_sprite import VectorSprite
import numpy as np


class Genome:
    def __init__(self, window_x_size, window_y_size, vectors: list, drawing: set, fitness=0):
        self.fitness = 0
        self.drawing = drawing
        self.vectors = vectors
        self.window_x_size = window_x_size
        self.window_y_size = window_y_size

    def mutate(self):
        pass

    def fitness_eval(self, target_drawing: set):
        if self.fitness != 0:
            return self.fitness
        for i in range(len(target_drawing)):
            self.step()
        return -np.sum(np.logical_xor(target_drawing, self.drawing)) + np.sum(np.intersect1d(target_drawing, self.drawing))

    def step(self):
        prev = self.vectors[0].start
        for vec in self.vectors:
            vec.start = prev
            prev = vec.calc_end_point()
            vec.step()
        self.drawing.add(self.vectors[-1].get_round_end_point(self.window_x_size, self.window_y_size))

    @staticmethod
    def cross_over(genome1, genome2):
        pass

    @staticmethod
    def random_genome(max_r, min_freq, max_freq, num_of_vectors, window_x_size, window_y_size):
        return Genome(window_x_size, window_y_size,
                      [VectorSprite.get_random_vector(max_r, min_freq, max_freq, (window_x_size // 2, window_y_size // 2)) for _ in range(num_of_vectors)],
                      set())
