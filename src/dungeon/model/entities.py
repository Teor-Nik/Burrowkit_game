"""Burrowkit Game Dungeon entities."""

import random
from enum import Enum

from dungeon.model.level import Difficulty, GameLevel


class EntityType(Enum):
    """List of Entity types."""

    PLAYER = 0
    MONSTER = 1
    KIT = 2


class MonsterType(Enum):
    """List of types of monsters and their points."""

    BAT = ("Bat", 1)
    OOZE = ("Ooze", 2)
    GOBLIN = ("Goblin", 4)
    GOBLIN_BRUTE = ("Goblin Brute", 10)
    GOBLIN_KING = ("Goblin King", 20)


class Direction(Enum):
    """List of possible movement directions."""

    UP = (1, 0, 1)
    DOWN = (-1, 0, 2)
    LEFT = (0, 1, 3)
    RIGHT = (0, -1, 4)


DIFFICULTY_EXP: dict[Difficulty, int] = {
    Difficulty.EASY: 3,
    Difficulty.MEDIUM: 6,
    Difficulty.HARD: 12,
}


class Entity:
    """Class representing an entity within the dungeon game."""

    def __init__(self, game: GameLevel, position: tuple[int, int]) -> None:
        """Initialise an Entity."""
        self.game = game
        self.position = position
        self.player_turn = True


class Player(Entity):
    """Class representing a player in the dungeon game."""

    def __init__(self, game: GameLevel, position: tuple[int, int]) -> None:
        """Initialise the Player."""
        super().__init__(game, position)
        self.turn = 1
        self.creature = EntityType.PLAYER

    def move_direction(self, movement: Direction) -> bool:
        """Move player to grid coordinates."""
        new_row = self.position[0] - movement.value[0]
        new_col = self.position[1] - movement.value[1]
        if self.game.validate_update(new_row, new_col):
            self.position = self.game.game_progress(new_row, new_col)
            self.turn += 1
            self.player_turn = False
            return True
        return False


class Monster(Entity):
    """Class representing a monster in the dungeon game."""

    def __init__(
        self, game: GameLevel, position: tuple[int, int], monster_type: MonsterType
    ) -> None:
        """Initialise the monster."""
        super().__init__(game, position)
        self.creature = EntityType.MONSTER
        self.monster_type = monster_type

    def move_direction(self) -> bool:
        """Move player to grid coordinates."""
        valid_movement = False
        while not valid_movement:
            movement = round(random.uniform(1, len(Direction)))
            for position, direction in enumerate(Direction):
                if movement == direction.value[2]:
                    new_row = self.position[0] - direction.value[0]
                    new_col = self.position[1] - direction.value[1]
                    if self.game.validate_nonplayer_update(new_row, new_col):
                        self.position = (new_row, new_col)
                        valid_movement = True
        return valid_movement


class EntityModel:
    """Class tracking the entities within the dungeon game."""

    def __init__(self) -> None:
        """Initialise the entities."""
        self.entities_list: list[Monster] = []

    def add_entities(self, entity: Monster) -> None:
        """Store all of the entities in the current level."""
        self.entities_list.append(entity)

    def generate_monsters(self, game: GameLevel) -> None:
        """Generate the monsters needed for that level."""
        # Only include all monsters for the MAX level of the game
        if game.current_level == game.max_level:
            types = list(MonsterType)
        else:
            types = [
                monsters for monsters in MonsterType if monsters.name != "GOBLIN_KING"
            ]
        # Create decreasing weights based on position
        weights = list(range(len(types), 0, -1))
        for num in range(game.difficulty.value):
            # Select one random enum member favoring earlier items
            chosen_type = random.choices(types, weights=weights, k=1)[0]
            monster = Monster(game, game.random_position(), chosen_type)
            self.add_entities(monster)
            num += 1

    def monster_stats(self) -> str:
        """Generate a list of the monster stats."""
        stats: str = ""
        for mon in self.entities_list:
            stats = stats + f"\n{mon.monster_type.value[0]}: {mon.position}"
        return stats
