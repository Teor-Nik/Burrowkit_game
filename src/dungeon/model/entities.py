"""Burrowkit Game Dungeon entities."""

from collections import deque
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

    def bfs_move_away(
            self, player_pos: tuple[int, int], max_distance: int = 3
    ) -> tuple[int, int] | None:
        """Find a move that goes away from the player, up to max_distance."""
        start = player_pos
        queue = deque([start])
        distances: dict[tuple[int, int], int] = {start: 0}

        # BFS from player to get distances
        while queue:
            current_pos = queue.popleft()
            qrow, qcol = current_pos
            for _, direction in enumerate(Direction):
                setrow = qrow + direction.value[0]
                setcol = qcol + direction.value[1]
                neighbor_pos = (setrow, setcol)
                if (
                    self.game.validate_nonplayer_update(setrow, setcol)
                    and neighbor_pos not in distances
                ):
                    distances[neighbor_pos] = distances[current_pos] + 1
                    queue.append(neighbor_pos)

        # Current distance from player
        current_dist = distances.get(self.position, None)
        if current_dist is None:
            return None  # Can't reach current position from player

        # Find a neighbor that increases distance but stays within max_distance
        qrow, qcol = self.position
        for _, direction in enumerate(Direction):
            setrow = qrow + direction.value[0]
            setcol = qcol + direction.value[1]
            neighbor_pos = (setrow, setcol)
            if self.game.validate_nonplayer_update(setrow, setcol):
                neighbor_dist = distances.get(neighbor_pos, None)
                if (neighbor_dist is not None
                    and neighbor_dist > current_dist
                    and neighbor_dist <= max_distance
                ):
                    return neighbor_pos  # First valid move away

        return None  # No valid move away

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

    def check_player_distance(
            self,
            player_pos: tuple[int, int],
            distance_check: int,
            current_pos: tuple[int, int],
    ) -> bool:
        """Check the distance to the player, if close return True."""
        row = player_pos[0] - current_pos[0]
        col = player_pos[1] - current_pos[1]
        max_dist = distance_check
        # number of tiles away to match against (any direction)
        dist = (max_dist, -max_dist)
        valid_path = False
        # if within N tiles of the player in any direction return true
        if (row < dist[0] and row > dist[1]) and (col < dist[0] and col > dist[1]):
            valid_path = True
        return valid_path
