"""Burrowkit Game Dungeon entities."""

from collections import deque
from enum import Enum

from dungeon.model.level import GameLevel, Position


class EntityType(Enum):
    """List of Entity types."""

    PLAYER = 0
    KIT = 1
    RATBLACK = 2
    RATBROWN = 3
    RATGREY = 4
    RATWHITE = 5
    SLIMEBLUE = 6
    SLIMEGREEN = 7
    SLIMEORANGE = 8
    SLIMEPINK = 9
    SLIMEPURPLE = 10
    GOBLIN = 11
    GOBLIN_BRUTE = 12
    GOBLIN_KING = 13


class EntityAttack(Enum):
    """Attack options: name, damage, hit rate and the level that unlocks it."""

    PUNCH = ("Punch", 2, 0.80, 1)
    SLUDGE = ("Sludge", 1, 0.80, 1)
    BITE = ("Bite", 1, 0.60, 1)
    CLUB_BASH = ("Club Bash", 2, 0.80, 1)
    BODYSLAM = ("Body Slam", 2, 0.80, 1)
    STAB = ("Stab", 3, 0.75, 2)
    SLASH = ("Slash", 4, 0.70, 3)
    IRON_JAB = ("Iron Jab", 7, 0.60, 4)
    BLADE_RUSH = ("Phantom Blade Rush", 10, 0.50, 5)

    def __init__(
        self, label: str, damage: int, hit_rate: float, unlock_level: int
    ) -> None:
        """Unpack the tuple value into named attributes."""
        self.label = label
        self.damage = damage
        self.hit_rate = hit_rate
        self.unlock_level = unlock_level

_RAT_ATTACKS = (EntityAttack.BITE,)
_SLIME_ATTACKS = (EntityAttack.SLUDGE,)


# Which attacks each kind of entity knows (before level requirements).
ALLOWED_ATTACKS: dict[EntityType, tuple[EntityAttack, ...]] = {
    EntityType.PLAYER: (
        EntityAttack.PUNCH,
        EntityAttack.STAB,
        EntityAttack.SLASH,
        EntityAttack.IRON_JAB,
        EntityAttack.BLADE_RUSH,
    ),
    EntityType.RATBLACK: _RAT_ATTACKS,
    EntityType.RATBROWN: _RAT_ATTACKS,
    EntityType.RATGREY: _RAT_ATTACKS,
    EntityType.RATWHITE: _RAT_ATTACKS,
    EntityType.SLIMEBLUE: _SLIME_ATTACKS,
    EntityType.SLIMEGREEN: _SLIME_ATTACKS,
    EntityType.SLIMEORANGE: _SLIME_ATTACKS,
    EntityType.SLIMEPINK: _SLIME_ATTACKS,
    EntityType.SLIMEPURPLE: _SLIME_ATTACKS,
    EntityType.GOBLIN: (EntityAttack.PUNCH,),
    EntityType.GOBLIN_BRUTE: (EntityAttack.PUNCH, EntityAttack.CLUB_BASH),
    EntityType.GOBLIN_KING: (EntityAttack.CLUB_BASH, EntityAttack.BODYSLAM),
}

class Direction(Enum):
    """Movement directions as (row change, column change)."""

    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def step(self, position: Position) -> Position:
        """Return the position one tile away from ``position`` in this direction."""
        row, col = position
        d_row, d_col = self.value
        return (row + d_row, col + d_col)

def grid_distance(a: Position, b: Position) -> int:
    """Return the number of king-moves between two tiles (diagonals count as 1)."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


ADJACENT: int = 1  # attacks reach neighbouring tiles, diagonals included
HEALTH_MULTIPLIER: int = 15
EXP_MULTIPLIER: int = 100

class Entity:
    """Class representing an entity within the dungeon game."""

    creature: EntityType  # set by each subclass

    def __init__(self, game: GameLevel, position: tuple[int, int], id: int) -> None:
        """Initialise an Entity."""
        self.game = game
        self.position = position
        self.entity_id = id
        self.level = 1
        self.max_hp = self.level * HEALTH_MULTIPLIER
        self.experience = 0
        self.damage = 0  # damage taken so far; current HP is max_hp - damage
        self.fainted = False
        # self.turn = 1  # Entity turn counter - may remove this if not used
        # self.set_reference_id(id)

    @property
    def current_hp(self) -> int:
        """Return the health the entity has left."""
        return self.max_hp - self.damage

    @property
    def exp_to_next_level(self) -> int:
        """Return the experience needed to reach the next level."""
        return self.level * EXP_MULTIPLIER

    def move_direction(
        self, movement: Direction, taken_pos: list[tuple[int, int]]
    ) -> bool:
        """Move Entity to grid coordinates."""
        new_row = self.position[0] - movement.value[0]
        new_col = self.position[1] - movement.value[1]
        # print(taken_pos, "/n current:",self.position, "/n change", new_row, new_col)
        # print(self.game.validate_update(new_row, new_col))
        if (
            self.game.validate_update(new_row, new_col)
            and (new_row, new_col) not in taken_pos
        ):
            # print("all good")
            self.position = self.game.game_progress(new_row, new_col)
            # self.turn += 1
            return True
        return False

    def attack_moves(self) -> list[EntityAttack] | None:
        """Return a list of valid attack moves for the entities level."""
        return [
            attack
            for attack in ALLOWED_ATTACKS.get(self.creature, ())
            if attack.unlock_level <= self.level
        ]

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

    def increase_exp(self, exp_value: int) -> int:
        """Increase the player EXP based on level and monster killed."""
        self.experience += exp_value
        levels_gained = 0
        while self.experience >= self.exp_to_next_level:
            self.experience -= self.exp_to_next_level
            self.level += 1
            levels_gained += 1
            self.max_hp = self.level * HEALTH_MULTIPLIER
            # Levelling up heals you to at least 75% health.
            self.damage = min(self.damage, round(self.max_hp / 4))
        return levels_gained

    def remove_damage(self, health_value: int) -> None:
        """Calculate the entities damage restoration."""
        self.damage = max(0, self.damage - health_value)

    def take_damage(self, impact_value: int) -> bool:
        """Calculate the entities damage until no health left."""
        if impact_value <= 0:
            return False
        self.damage = min(self.max_hp, self.damage + impact_value)
        if self.damage >= self.max_hp:
            self.fainted = True
        return self.fainted

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
