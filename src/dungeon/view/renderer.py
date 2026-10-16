"""Module for rendering the game window using Pygame."""

import pygame

from dungeon.model.level import Tile

WINDOW_BKGND_COLOUR = (82, 65, 64)  # Dark brown background
WINDOW_HEIGHT = 600  # slightly larger to allow for buttons
WINDOW_WIDTH = 600
BLOCK_SMALL = 20

# Type alias for RGB tuple
RGB = tuple[int, int, int]


COLOUR_MAP: dict[Tile, RGB] = {
    Tile.EMPTY: (30, 117, 82),  # Dark green background
    Tile.WALL: (143, 132, 121),  # mossy brown
    Tile.STAIR: (152, 227, 185),  # green down stairs
    Tile.GOAL: (230, 227, 197),  # light colour for exit
    Tile.ENTRANCE: (165, 152, 227),  # blue for entry
}


class GameRenderer:
    """Class responsible for rendering the game window."""

    def __init__(self) -> None:
        """Initialise the game window."""
        # Initialize Pygame
        pygame.init()
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.block_size = BLOCK_SMALL

        # Set up the game window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Burrowkit Game: Dungeon Model")

        # Fill the background color
        self.screen.fill(WINDOW_BKGND_COLOUR)

    def reload_game_window(self) -> None:
        """Reload the game window."""
        pygame.display.flip()  # Update the display

    def draw_level(self, level_map: list[list[Tile]]) -> None:
        """Draw each level onto the map on the screen."""
        temp_x = 100  # store the initial x to reset after each row
        x = 100
        y = 50
        for row in level_map:
            for tile in row:
                colour = COLOUR_MAP.get(tile, (0, 0, 0))
                pygame.draw.rect(
                    self.screen, colour, (x, y, self.block_size, self.block_size)
                )
                x += self.block_size
            y += self.block_size
            x = temp_x  # reset x after each row
