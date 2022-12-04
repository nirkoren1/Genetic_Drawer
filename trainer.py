import threading
import numpy as np
from drawing_genome import Genome, cross_over
from main import simulate

population_size = 100
target_drawing = []
mutation_rate = 0.2
crossover_rate = 0.5
elitism = True
elitism_group_size = 8
tournament_group_size = 8
generation_num = 0
current_generation = []
prev_generation = []
max_r = 60
min_freq = -1
max_freq = 1
window_x_size = 1000
window_y_size = 1000
num_of_vectors = 25


def create_gen_zero():
    global current_generation
    for i in range(population_size):
        current_generation.append([Genome.random_genome(max_r, min_freq, max_freq, num_of_vectors, window_x_size,
                                                        window_y_size), - np.inf])


def eval_single_genome(idx, genome):
    current_generation[idx][1] = genome[0].fitness_eval(target_drawing)


def evaluate_generation():
    # threads = []
    # for idx, genome in enumerate(current_generation):
    #     t = threading.Thread(target=eval_single_genome, args=(idx, genome))
    #     t.start()
    #     threads.append(t)
    # for i in range(len(threads)):
    #     threads[i].join()
    for idx, genome in enumerate(current_generation):
        current_generation[idx][1] = genome[0].fitness_eval(target_drawing)


def tournament_selection():
    tournament_group_idx = np.random.choice(len(prev_generation), tournament_group_size, replace=False)
    tournament_group = [prev_generation[idx] for idx in tournament_group_idx]
    sorted_group = sorted(tournament_group, key=lambda x: x[1])
    return sorted_group[-1][0], sorted_group[-2][0]


def create_new_gen():
    global prev_generation, current_generation
    prev_generation = current_generation.copy()
    current_generation = []
    if elitism:
        sorted_gen = list(reversed(sorted(prev_generation, key=lambda x: x[1])))
        for i in range(elitism_group_size):
            elite_genome = sorted_gen[i]
            current_generation.append(elite_genome.copy())
            current_generation.append([(elite_genome.copy())[0].mutate(max_r, min_freq, max_freq), -np.inf])
            print(elite_genome)
    while len(current_generation) < population_size:
        rand_float = np.random.random()
        if rand_float < crossover_rate:
            genome1, genome2 = tournament_selection()
            new_genome = cross_over(genome1, genome2)
            if np.random.random() < mutation_rate:
                new_genome = new_genome.mutate(max_r, min_freq, max_freq)
            current_generation.append([new_genome, - np.inf])
        else:
            current_generation.append([Genome.random_genome(max_r, min_freq, max_freq, num_of_vectors, window_x_size,
                                                            window_y_size), - np.inf])


if __name__ == '__main__':
    for i in range(-300, 300, 1):
        try:
            int(pow(650 * 1e12 - pow(i, 6), 1 / 6))
        except Exception as e:
            pass
        else:
            target_drawing.append(
                ((window_x_size // 2) + i, int((window_y_size // 2) + pow(650 * 1e12 - pow(i, 6), 1 / 6))))
            target_drawing.append(
                ((window_x_size // 2) + i, int((window_y_size // 2) - pow(650 * 1e12 - pow(i, 6), 1 / 6))))
    target_drawing = np.array(target_drawing)
    create_gen_zero()
    num_of_gens = 100
    for i in range(num_of_gens):
        evaluate_generation()
        best = max(current_generation, key=lambda x: x[1])
        print(best[1])
        print(f"{i + 1}/{num_of_gens}")
        simulate(best[0].vectors, [window_x_size, window_y_size], target_drawing)
        create_new_gen()
