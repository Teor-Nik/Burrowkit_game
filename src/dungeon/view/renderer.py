"""Module for rendering the game window using Pygame."""

from enum import Enum

import pygame

from dungeon.model.entities import EntityType
from dungeon.model.items import ItemTypes
from dungeon.model.level import Tile


class Panel(Enum):
    """List of window panels."""

    MAP = 0
    PLAYER_STATS = 1
    KIT_STATS = 2
    PROGRESS = 3


WINDOW_BKGND_COLOUR = (144, 209, 197)  # Green map background 90D1C5
PROGRESS_WINDOW_BKGND_COLOUR = (165, 144, 209)
W_HEIGHT = 1000  # larger to allow for buttons
W_WIDTH = 1500  # larger to allow for buttons
MAP_SIZE = 800
# Calculate half dimensions
HALF_WIDTH = W_WIDTH // 2
HALF_HEIGHT = W_HEIGHT // 2
PANEL_WIDTH = 200
PANEL_HEIGHT = 200
BLOCK_SMALL = 20
OBJECT_SMALL = 12

# Type alias for RGB tuple
RGB = tuple[int, int, int]

COLOUR_MAP: dict[Tile, RGB] = {
    Tile.EMPTY: (30, 117, 82),  # Dark green background
    Tile.WALL: (143, 132, 121),  # mossy brown
    Tile.STAIR: (152, 227, 185),  # green down stairs
    Tile.GOAL: (227, 218, 159),  # light colour for exit
    Tile.ENTRANCE: (179, 171, 171),  # blue for entry
}

COLOUR_ENTITIES: dict[EntityType, RGB] = {
    EntityType.PLAYER: (144, 156, 209),  # Blue Player
    EntityType.RAT: (131, 129, 133),  # Red monster
    EntityType.OOZE: (98, 219, 222),  # Red monster
    EntityType.GOBLIN: (222, 125, 98),  # Red monster
    EntityType.GOBLIN_BRUTE: (214, 109, 109),  # Red monster
    EntityType.GOBLIN_KING: (184, 39, 39),  # Red monster
    EntityType.KIT: (209, 165, 144),  # Kit brown (fawn)
}

COLOUR_ITEMS: dict[ItemTypes, RGB] = {
    ItemTypes.GREEN_BERRY: (40, 77, 26),  # dark yelloy/green
    ItemTypes.YELLOW_BERRY: (77, 76, 26),  # dark yellow
    ItemTypes.BREAD: (77, 63, 26),  # dark yellow/orange
    ItemTypes.POITION: (26, 77, 57),  # dark green
    ItemTypes.RED_BERRY: (77, 26, 26),  # dark red
    ItemTypes.TRAP: (68, 26, 77),  # dark purple
}


class GameRenderer:
    """Class responsible for rendering the game window."""

    def __init__(self) -> None:
        """Initialise the game window."""
        self.panel = Panel
        # Initialize Pygame
        pygame.init()
        # Set up the game window
        self.screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
        pygame.display.set_caption("Burrowkit Game")
        self.header_font = pygame.font.SysFont(None, 45)
        self.detail_font = pygame.font.SysFont(None, 20)
        self.draw_quadrants()

    # Function to draw the 4 quadrants
    def draw_quadrants(self) -> None:
        """Divide the window up into four quadrants for the game."""
        self.screen.fill(WINDOW_BKGND_COLOUR)  # Clear screen

        # Top-left quadrant for MAP
        pygame.draw.rect(
            self.screen,
            (30, 117, 82),
            (0, 0, MAP_SIZE // 2, MAP_SIZE // 2)
        )
        self.map_section = self.screen.subsurface((0, 0, MAP_SIZE // 2, MAP_SIZE // 2))

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
        for row_position, row_tiles in enumerate(level_map):
            for col_position, tile in enumerate(row_tiles):
                colour = COLOUR_MAP[tile]
                row = row_position * BLOCK_SMALL
                col = col_position * BLOCK_SMALL
                self.render_map_cell(colour, row, col, BLOCK_SMALL)

    def render_panel(self, panel: Panel, label: str, details: str) -> None:
        """Render the panel based on the Panel type and information."""
        coords = (0, 0)
        if panel == Panel.PLAYER_STATS:
            coords = self.determine_quadrant_corner(self.player_section)
        if panel == Panel.KIT_STATS:
            coords = self.determine_quadrant_corner(self.kit_section)
        if panel == Panel.PROGRESS:
            coords = self.determine_quadrant_corner(self.overall_section)
        text_surface = self.header_font.render(label, True, (94, 83, 86))
        self.screen.blit(
            text_surface, (coords[0] + 10, coords[1] + 10, PANEL_WIDTH, PANEL_HEIGHT)
        )

        text_surface = self.detail_font.render(details, True, (94, 83, 86))
        self.screen.blit(
            text_surface, (coords[0] + 10, coords[1] + 40, PANEL_WIDTH, PANEL_HEIGHT)
        )

    def draw_entity(
        self, type: EntityType, coords: tuple[int, int]
    ) -> None:
        """Draw the player on the level."""
        row_num = coords[0] * BLOCK_SMALL
        col_num = coords[1] * BLOCK_SMALL
        colour = COLOUR_ENTITIES[type]

        half_diff = (BLOCK_SMALL - OBJECT_SMALL) / 2
        self.render_map_cell(
            colour,
            round(row_num + half_diff),
            round(col_num + half_diff),
            OBJECT_SMALL,
        )

    def draw_item(self, type: ItemTypes, coords: tuple[int, int]) -> None:
        """Draw the Items on the level."""
        row_num = coords[0] * BLOCK_SMALL
        col_num = coords[1] * BLOCK_SMALL
        colour = COLOUR_ITEMS[type]
        half_diff = (BLOCK_SMALL - OBJECT_SMALL) / 2
        self.render_map_cell(
                colour,
                round(row_num + half_diff),
                round(col_num + half_diff),
                OBJECT_SMALL,
        )

    def render_map_cell(
        self, colour: tuple[int, int, int], row: int, col: int, size: int
    ) -> None:
        """Render a single cell based on the cell type passed in."""
        pygame.draw.rect(self.screen, colour, (col, row, size, size))

    @staticmethod
    def show_error(message: str) -> None:
        """Display error message to log."""
        print(f"Error: {message}")

    @staticmethod
    def show_log(message: str) -> None:
        """Display note message to log."""
        print(f"Note: {message}")
