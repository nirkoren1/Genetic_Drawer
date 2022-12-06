from vector_sprite import VectorSprite
import numpy as np
from scipy.spatial.distance import directed_hausdorff


class Genome:
    def __init__(self, window_x_size, window_y_size, dna: list, fitness=-np.inf):
        self.fitness = fitness
        self.window_x_size = window_x_size
        self.window_y_size = window_y_size
        self.dna = dna
        self.vectors_sprites = [VectorSprite(dna[i], ((-1) ** (i + 1)) * ((i + 1) // 2)) for i in range(len(dna))]
        self.drawing = []

    def fitness_eval(self, target_drawing, num_of_iterations=2000):
        self.drawing = []
        precision = 1 / num_of_iterations
        teta = 0
        for i in range(num_of_iterations):
            self.step(teta)
            teta += precision
        drawing = np.array(list(self.drawing))
        self.fitness = - max(directed_hausdorff(drawing, target_drawing)[0], directed_hausdorff(target_drawing, drawing)[0])
        return self.fitness

    def step(self, teta):
        end_point = complex(self.window_x_size // 2, self.window_y_size // 2)
        for vec in self.vectors_sprites:
            end_point += vec.calc_end_point(teta)
        self.drawing.append([self.window_x_size // 2 + end_point.real, self.window_y_size // 2 + end_point.imag])

    def draw_on_surface(self, surface, teta):
        start = complex(self.window_x_size // 2, self.window_y_size // 2)
        for vec in self.vectors_sprites:
            end = start + vec.calc_end_point(teta)
            vec.draw_on_surface(start, end, surface)
            start = end

    @staticmethod
    def random_genome(max_c, num_of_vectors, window_x_size, window_y_size):
        return Genome(window_x_size, window_y_size,
                      [complex(np.random.random() * max_c, np.random.random() * max_c) for _ in range(num_of_vectors)])


def mutate(genome: Genome, max_c):
    dna = genome.dna.copy()
    dna[np.random.randint(0, len(dna))] = complex(np.random.random() * max_c, np.random.random() * max_c)
    return Genome(genome.window_x_size, genome.window_y_size, dna)


def cross_over(genome1: Genome, genome2: Genome):
    rand_idx_slice = np.random.randint(1, len(genome1.dna) - 1)
    dna1 = genome1.dna.copy()
    dna2 = genome2.dna.copy()
    new_dna = dna1[:rand_idx_slice] + dna2[rand_idx_slice:]
    return Genome(genome1.window_x_size, genome1.window_y_size, new_dna)


if __name__ == '__main__':
    l = [1, 2, 3,4 ]
    print(l[:2])