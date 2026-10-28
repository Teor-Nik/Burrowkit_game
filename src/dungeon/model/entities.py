"""Burrowkit Game Dungeon entities."""

import random
from collections import deque
from enum import Enum

from dungeon.model.level import Difficulty, GameLevel


class EntityType(Enum):
    """List of Entity types."""

    PLAYER = 0
    MONSTER = 1
    KIT = 2


class EntitySubType(Enum):
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
    Difficulty.EASY: 5,
    Difficulty.MEDIUM: 10,
    Difficulty.HARD: 13,
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
        self, game: GameLevel, position: tuple[int, int], monster_type: EntitySubType
    ) -> None:
        """Initialise the monster."""
        super().__init__(game, position)
        self.creature = EntityType.MONSTER
        self.monster_type = monster_type
        self.visible = False

    def check_position(self, curr_filled: list[tuple[int, int]], pos: tuple[int, int]) -> bool:
        """Check if the position is already occupied."""
        taken = False
        if pos in curr_filled:
            taken = True
        return taken

    def check_player_distance(self, player_pos: tuple[int, int]) -> bool:
        """Check the distance to the player, if close return True."""
        row = player_pos[0] - self.position[0]
        col = player_pos[1] - self.position[1]

        dist = (5, -5)  # number of tiles away to match against (any direction)
        valid_path = False
        # if within N tiles of the player in any direction return true
        if (row < dist[0] and row > dist[1]) and (col < dist[0] and col > dist[1]):
            valid_path = True
        return valid_path

    def bfs_pathfinder(
            self,
            player_pos: tuple[int, int],
            curr_filled: list[tuple[int, int]]
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
                curr = current_pos
                while curr is not None:
                    curr = parent[curr]
                    if curr is not None:
                        path.append(curr)
                return path

            for direction in enumerate(Direction):
                setrow = qrow + direction[1].value[0]
                setcol = qcol + direction[1].value[1]
                neighbor_pos = (setrow, setcol)
                if (self.game.validate_nonplayer_update(setrow, setcol)
                    and neighbor_pos not in parent
                    # and not self.check_position(curr_filled, neighbor_pos)
                ):
                    parent[neighbor_pos] = current_pos
                    queue.append(neighbor_pos)
        return None


class EntityModel:
    """Class tracking the entities within the dungeon game."""

    def __init__(self, game: GameLevel) -> None:
        """Initialise the entities."""
        self.entities_list: list[Monster] = []
        self.game = game

    def add_entities(self, entity: Monster) -> None:
        """Store all of the entities in the current level."""
        self.entities_list.append(entity)

    def generate_monsters(self, game: GameLevel) -> None:
        """Generate the monsters needed for that level."""
        self.entities_list: list[Monster] = []
        # Only include all monsters for the MAX level of the game
        if game.current_level == game.max_level:
             types = [monsters for monsters in EntitySubType]
        else:
            types = [
                monsters for monsters in EntitySubType if monsters.name not in (
                    "GOBLIN_KING"
                )
            ]
        # Create decreasing weights based on position
        weights = list(range(len(types), 0, -1))
        for num in range(DIFFICULTY_EXP[game.difficulty]):
            # Select one random enum member favoring earlier items
            chosen_type = random.choices(types, weights=weights, k=1)[0]
            monster = Monster(game, game.random_position(), chosen_type)
            self.add_entities(monster)

    def move_monsters(self, player_pos: tuple[int, int]) -> None:
        """Move all monsters to new valid grid coordinates."""
        for monster in self.entities_list:
            filled_positions = []
            for mon in self.entities_list:
                filled_positions.append(mon.position)
            valid_movement = False
            bfs = False
            if monster.check_player_distance(player_pos):
                monster.visible = True
                bfs = True
            if bfs:
                path = monster.bfs_pathfinder(player_pos, filled_positions)
                next_pos = monster.position
                if path is not None:
                    result = path[-2:-1]
                    check_next_pos = result[0] if result else None
                    if (
                        isinstance(check_next_pos,(tuple))
                        and check_next_pos != monster.position
                        and check_next_pos != player_pos
                        and check_next_pos not in filled_positions
                    ):
                        next_pos = check_next_pos
                monster.position = (next_pos[0], next_pos[1])
                valid_movement = True
            if not valid_movement or not bfs:
                while not valid_movement:
                    movement = round(random.uniform(1, len(Direction)))
                    for direction in enumerate(Direction):
                        if movement == direction[1].value[2]:
                            new_row = monster.position[0] - direction[1].value[0]
                            new_col = monster.position[1] - direction[1].value[1]
                            if (self.game.validate_nonplayer_update(new_row, new_col)
                                and (new_row, new_col) not in filled_positions
                            ):
                                monster.position = (new_row, new_col)
                                valid_movement = True

    def monster_stats(self) -> str:
        """Generate a list of the monster stats."""
        stats: str = ""
        for mon in self.entities_list:
            stats = stats + f"\n{mon.monster_type.value[0]}: {mon.position}"
        return stats
