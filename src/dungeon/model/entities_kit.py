"""Entities of a Kit Sub-Class."""

from enum import Enum

from dungeon.model.entities import Entity, EntityType, grid_distance
from dungeon.model.level import GameLevel


class KitSubType(Enum):
    """List of types of Kits and their level, damage and hit rate."""

    KIT = ("Kit", 1, 1, 0.50)
    JUNIOR_KIT = ("Junior Kit", 3, 2, 0.45)
    MASTER_FOX = ("Master", 7, 3, 0.40)
    ELDER_FOX = ("Elder", 25, 8, 0.75)

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
        # print("Kit is moving...",grid_distance(self.position, player_pos))
        if not grid_distance(self.position, player_pos) <= 3:
            path = self.bfs_pathfinder(player_pos)
            # print ("Kit path:", path)
            # next_pos = self.position
            if path is not None and path != player_pos and path not in filled_positions:
                self.position = path
            #     result = path[-2:-1]
            #     check_next_pos = result[0] if result else None
            #     if (
            #         isinstance(check_next_pos, (tuple))
            #         and check_next_pos != self.position
            #         and check_next_pos != player_pos
            #         and check_next_pos not in filled_positions
            #     ):
            #         next_pos = check_next_pos
            # self.position = (next_pos[0], next_pos[1])
        elif grid_distance(self.position, player_pos) <= 3:
            away_path = self.bfs_move_away(player_pos)
            # next_pos = self.position
            if away_path is not None and away_path != player_pos and away_path not in filled_positions:
                self.position = away_path
            #     check_next_pos = away_path
            #     if (
            #         isinstance(check_next_pos, (tuple))
            #         and check_next_pos != self.position
            #         and check_next_pos != player_pos
            #         and check_next_pos not in filled_positions
            #     ):
            #         next_pos = check_next_pos
            # self.position = (next_pos[0], next_pos[1])
        # print("Kit moved to:", self.position, "from:", player_pos)
