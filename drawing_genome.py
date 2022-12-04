from vector_sprite import VectorSprite
import numpy as np


class Genome:
    def __init__(self, window_x_size, window_y_size, vectors: list, drawing: set, fitness=-np.inf):
        self.fitness = fitness
        self.drawing = []
        self.vectors = vectors
        self.window_x_size = window_x_size
        self.window_y_size = window_y_size

    def mutate(self, max_r, min_freq, max_freq):
        rand_vec_idx = np.random.randint(0, len(self.vectors))
        self.vectors[rand_vec_idx] = VectorSprite.get_random_vector(max_r, min_freq, max_freq,
                                                                    (self.window_x_size // 2,
                                                                     self.window_y_size // 2))
        return self

    def fitness_eval(self, target_drawing):
        for vec in self.vectors:
            vec.teta = 90
        for i in range(2000):
            self.step()
        nrows, ncols = target_drawing.shape
        dtype = {'names': ['f{}'.format(i) for i in range(ncols)],
                 'formats': ncols * [target_drawing.dtype]}
        drawing = np.array(list(self.drawing))
        self.fitness = len(np.intersect1d(target_drawing.view(dtype), drawing.view(dtype))) / len(np.union1d(target_drawing.view(dtype), drawing.view(dtype)))
        return self.fitness

    def step(self):
        prev = self.vectors[0].start
        for vec in self.vectors:
            vec.start = prev
            prev = vec.calc_end_point()
            vec.step()
        self.drawing.append(self.vectors[-1].get_round_end_point(self.window_x_size, self.window_y_size))

    def draw_on_surface(self, surface):
        for vec in self.vectors:
            vec.draw_on_surface(surface)

    @staticmethod
    def random_genome(max_r, min_freq, max_freq, num_of_vectors, window_x_size, window_y_size):
        return Genome(window_x_size, window_y_size,
                      [VectorSprite.get_random_vector(max_r, min_freq, max_freq,
                                                      (window_x_size // 2, window_y_size // 2))
                       for _ in range(num_of_vectors)],
                      set())


def cross_over(genome1: Genome, genome2: Genome):
    rand_idx_slice = np.random.randint(1, len(genome1.vectors) - 1)
    new_vectors = genome1.vectors[:rand_idx_slice].copy() + genome2.vectors[rand_idx_slice:].copy()
    return Genome(genome1.window_x_size, genome1.window_y_size, new_vectors, set())
