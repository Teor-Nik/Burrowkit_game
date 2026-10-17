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
        # Create a GameLevel instance with the first level map
        self.game_model = level.GameLevel(1)
        self.current_level = self.game_model.build_grid_initial(
            self.game_model.level_number
        )
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
                self.game_renderer.draw_level(self.game_model.level)
            # Render the game window
            self.game_renderer.reload_game_window()
            # if self.current_level.is_walkable(2,2):
            #     print("true")
            # else:
            #     print("NOT true")

        # Quit Pygame
        pygame.quit()
