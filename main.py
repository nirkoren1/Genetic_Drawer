import pygame
from vector_sprite import VectorSprite
from drawing_genome import Genome


def simulate(genome: Genome, window_size, target_drawing):
    drawing = set()

    pygame.init()

    drawing_screen = pygame.Surface(window_size)

    for point in target_drawing:
        pygame.draw.circle(drawing_screen, (0, 200, 0), point, 1)
    screen = pygame.display.set_mode(window_size)

    running = True
    counter = 0
    teta = 0
    num_of_iterations = 5000
    precision = 1 / num_of_iterations
    while running:
        counter += 1
        if counter == num_of_iterations:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(drawing_screen, (0, 0))
        genome.draw_on_surface(screen, teta)
        pygame.draw.circle(drawing_screen, (200, 0, 0), genome.step(teta), 1)
        teta += precision

        pygame.display.flip()

    # Quit the program
    pygame.quit()


if __name__ == '__main__':
    window_size = [500, 500]
    simulate(Genome.random_genome(60, 11, window_size[0], window_size[1]), window_size, set())
