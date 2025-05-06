import pygame
import time

def draw_card_animation(screen, card_image, start_pos, end_pos, duration=1):
    """
    Animates a card moving from start_pos to end_pos on the screen.

    Args:
        screen (pygame.Surface): The game screen to draw on.
        card_image (pygame.Surface): The image of the card to animate.
        start_pos (tuple): Starting position (x, y) of the card.
        end_pos (tuple): Ending position (x, y) of the card.
        duration (float): Duration of the animation in seconds.
    """
    clock = pygame.time.Clock()
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            break

        # Calculate the current position based on linear interpolation
        t = elapsed_time / duration
        current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * t

        # Redraw the screen
        screen.fill((0, 128, 0))  # Example background color (green for a table)
        screen.blit(card_image, (current_x, current_y))
        pygame.display.flip()

        clock.tick(60)  # Limit to 60 FPS

    # Ensure the card ends at the final position
    screen.blit(card_image, end_pos)
    pygame.display.flip()