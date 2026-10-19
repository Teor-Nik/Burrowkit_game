"""Module for rendering the game window using Pygame."""

import pygame

from dungeon.model.entities import Entity
from dungeon.model.level import Tile

WINDOW_BKGND_COLOUR = (82, 65, 64)  # Dark brown background
WINDOW_HEIGHT = 600  # slightly larger to allow for buttons
WINDOW_WIDTH = 600
BLOCK_SMALL = 20
ENTITY_SMALL = 15

# Type alias for RGB tuple
RGB = tuple[int, int, int]

DRAW_COORDINATES = tuple([int, int])

COLOUR_MAP: dict[Tile, RGB] = {
    Tile.EMPTY: (30, 117, 82),  # Dark green background
    Tile.WALL: (143, 132, 121),  # mossy brown
    Tile.STAIR: (152, 227, 185),  # green down stairs
    Tile.GOAL: (230, 227, 197),  # light colour for exit
    Tile.ENTRANCE: (165, 152, 227),  # blue for entry
}

COLOUR_ENTITIES: dict[Entity, RGB] = {
    Entity.PLAYER: (28, 28, 235),  # Bright Blue Player
    Entity.MONSTER: (179, 20, 20),  # Red monster
    Entity.KIT: (179, 151, 111),  # Kit brown (fawn)
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
        self.entity_size = ENTITY_SMALL

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
        temp_col = 0  # store the initial x to reset after each row
        row = 0
        col = 0
        for row_tiles in level_map:
            for col_tile in row_tiles:
                colour = COLOUR_MAP.get(col_tile, (143, 132, 121))
                self.render_cell(colour, row, col, self.block_size)
                col += self.block_size
            row += self.block_size

            col = temp_col  # reset x after each row

    def draw_entity(self, type: Entity, coords: tuple[int, int]) -> None:
        """Draw the player on the level."""
        row_num = coords[0] * self.block_size
        col_num = coords[1] * self.block_size
        row = round(row_num / 10) * 10
        col = round(col_num / 10) * 10
        colour = COLOUR_ENTITIES.get(type, (0, 0, 121))
        self.render_cell(colour, row, col, self.entity_size)

    def render_cell(
        self, colour: tuple[int, int, int], row: int, col: int, size: int
    ) -> None:
        """Render a single cell based on the cell type passed in."""
        pygame.draw.rect(self.screen, colour, (col, row, size, size))
