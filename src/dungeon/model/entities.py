"""Burrowkit Game Dungeon entities."""

from enum import Enum

from dungeon.model.level import GameLevel


class EntityType(Enum):
    """List of Entity types."""

    PLAYER = 0
    KIT = 1
    RAT = 2
    OOZE = 3
    GOBLIN = 4
    GOBLIN_BRUTE = 5
    GOBLIN_KING = 6


class EntityAttack(Enum):
    """Attack options, damage, hit rate and level required."""

    PUNCH = ("Punch", 2, 0.80, 1)
    SLUDGE = ("Sludge", 2, 0.80, 1)
    BITE = ("Bite", 1, 0.60, 1)
    CLUB_BASH = ("Club Bash", 2, 0.80, 1)
    BODYSLAM = ("BodySlam", 2, 0.80, 1)
    STAB = ("Stab", 3, 0.75, 2)
    SLASH = ("Slash", 4, 0.70, 3)
    IRON_JAB = ("Iron Jab", 7, 0.60, 4)
    BLADE_RUSH = ("Phantom Blade Rush", 10, 0.50, 5)

Attack_Allowed: dict[EntityAttack, EntityType] = {
    EntityAttack.PUNCH: EntityType.PLAYER,
    EntityAttack.STAB: EntityType.PLAYER,
    EntityAttack.SLASH: EntityType.PLAYER,
    EntityAttack.IRON_JAB: EntityType.PLAYER,
    EntityAttack.BLADE_RUSH: EntityType.PLAYER,
    EntityAttack.SLUDGE: EntityType.OOZE,
    EntityAttack.BITE: EntityType.RAT,
    EntityAttack.PUNCH: EntityType.GOBLIN,
    EntityAttack.PUNCH: EntityType.GOBLIN_BRUTE,
    EntityAttack.CLUB_BASH: EntityType.GOBLIN_BRUTE,
    EntityAttack.CLUB_BASH: EntityType.GOBLIN_KING,
    EntityAttack.BODYSLAM: EntityType.GOBLIN_KING,
}

class Direction(Enum):
    """List of possible movement directions."""

    UP = (1, 0, 1)
    DOWN = (-1, 0, 2)
    LEFT = (0, 1, 3)
    RIGHT = (0, -1, 4)

HEALTH_MULTIPLIER: int = 15

class Entity:
    """Class representing an entity within the dungeon game."""

    def __init__(self, game: GameLevel, position: tuple[int, int], id: int) -> None:
        """Initialise an Entity."""
        self.game = game
        self.position = position
        self.level = 1  # Entity current level, starts at 1
        self.hp = self.level * HEALTH_MULTIPLIER
        self.experience = 0  # Entity current experience, starts at 0
        self.damage = 0  # Entity current damage, starts at 0
        self.turn = 1  # Entity turn counter - may remove this if not used
        self.set_reference_id(id)

    def move_direction(
        self, movement: Direction, taken_pos: list[tuple[int, int]]
    ) -> bool:
        """Move Entity to grid coordinates."""
        new_row = self.position[0] - movement.value[0]
        new_col = self.position[1] - movement.value[1]
        if (
            self.game.validate_update(new_row, new_col)
            and (new_row, new_col) not in taken_pos
        ):
            self.position = self.game.game_progress(new_row, new_col)
            self.turn += 1
            return True
        return False

    def check_distance(self, position: tuple[int, int]) -> bool:
        """Check the distance to the a position, if close return True."""
        row = position[0] - self.position[0]
        col = position[1] - self.position[1]

        dist = (2, -2)  # number of tiles away to match against (any direction)
        match_position = False
        # if within N tiles of the position in any direction return true
        if (row < dist[0] and row > dist[1]) and (col < dist[0] and col > dist[1]):
            match_position = True
        return match_position

    def set_reference_id(self, num: int) -> None:
        """Set the monsters ID reference."""
        self.id_refererence = num + 101

