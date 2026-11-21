"""Entities of a Monster Sub-Class."""

import random
from enum import Enum

from dungeon.model.entities import (
    Direction,
    Entity,
    EntityType,
)
from dungeon.model.level import GameLevel


class EntitySubType(Enum):
    """List of types of monsters and their points, hp and hit rate."""

    RATBLACK = ("Rat", 4, 10, 0.75)
    RATBROWN = ("Rat", 4, 10, 0.50)
    RATGREY = ("Rat", 4, 10, 0.65)
    RATWHITE = ("Rat", 4, 10, 0.85)
    SLIMEBLUE = ("Slime", 6, 20, 0.55)
    SLIMEGREEN = ("Slime", 6, 20, 0.85)
    SLIMEORANGE = ("Slime", 6, 20, 0.75)
    SLIMEPINK = ("Slime", 6, 20, 0.55)
    SLIMEPURPLE = ("Slime", 6, 20, 0.90)
    GOBLIN = ("Goblin", 7, 25, 0.65)
    GOBLIN_BRUTE = ("Goblin Brute", 10, 30, 0.75)
    GOBLIN_KING = ("Goblin King", 25, 80, 0.95)

SubType: dict[EntityType, EntitySubType] = {
    EntityType.SLIMEBLUE: EntitySubType.SLIMEBLUE,
    EntityType.SLIMEGREEN: EntitySubType.SLIMEGREEN,
    EntityType.SLIMEORANGE: EntitySubType.SLIMEORANGE,
    EntityType.SLIMEPINK: EntitySubType.SLIMEPINK,
    EntityType.SLIMEPURPLE: EntitySubType.SLIMEPURPLE,
    EntityType.RATBLACK: EntitySubType.RATBLACK,
    EntityType.RATBROWN: EntitySubType.RATBROWN,
    EntityType.RATGREY: EntitySubType.RATGREY,
    EntityType.RATWHITE: EntitySubType.RATWHITE,
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
        self.visible = False
        self.move_processed = False
        self.most_recent_move = None

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

    def attack_player(self, player_pos: tuple[int, int]) -> int:
        """Attack the player while on turn."""
        if self.check_player_distance(player_pos, 2, self.position):
            filtered_move = self.attack_moves()
            if filtered_move is not None:
                move = random.choice(filtered_move)
                self.most_recent_move = f"{move.value[0]}"
                percentage_chance = self.monster_type.value[3]
                rand = random.random()
                if rand < percentage_chance:
                    self.most_recent_move += f", {move.value[1]} damage."
                    return move.value[1]
                else:
                    self.most_recent_move += ", missed!"
        return 0

    def monster_stats(self) -> str:
        """Generate a the monster stats."""
        stats: str = ""
        # Get raw values ready to format
        name = self.monster_type.value[0]
        hp = self.monster_type.value[1]
        hp_remaining = self.hp
        # format raw values
        name_and_id = f"  {name} (#{self.entity_id})"
        hp_stats = f"HP: ({hp_remaining} / {hp})"
        recent_move: str = ""
        if self.move_processed:
            recent_move = "\n     *********************"
        else:
            recent_move = f"\n     Move: {self.most_recent_move}"
        stats = stats + (
            f"\n{name_and_id:<30}"
            f"{hp_stats:<20}"
            f"{recent_move}"
        )
        return stats

    def determine_visibility(self, player_pos: tuple[int, int]) -> None:
        """Determine if the monster should be visible or not."""
        if self.check_player_distance(player_pos, PLAYER_CHASE_DISTANCE, self.position):
            self.visible = True
        else:
            self.visible = False

    def move_monster(
            self, player_pos: tuple[int, int], filled_positions: list[tuple[int, int]]
    ) -> None:
        """Move monster to new valid grid coordinates."""
        self.move_processed = True
        valid_movement = False
        self.determine_visibility(player_pos)
        if self.visible:
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
        if not valid_movement or not self.visible:
            while not valid_movement:
                movement = round(random.uniform(1, len(Direction)))
                for direction in enumerate(Direction):
                    if movement-1 == direction[0]:
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
