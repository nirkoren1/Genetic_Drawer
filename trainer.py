import threading
import multiprocessing
import numpy as np
from drawing_genome import Genome, cross_over, mutate
from main import simulate

population_size = 100
target_drawing = []
drawing = []
mutation_rate = 0.1
crossover_rate = 0.5
elitism = True
elitism_group_size = 8
tournament_group_size = 8
generation_num = 0
current_generation = []
prev_generation = []
max_c = 100
window_x_size = 1000
window_y_size = 1000
num_of_vectors = 7


def create_gen_zero():
    global current_generation
    for _ in range(population_size):
        current_generation.append([Genome.random_genome(max_c, num_of_vectors, window_x_size, window_y_size), - np.inf])


def eval_single_genome(idx, genome):
    current_generation[idx][1] = genome[0].fitness_eval(target_drawing)


def evaluate_generation():
    for genome in current_generation:
        genome[1] = genome[0].fitness_eval(target_drawing)


def tournament_selection():
    tournament_group_idx = np.random.choice(len(prev_generation), tournament_group_size, replace=False)
    tournament_group = [prev_generation[idx] for idx in tournament_group_idx]
    sorted_group = sorted(tournament_group, key=lambda x: x[1])
    return sorted_group[-1][0]


def create_new_gen():
    global prev_generation, current_generation
    prev_generation = current_generation.copy()
    current_generation = []
    if elitism:
        sorted_gen = list(reversed(sorted(prev_generation, key=lambda x: x[1])))
        for i in range(elitism_group_size):
            elite_genome = sorted_gen[i]
            current_generation.append(elite_genome)
            mutated_elite = mutate(elite_genome[0], max_c)
            current_generation.append([mutated_elite, -np.inf])
    while len(current_generation) < population_size:
        rand_float = np.random.random()
        if rand_float < crossover_rate:
            new_genome = cross_over(tournament_selection(), tournament_selection())
            if np.random.random() < mutation_rate:
                new_genome = mutate(new_genome, max_c)
            current_generation.append([new_genome, - np.inf])
        else:
            current_generation.append([Genome.random_genome(max_c, num_of_vectors, window_x_size, window_y_size),
                                       -np.inf])


if __name__ == '__main__':
    for i in range(-300, 300, 1):
        try:
            int(pow(650 * 1e12 - pow(i, 6), 1 / 6))
        except Exception as e:
            pass
        else:
            drawing.append(
                ((window_x_size // 2) + i, int((window_y_size // 2) + pow(650 * 1e12 - pow(i, 6), 1 / 6))))
            drawing.append(
                ((window_x_size // 2) + i, int((window_y_size // 2) - pow(650 * 1e12 - pow(i, 6), 1 / 6))))

    # approx_num_of_target_points = 50
    # prob = approx_num_of_target_points / len(drawing)
    # for point in drawing:
    #     if np.random.random() < prob:
    #         target_drawing.append(point)
    # target_drawing = np.array(target_drawing)
    # num_of_vectors = len(target_drawing)
    target_drawing = np.array(drawing)

    create_gen_zero()
    num_of_gens = 1000
    for i in range(num_of_gens):
        evaluate_generation()
        best = max(current_generation, key=lambda x: x[1])
        print(best[1])
        print(f"{i + 1}/{num_of_gens}")
        if i % 10 == 0:
            simulate(best[0], [window_x_size, window_y_size], target_drawing)
        create_new_gen()
