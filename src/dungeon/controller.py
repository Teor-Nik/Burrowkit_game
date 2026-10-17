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
        self.current_level = level.GameLevel(1)
        self.start_game()

    def start_game(self) -> None:
        """Start the game."""
        # Main game loop
        running = True
        clock = pygame.time.Clock()
        level_loaded = False
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if not level_loaded:
                self.game_renderer.draw_level(self.current_level.check_level())
                level_loaded = True

            # if self.current_level.stairs_reached():
            #     level_loaded = False

            # Render the game window
            self.game_renderer.reload_game_window()
            # if self.current_level.is_walkable(2,2):
            #     print("true")
            # else:
            #     print("NOT true")

        # Quit Pygame
        pygame.quit()
