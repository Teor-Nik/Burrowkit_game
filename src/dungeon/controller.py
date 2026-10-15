"""Burrowkit Game: Dungeon Controller."""

import pygame

from dungeon.model import level
from dungeon.view import renderer


class GameController:
    """Class responsible for controlling the game flow."""

    def __init__(self) -> None:
        """Initialize the game controller."""
        # Create a GameRenderer instance
        self.game_renderer = renderer.GameRenderer()
        self.start_game()

    def start_game(self) -> None:
        """Start the game."""
        # Main game loop
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Create a GameLevel instance with the first level map
            self.current_level = level.GameLevel().level_one_map
            dungeon_map = self.current_level
            # dungeon_map = level.GameLevel.check_level(self.current_level, "1") -- JAVA
            # block = level.GameLevel.get_block_size(self.current_level) -- JAVA
            self.game_renderer.draw_level(dungeon_map)
            # Render the game window
            self.game_renderer.reload_game_window()

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
