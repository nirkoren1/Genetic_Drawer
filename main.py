import pygame
from vector_sprite import VectorSprite


def simulate(vectors, window_size):
    sprites = vectors
    drawing = set()

    pygame.init()

    drawing_screen = pygame.Surface(window_size)
    screen = pygame.display.set_mode(window_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(drawing_screen, (0, 0))
        prev = sprites[0].start
        for sp in sprites:
            sp.start = prev
            prev = sp.calc_end_point()
            sp.draw_on_surface(screen)
            sp.step()

        pygame.draw.circle(drawing_screen, (200, 0, 0), sprites[-1].end, 1)
        # print(sprites[-1].get_round_end_point(500, 500))
        drawing.add(sprites[-1].get_round_end_point(window_size[0], window_size[1]))
        print('\r', len(drawing), end='')
        pygame.display.flip()

    # Quit the program
    pygame.quit()


if __name__ == '__main__':
    window_size = [500, 500]
    simulate([VectorSprite.get_random_vector(60,
                                             -0.3,
                                             0.3,
                                             (window_size[0] // 2, window_size[1] // 2)) for _ in range(20)],
             window_size)
