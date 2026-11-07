"""Entities of a Kit Sub-Class."""

from enum import Enum

from dungeon.model.entities import Entity, EntityType
from dungeon.model.level import GameLevel


class KitSubType(Enum):
    """List of types of monsters and their level, damage and hit rate."""

    KIT = ("Kit", 1, 1, 0.50)
    JUNIOR_KIT = ("Junior Kit", 3, 2, 0.45)
    FOX = ("Fox", 5, 2, 0.45)
    MASTER_FOX = ("Master Fox", 7, 3, 0.40)
    ELDER_FOX = ("Elder Fox", 25, 8, 0.75)

class Kit(Entity):
    """Class representing a monster in the dungeon game."""

    def __init__(
        self, game: GameLevel, position: tuple[int, int], id: int
    ) -> None:
        """Initialise the monster."""
        super().__init__(game, position, id)
        self.position = position
        self.creature = EntityType.KIT
        self.monster_type = KitSubType.KIT

    def move_kit(
            self, player_pos: tuple[int, int], filled_positions: list[tuple[int, int]]
    ) -> None:
        """Move Kit to new valid grid coordinates."""
        if not self.check_player_distance(player_pos, 3, self.position):
            path = self.bfs_pathfinder(player_pos)
            next_pos = self.position
            if path is not None:
                result = path[-2:-1]
                check_next_pos = result[0] if result else None
                if (
                    isinstance(check_next_pos, (tuple))
                    and check_next_pos != self.position
                    and check_next_pos != player_pos
                    and check_next_pos not in filled_positions
                ):
                    next_pos = check_next_pos
            self.position = (next_pos[0], next_pos[1])
        elif self.check_player_distance(player_pos, 3, self.position):
            away_path = self.bfs_move_away(player_pos)
            next_pos = self.position
            if away_path is not None:
                check_next_pos = away_path
                if (
                    isinstance(check_next_pos, (tuple))
                    and check_next_pos != self.position
                    and check_next_pos != player_pos
                    and check_next_pos not in filled_positions
                ):
                    next_pos = check_next_pos
            self.position = (next_pos[0], next_pos[1])
