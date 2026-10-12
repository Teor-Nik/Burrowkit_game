"""Module for rendering the game window using Pygame."""
import pygame


# render window
def render_game_window():
    """Initialise the game window."""
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Burrowkit Game")
    screen.fill((0, 0, 0))  # Fill the screen with black
    pygame.display.flip()  # Update the display
    return screen

def exit_game():
    """Exit the game and clean up resources."""
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
