"""Module for rendering the game window using Pygame."""

from enum import Enum

import pygame

from dungeon.model.entities import EntityType
from dungeon.model.level import Tile


class Panel(Enum):
    """List of window panels."""

    MAP = 0
    PLAYER_STATS = 1
    KIT_STATS = 2
    PROGRESS = 3


WINDOW_BKGND_COLOUR = (144, 209, 197)  # Green map background 90D1C5
PROGRESS_WINDOW_BKGND_COLOUR = (165, 144, 209)
W_HEIGHT = 800  # larger to allow for buttons
W_WIDTH = 800  # larger to allow for buttons
# Calculate half dimensions
HALF_WIDTH = W_WIDTH // 2
HALF_HEIGHT = W_HEIGHT // 2
PANEL_WIDTH = 200
PANEL_HEIGHT = 200
BLOCK_SMALL = 20
EntityType_SMALL = 15

# Type alias for RGB tuple
RGB = tuple[int, int, int]

DRAW_COORDINATES = tuple([int, int])

COLOUR_MAP: dict[Tile, RGB] = {
    Tile.EMPTY: (30, 117, 82),  # Dark green background
    Tile.WALL: (143, 132, 121),  # mossy brown
    Tile.STAIR: (152, 227, 185),  # green down stairs
    Tile.GOAL: (227, 218, 159),  # light colour for exit
    Tile.ENTRANCE: (179, 171, 171),  # blue for entry
}

COLOUR_ENTITIES: dict[EntityType, RGB] = {
    EntityType.PLAYER: (144, 156, 209),  # Blue Player
    EntityType.MONSTER: (179, 20, 20),  # Red monster
    EntityType.KIT: (209, 165, 144),  # Kit brown (fawn)
}


class GameRenderer:
    """Class responsible for rendering the game window."""

    def __init__(self) -> None:
        """Initialise the game window."""
        # Initialize Pygame
        pygame.init()
        self.width = W_WIDTH
        self.height = W_HEIGHT
        self.block_size = BLOCK_SMALL
        self.EntityType_size = EntityType_SMALL
        self.panel = Panel
        # Set up the game window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Burrowkit Game: Dungeon Model")
        self.draw_quadrants()

    # Function to draw the 4 quadrants
    def draw_quadrants(self) -> None:
        """Divide the window up into four quadrants for the game."""
        self.screen.fill(WINDOW_BKGND_COLOUR)  # Clear screen

        # Top-left quadrant for MAP
        pygame.draw.rect(self.screen, (30, 117, 82), (0, 0, HALF_WIDTH, HALF_HEIGHT))
        self.map_section = self.screen.subsurface((0, 0, HALF_WIDTH, HALF_HEIGHT))

        # Top-right quadrant for Player section
        pygame.draw.rect(
            self.screen, (182, 205, 240), (HALF_WIDTH, 0, HALF_WIDTH, HALF_HEIGHT)
        )
        self.player_section = self.screen.subsurface(
            (HALF_WIDTH, 0, HALF_WIDTH, HALF_HEIGHT)
        )

        # Bottom-left quadrant for kit section
        pygame.draw.rect(
            self.screen, (224, 216, 200), (0, HALF_HEIGHT, HALF_WIDTH, HALF_HEIGHT)
        )
        self.kit_section = self.screen.subsurface(
            (0, HALF_HEIGHT, HALF_WIDTH, HALF_HEIGHT)
        )

        # Bottom-right quadrant for Overall Game Stats
        pygame.draw.rect(
            self.screen,
            (200, 224, 216),
            (HALF_WIDTH, HALF_HEIGHT, HALF_WIDTH, HALF_HEIGHT),
        )
        self.overall_section = self.screen.subsurface(
            (HALF_WIDTH, HALF_HEIGHT, HALF_WIDTH, HALF_HEIGHT)
        )

        # Optional: draw dividing lines
        pygame.draw.line(
            self.screen, (173, 161, 146), (HALF_WIDTH, 0), (HALF_WIDTH, W_HEIGHT), 5
        )
        pygame.draw.line(
            self.screen, (173, 161, 146), (0, HALF_HEIGHT), (W_WIDTH, HALF_HEIGHT), 5
        )

    # Function to get top-left point for each quadrant in screen coordinates
    def determine_quadrant_corner(self, type: pygame.Surface) -> tuple[int, int]:
        """Determine where the top left corner of the panel is."""
        if type == self.map_section:
            return (0, 0)  # Top-left quadrant
        if type == self.player_section:
            return (HALF_WIDTH, 0)  # Top-right quadrant
        if type == self.kit_section:
            return (0, HALF_HEIGHT)  # Bottom-left quadrant
        if type == self.overall_section:
            return (HALF_WIDTH, HALF_HEIGHT)  # Bottom-right quadrant
        return (0, 0)

    def reload_game_window(self) -> None:
        """Reload the game window."""
        pygame.display.flip()  # Update the display

    def draw_level(self, level_map: list[list[Tile]]) -> None:
        """Draw each level onto the map on the screen."""
        coords = self.determine_quadrant_corner(self.map_section)
        row = coords[0]
        col = coords[1]
        temp_col = 0  # store the initial x to reset after each row
        for row_tiles in level_map:
            for col_tile in row_tiles:
                colour = COLOUR_MAP.get(col_tile, (143, 132, 121))
                self.render_map_cell(colour, row, col, self.block_size)
                col += self.block_size
            row += self.block_size

            col = temp_col  # reset x after each row

    def render_panel(self, panel: Panel, label: str, details: str) -> None:
        """Render the panel based on the Panel type and information."""
        coords = (0, 0)
        if panel == Panel.PLAYER_STATS:
            coords = self.determine_quadrant_corner(self.player_section)
        if panel == Panel.KIT_STATS:
            coords = self.determine_quadrant_corner(self.kit_section)
        if panel == Panel.PROGRESS:
            coords = self.determine_quadrant_corner(self.overall_section)
        font = pygame.font.SysFont(None, 45)
        text_surface = font.render(label, True, (94, 83, 86))
        self.screen.blit(
            text_surface, (coords[0] + 10, coords[1] + 10, PANEL_WIDTH, PANEL_HEIGHT)
        )
        font = pygame.font.SysFont(None, 20)
        text_surface = font.render(details, True, (94, 83, 86))
        self.screen.blit(
            text_surface, (coords[0] + 10, coords[1] + 40, PANEL_WIDTH, PANEL_HEIGHT)
        )

    def draw_entity_type(self, type: EntityType, coords: tuple[int, int]) -> None:
        """Draw the player on the level."""
        row_num = coords[0] * self.block_size
        col_num = coords[1] * self.block_size
        row = round(row_num / 10) * 10
        col = round(col_num / 10) * 10
        colour = COLOUR_ENTITIES.get(type, (0, 0, 121))
        self.render_map_cell(colour, row, col, self.EntityType_size)

    def render_map_cell(
        self, colour: tuple[int, int, int], row: int, col: int, size: int
    ) -> None:
        """Render a single cell based on the cell type passed in."""
        pygame.draw.rect(self.screen, colour, (col, row, size, size))
