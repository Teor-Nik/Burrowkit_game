"""Entities of a Monster Sub-Class."""

import random
from collections import deque
from enum import Enum

from dungeon.model.entities import (
    Direction,
    Entity,
    EntityType,
)
from dungeon.model.level import GameLevel


class EntitySubType(Enum):
    """List of types of monsters and their points, damage and hit rate."""

    RAT = ("Rat", 2, 1, 0.50)
    OOZE = ("Ooze", 3, 2, 0.45)
    GOBLIN = ("Goblin", 5, 2, 0.45)
    GOBLIN_BRUTE = ("Goblin Brute", 7, 3, 0.40)
    GOBLIN_KING = ("Goblin King", 25, 8, 0.75)

SubType: dict[EntityType, EntitySubType] = {
    EntityType.OOZE: EntitySubType.OOZE,
    EntityType.RAT: EntitySubType.RAT,
    EntityType.GOBLIN: EntitySubType.GOBLIN,
    EntityType.GOBLIN_BRUTE: EntitySubType.GOBLIN_BRUTE,
    EntityType.GOBLIN_KING: EntitySubType.GOBLIN_KING,
}

PLAYER_CHASE_DISTANCE: int = 5

class Monster(Entity):
    """Class representing a monster in the dungeon game."""

    def __init__(
        self, game: GameLevel, position: tuple[int, int], id: int
    ) -> None:
        """Initialise the monster."""
        super().__init__(game, position, id)
        mon_type = self.monster_level_types(game)
        self.position = position
        self.creature = mon_type
        self.monster_type = SubType[self.creature]
        self.hp = self.monster_type.value[1]
        self.visible = True
        self.move_processed = False

    def monster_level_types(self, game: GameLevel) -> EntityType:
        """Generate a monster needed for this level."""
        # Only include all monsters for the MAX level of the game
        if game.current_level == game.max_level:
            types = [monsters for monsters in SubType]
        else:
            types = [
                monsters
                for monsters in SubType
                if monsters.name not in ("GOBLIN_KING")
            ]
        weights = list(range(len(types), 0, -1))
        # for _ in range(DIFFICULTY_EXP[game.difficulty]):
            # Select one random enum member favoring earlier items
        chosen_type = random.choices(types, weights=weights, k=1)[0]
        return chosen_type

    def check_position(
        self, curr_filled: list[tuple[int, int]], pos: tuple[int, int]
    ) -> bool:
        """Check if the position is already occupied."""
        taken = False
        if pos in curr_filled:
            taken = True
        return taken

    def check_player_distance(
            self, player_pos: tuple[int, int], distance_check: int
    ) -> bool:
        """Check the distance to the player, if close return True."""
        row = player_pos[0] - self.position[0]
        col = player_pos[1] - self.position[1]
        max_dist = distance_check
        # number of tiles away to match against (any direction)
        dist = (max_dist, -max_dist)
        valid_path = False
        # if within N tiles of the player in any direction return true
        if (row < dist[0] and row > dist[1]) and (col < dist[0] and col > dist[1]):
            valid_path = True
        return valid_path

    def bfs_pathfinder(
        self, player_pos: tuple[int, int]
    ) -> list[tuple[int, int]] | None:
        """Find the best path towards the players curernt position."""
        start = self.position
        queue = deque([start])
        parent: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        while queue:
            current_pos = queue.popleft()
            qrow, qcol = current_pos
            if current_pos == player_pos:
                path = []
                curr: tuple[int, int] | None = current_pos
                while curr is not None:
                    curr = parent[curr]
                    if curr is not None:
                        path.append(curr)
                return path

            for direction in enumerate(Direction):
                setrow = qrow + direction[1].value[0]
                setcol = qcol + direction[1].value[1]
                neighbor_pos = (setrow, setcol)
                if (
                    self.game.validate_nonplayer_update(setrow, setcol)
                    and neighbor_pos not in parent
                ):
                    parent[neighbor_pos] = current_pos
                    queue.append(neighbor_pos)
        return None

    def attack_player(self, player_pos: tuple[int, int]) -> int:
        """Attack the player while on turn."""
        if self.check_player_distance(player_pos, 2):
            percentage_chance = self.monster_type.value[3]
            rand = random.random()
            if rand < percentage_chance: # and player.turn > 5:
                # player.damage += self.monster_type.value[2]
                # print(player.damage)
                print (rand, percentage_chance)
                return self.monster_type.value[2]
        return 0

    def monster_stats(self) -> str:
        """Generate a list of the monster stats."""
        stats: str = ""
        name = self.monster_type.value[0]
        hp = self.monster_type.value[1]
        hp_remaining = self.hp
        stats = stats + (
            f"\n    ID:  {self.id_refererence}    {name}\n"
            f"        - HP: {hp_remaining} / {hp}\n"
        )
        return stats

    def move_monster(
            self, player_pos: tuple[int, int], filled_positions: list[tuple[int, int]]
    ) -> None:
        """Move all monsters to new valid grid coordinates."""
        self.move_processed = True
        valid_movement = False
        bfs = False
        print (self.visible)
        if self.check_player_distance(player_pos, PLAYER_CHASE_DISTANCE):
            self.visible = True
            bfs = True
        if bfs:
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
            valid_movement = True
        if not valid_movement or not bfs:
            while not valid_movement:
                movement = round(random.uniform(1, len(Direction)))
                for direction in enumerate(Direction):
                    if movement == direction[1].value[2]:
                        new_row = self.position[0] - direction[1].value[0]
                        new_col = self.position[1] - direction[1].value[1]
                        if (
                            self.game.validate_nonplayer_update(new_row, new_col)
                            and (new_row, new_col) not in filled_positions
                        ):
                            self.position = (new_row, new_col)
                            valid_movement = True
                if not valid_movement:
                    # give the whileloop a way out if there are no feasible moves
                    break
