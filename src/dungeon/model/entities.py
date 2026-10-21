"""Burrowkit Game Dungeon entities."""

from enum import Enum

from dungeon.model.level import GameLevel


class EntityType(Enum):
    """List of Entity types."""

    PLAYER = 0
    MONSTER = 1
    KIT = 2


class Entity:
  """Class representing an entity within the dungeon game."""

  def __init__ (self, game_level: GameLevel, coords: tuple[int, int]) -> None:
    """Initialise an Entity."""
    self.game = game_level
    self.position = coords

class Player(Entity):
    """Class representing a player in the dungeon game."""

    def __init__(self, game_level: GameLevel, coords: tuple[int, int]) -> None:
        """Initialise the Player."""
        self.game = game_level
        self.position = coords
        self.type = EntityType.PLAYER

    def player_move_coords(self, coords: tuple[int, int], keyname: str) -> bool:
        """Move player to grid coordinates."""
        row_position = coords[0]
        col_position = coords[1]
        if not isinstance(row_position, int):
            raise TypeError("First element is not an integer.")
        if not isinstance(col_position, int):
            raise TypeError("First element is not an integer.")
        new_row = row_position
        new_col = col_position
        if keyname == "up":
            new_row -= 1
        elif keyname == "down":
            new_row += 1
        elif keyname == "left":
            new_col -= 1
        elif keyname == "right":
            new_col += 1
        if self.game.valid_move(new_row, new_col, row_position, col_position):
            self.position = (new_row, new_col)
            return True
        return False
