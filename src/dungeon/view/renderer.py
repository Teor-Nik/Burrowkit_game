"""Module for rendering the game window using Pygame."""

from enum import Enum
from pathlib import Path

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
W_HEIGHT = 800  # larger to allow for buttons
W_WIDTH = 1500  # larger to allow for buttons
MAP_SIZE = 1000
# Calculate half dimensions
HALF_WIDTH = W_WIDTH // 2
HALF_HEIGHT = W_HEIGHT // 2
PANEL_WIDTH = 400
PANEL_HEIGHT = 400
BLOCK_SMALL = 40
OBJECT_SMALL = 40
OBJECT_XS = 40
ITEM_SMALL = 13

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
    EntityType.RATBLACK: (131, 129, 133),  # Red monster
    EntityType.RATWHITE: (131, 129, 133),  # Red monster
    EntityType.RATGREY: (131, 129, 133),  # Red monster
    EntityType.RATBROWN: (131, 129, 133),  # Red monster
    EntityType.SLIMEBLUE: (98, 219, 222),  # Red monster
    EntityType.SLIMEGREEN: (98, 219, 222),  # Red monster
    EntityType.SLIMEORANGE: (98, 219, 222),  # Red monster
    EntityType.SLIMEPINK: (98, 219, 222),  # Red monster
    EntityType.SLIMEPURPLE: (98, 219, 222),  # Red monster
    EntityType.GOBLIN: (222, 125, 98),  # Red monster
    EntityType.GOBLIN_BRUTE: (214, 109, 109),  # Red monster
    EntityType.GOBLIN_KING: (184, 39, 39),  # Red monster
    EntityType.KIT: (209, 165, 144),  # Kit brown (fawn)
}

DIRECTORY:str = "src/dungeon/view/images"

OBJECT_IMAGE: dict[EntityType | ItemTypes | Tile, str] = {
    EntityType.PLAYER: "knight.png",
    EntityType.RATBLACK: "rat_black.png",
    EntityType.RATBROWN: "rat_brown.png",
    EntityType.RATGREY: "rat_grey.png",
    EntityType.RATWHITE: "rat_white.png",
    EntityType.SLIMEBLUE: "slime_blue.png",
    EntityType.SLIMEGREEN: "slime_green.png",
    EntityType.SLIMEORANGE: "slime_orange.png",
    EntityType.SLIMEPINK: "slime_pink.png",
    EntityType.SLIMEPURPLE: "slime_purple.png",
    EntityType.GOBLIN: "goblin_small.png",
    EntityType.GOBLIN_BRUTE: "goblin_brute.png",
    EntityType.GOBLIN_KING: "goblin_king.png",
    EntityType.KIT: "wolf_grey.png",
    ItemTypes.BLUE_BERRY: "berry_blue.png",
    ItemTypes.ORANGE_BERRY: "berry_orange.png",
    ItemTypes.BREAD: "bread.png",
    ItemTypes.YELLOW_POITION: "potion_yellow.png",
    ItemTypes.RED_BERRY: "berry_red.png",
    ItemTypes.PURPLE_POITION: "potion_purple.png",
    ItemTypes.CHEST: "treasure_chest.png",
    Tile.WALL: "rock_large.png",
    Tile.STAIR: "stairs.png",
    Tile.GOAL: "exit_door.png",
    Tile.ENTRANCE: "trap_door.png",
}

COLOUR_ITEMS: dict[ItemTypes, RGB] = {
    ItemTypes.BLUE_BERRY: (94, 168, 37),  # yelloy/green
    ItemTypes.ORANGE_BERRY: (209, 194, 29),  # gold yellow
    ItemTypes.BREAD: (209, 122, 29),  # brown/orange
    ItemTypes.YELLOW_POITION: (89, 189, 25),  # bright green
    ItemTypes.RED_BERRY: (189, 25, 47),  # red
    ItemTypes.PURPLE_POITION: (113, 33, 122),  # dark purple
    ItemTypes.CHEST: (94, 168, 37),
}

ASSET_DIR = Path(__file__).parent / "images"
SpriteKey = EntityType | ItemTypes | Tile

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
        self.images = self._load_images()


    @staticmethod
    def _load_images() -> dict[SpriteKey, pygame.Surface]:
        """Load and scale every sprite once; missing ones fall back to colours."""
        images: dict[SpriteKey, pygame.Surface] = {}
        for key, filename in OBJECT_IMAGE.items():
            try:
                image = pygame.image.load(ASSET_DIR / filename).convert_alpha()
            except (pygame.error, FileNotFoundError) as error:
                print("Could not load %s: %s", filename, error)
                continue
            images[key] = pygame.transform.scale(image, (BLOCK_SMALL, BLOCK_SMALL))
        return images

    # Function to draw the 4 quadrants
    def draw_quadrants(self) -> None:
        """Divide the window up into four quadrants for the game."""
        self.screen.fill(WINDOW_BKGND_COLOUR)  # Clear screen

        # Top-left quadrant for MAP
        map_rect = pygame.Rect(0, 0, 810, 800)
        self.map_section = self.screen.subsurface(map_rect)
        player_rect = pygame.Rect(805, 0, 695, 325)
        overall_rect = pygame.Rect(805, 320, 695, 325)
        kit_rect = pygame.Rect(805, 640, 695, 160)
        self.player_section = self.screen.subsurface(player_rect)
        self.kit_section = self.screen.subsurface(kit_rect)
        self.overall_section = self.screen.subsurface(overall_rect)

        border_color = (173, 161, 146)
        for rect in [map_rect, player_rect, overall_rect, kit_rect]:
            pygame.draw.rect(self.screen, border_color, rect, 10)

    # Function to get top-left point for each quadrant in screen coordinates
    def determine_quadrant_corner(self, type: pygame.Surface) -> tuple[int, int]:
        """Determine where the top left corner of the panel is."""
        if type == self.map_section:
            return (0, 0)  # Top-left quadrant
        if type == self.player_section:
            return (809, 10)  # Top-right quadrant
        if type == self.kit_section:
            return (809, 645)  # Bottom-left quadrant
        if type == self.overall_section:
            return (809, 325)  # Bottom-right quadrant
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
                rect = self.render_cell(
                    COLOUR_MAP[Tile.EMPTY],
                    row,
                    col,
                    OBJECT_SMALL,
                )
                if tile != Tile.EMPTY:
                    image = self.images.get(tile)
                    if image is not None:
                        self.screen.blit(image, rect.topleft)
                    # success = self.render_image_rect(rect, OBJECT_SMALL, tile)
                    else:
                        rect = self.render_cell(
                            colour,
                            row,
                            col,
                            OBJECT_SMALL,
                        )
                        self.render_cell(colour, row, col, BLOCK_SMALL)

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
        image = self.images.get(type)
        row_num = coords[0] * BLOCK_SMALL
        col_num = coords[1] * BLOCK_SMALL
        bkgnd_colour = COLOUR_MAP[Tile.EMPTY]
        half_diff_block = (BLOCK_SMALL - OBJECT_SMALL) / 2
        rect = self.render_cell(
            bkgnd_colour,
            round(row_num + half_diff_block),
            round(col_num + half_diff_block),
            OBJECT_SMALL,
        )
        print (image)
        if image is not None:
            self.screen.blit(image, rect.topleft)
        else:
            pygame.draw.rect(self.screen, COLOUR_ENTITIES[type], rect)

    def render_image_rect(
            self, rect: pygame.Rect, size: int, type: EntityType | ItemTypes | Tile
    ) -> bool:
        """Render an image onto a rectangle."""
        # Load and scale image to fit rectangle
        try:
            img = f"{DIRECTORY}/{OBJECT_IMAGE[type]}"
            image = pygame.image.load(img)
            # Scale image to rectangle size
            image_scaled = pygame.transform.scale(image, (size, size))
            # Render image inside rectangle
            self.screen.blit(image_scaled, rect.topleft)
            return True
        except pygame.error as e:
            print(f"Error loading image: {e}")
            return False

    def draw_item(self, type: ItemTypes, coords: tuple[int, int]) -> None:
        """Draw the Items on the level."""
        image = self.images.get(type)
        row_num = coords[0] * BLOCK_SMALL
        col_num = coords[1] * BLOCK_SMALL
        bkgnd_colour = COLOUR_MAP[Tile.EMPTY]
        half_diff_block = (BLOCK_SMALL - OBJECT_SMALL) / 2
        rect = self.render_cell(
            bkgnd_colour,
            round(row_num + half_diff_block),
            round(col_num + half_diff_block),
            OBJECT_XS,
        )
        if image is not None:
                self.screen.blit(image, rect.topleft)
        else:
            pygame.draw.rect(self.screen, COLOUR_ITEMS[type], rect)


    def render_circle_object(
        self, colour: tuple[int, int, int], row: int, col: int, size: int
    ) -> None:
        """Render a single round object on the map."""
        pygame.draw.circle(self.screen, colour, (col, row), size)

    def render_cell(
        self, colour: tuple[int, int, int], row: int, col: int, size: int
    ) -> pygame.Rect:
        """Render a single cell based on the cell type passed in."""
        rect = pygame.Rect(col, row, size, size)
        pygame.draw.rect(self.screen, colour, rect)
        return rect

    @staticmethod
    def show_error(message: str) -> None:
        """Display error message to log."""
        print(f"Error: {message}")

    @staticmethod
    def show_log(message: str) -> None:
        """Display note message to log."""
        print(f"Note: {message}")
