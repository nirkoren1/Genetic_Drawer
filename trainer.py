import numpy as np

from drawing_genome import Genome

population_size = 100
target_drawing = []
mutation_rate = 0.2
crossover_rate = 1
elitism = True
elitism_group_size = 8
generation_num = 0
current_generation = []
prev_generation = []
max_r = 60
min_freq = -1
max_freq = 1
window_x_size = 500
window_y_size = 500
num_of_vectors = 30


def create_gen_zero():
    for i in range(population_size):
        current_generation.append((Genome.random_genome(max_r, min_freq, max_freq, num_of_vectors, window_x_size,
                                                        window_y_size), - np.inf))


def evaluate_generation():
    for idx, genome in enumerate(current_generation):
        current_generation[idx][1] = genome.fitness_eval(target_drawing)

