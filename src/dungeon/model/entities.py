"""Burrowkit Game Dungeon entities."""

from enum import Enum

from dungeon.model.level import GameLevel


class EntityType(Enum):
    """List of Entity types."""

    PLAYER = 0
    MONSTER = 1
    KIT = 2


class Direction(Enum):
    """List of possible movement directions."""

    up = (1, 0)
    down = (-1, 0)
    left = (0, 1)
    right = (0, -1)

class Entity:
    """Class representing an entity within the dungeon game."""

    def __init__(self, game_level: GameLevel, coords: tuple[int, int]) -> None:
        """Initialise an Entity."""
        self.game = game_level
        self.position = coords
        self.creature = EntityType


class Player(Entity):
    """Class representing a player in the dungeon game."""

    def __init__(self, game_level: GameLevel, coords: tuple[int, int]) -> None:
        """Initialise the Player."""
        super().__init__(game_level, coords)
        self.creature = EntityType.PLAYER

    def move_direction(self, movement: str) -> bool:
        """Move player to grid coordinates."""
        for position, direction in enumerate(Direction):
            if direction.name == movement:
                new_row = self.position[0] - direction.value[0]
                new_col = self.position[1] - direction.value[1]
                if self.game.validate_update(new_row, new_col):
                    self.position = self.game.game_progress(new_row, new_col)
                    return True
        return False
