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
    """List of types of monsters and their points, damage and hit rate."""

    RAT = ("Rat", 2, 1, 0.50)
    OOZE = ("Ooze", 3, 2, 0.45)
    GOBLIN = ("Goblin", 5, 2, 0.45)
    GOBLIN_BRUTE = ("Goblin Brute", 7, 3, 0.40)
    GOBLIN_KING = ("Goblin King", 25, 8, 0.75)


class Direction(Enum):
    """List of possible movement directions."""

    UP = (1, 0, 1)
    DOWN = (-1, 0, 2)
    LEFT = (0, 1, 3)
    RIGHT = (0, -1, 4)


DIFFICULTY_EXP: dict[Difficulty, int] = {
    Difficulty.EASY: 8,
    Difficulty.MEDIUM: 15,
    Difficulty.HARD: 20,
}

EXP_MULTIPLIER: int = 100
HEALTH_MULTIPLIER: int = 15
PLAYER_CHASE_DISTANCE: int = 5


class PlayerAttack(Enum):
    """Player attack options, damage, hit rate and level required."""

    PUNCH = ("Punch", 2, 0.80, 1)
    STAB = ("Stab", 3, 0.75, 2)
    SLASH = ("Slash", 4, 0.70, 3)
    IRON_JAB = ("Iron Jab", 7, 0.60, 4)
    BLADE_RUSH = ("Phantom Blade Rush", 10, 0.50, 5)


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
        self.creature = EntityType.PLAYER
        self.level = 1  # Player current level, starts at 1
        self.hp = self.level * HEALTH_MULTIPLIER
        self.experience = 0  # Player current experience, starts at 0
        self.damage = 0  # Player current damage, starts at 0
        self.turn = 1  # Player turn counter - may remove this if not used

    def move_direction(
        self, movement: Direction, taken_pos: list[tuple[int, int]]
    ) -> bool:
        """Move player to grid coordinates."""
        new_row = self.position[0] - movement.value[0]
        new_col = self.position[1] - movement.value[1]
        if (
            self.game.validate_update(new_row, new_col)
            and (new_row, new_col) not in taken_pos
        ):
            self.position = self.game.game_progress(new_row, new_col)
            self.turn += 1
            self.player_turn = False
            return True
        return False

    def check_monster_distance(self, monster_pos: tuple[int, int]) -> bool:
        """Check the distance to the player, if close return True."""
        row = monster_pos[0] - self.position[0]
        col = monster_pos[1] - self.position[1]

        dist = (2, -2)  # number of tiles away to match against (any direction)
        match_position = False
        # if within N tiles of the player in any direction return true
        if (row < dist[0] and row > dist[1]) and (col < dist[0] and col > dist[1]):
            match_position = True
        return match_position

    def increase_exp(self, monster: EntitySubType) -> None:
        """Increase the player EXP based on level and monster killed."""
        self.experience += self.game.difficulty.value[0] * monster.value[2]
        self.determine_levle()

    def determine_levle(self) -> None:
        """Determine the player Level and reset experieince on level up."""
        if self.experience >= self.level * EXP_MULTIPLIER:
            self.level += 1
            self.hp = self.level * HEALTH_MULTIPLIER
            self.experience = 0

    def player_stats(self) -> str:
        """Generate a list of the monster stats."""
        required_exp = self.level * EXP_MULTIPLIER
        current_damage = self.hp - self.damage
        attackmoves: str = ""
        for move in PlayerAttack:
            if self.level >= move.value[3]:
                attackmoves += f"    - {move.value[0]}  ({move.value[1]})\n"
        stats: str = (
            f"\nLevel:   {self.level}\n"
            f"\n    Exp:   {self.experience} / {required_exp}.\n"
            f"\n    Health:   {current_damage} / {self.hp}\n"
            f"\nAttack Moves   (damage):\n{attackmoves}"
        )
        return stats

    def attack_monster(self, attack_key: PlayerAttack, monsters: list["Monster"]) -> None:
        """Attack the nearest adjacent Monster."""
        print("Attack!")
        attack_made = False
        for move in PlayerAttack:
            if self.level >= move.value[3]:
                monsters.sort(key=lambda obj: obj.hit_points)
                for mon in monsters:
                    if not attack_made:
                        if self.check_monster_distance(mon.position):
                            print(mon.monster_type.value[0], mon.hit_points)
                            mon.hit_points -= attack_key.value[1]
                            attack_made = True
                            if mon.hit_points <= 0:
                                self.increase_exp(mon.monster_type)


class Monster(Entity):
    """Class representing a monster in the dungeon game."""

    def __init__(
        self, game: GameLevel, position: tuple[int, int], monster_type: EntitySubType
    ) -> None:
        """Initialise the monster."""
        super().__init__(game, position)
        self.creature = EntityType.MONSTER
        self.monster_type = monster_type
        self.hit_points = self.monster_type.value[1]
        self.visible = False

    def set_reference_id(self, num: int) -> None:
        """Set the monsters ID reference."""
        self.id_refererence = num + 101

    def check_position(
        self, curr_filled: list[tuple[int, int]], pos: tuple[int, int]
    ) -> bool:
        """Check if the position is already occupied."""
        taken = False
        if pos in curr_filled:
            taken = True
        return taken

    def check_player_distance(self, player_pos: tuple[int, int], distance_check: int) -> bool:
        """Check the distance to the player, if close return True."""
        row = player_pos[0] - self.position[0]
        col = player_pos[1] - self.position[1]
        max_dist = distance_check
        dist = (max_dist, -max_dist)  # number of tiles away to match against (any direction)
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

    def attack_player(self, player: Player):
        """Attack the player while on turn."""
        percentage_chance = self.monster_type.value[3]
        rand = random.random()
        if rand < percentage_chance and player.turn > 5:
            player.damage += self.monster_type.value[2]
            print(player.damage)
        print (rand, percentage_chance)


class EntityModel:
    """Class tracking the entities within the dungeon game."""

    def __init__(self, game: GameLevel) -> None:
        """Initialise the entities."""
        self.entities_list: list[Monster] = []
        self.game = game

    def add_entities(self, entity: Monster) -> None:
        """Store all of the entities in the current level."""
        self.entities_list.append(entity)

    def list_taken_positions(self) -> list[tuple[int, int]]:
        """Provide a list of every filled position by a Monster."""
        filled_positions: list[tuple[int, int]] = []
        for mon in self.entities_list:
            filled_positions.append(mon.position)
        return filled_positions

    def generate_monsters(self, game: GameLevel) -> None:
        """Generate the monsters needed for that level."""
        self.entities_list.clear()
        # Only include all monsters for the MAX level of the game
        if game.current_level == game.max_level:
            types = [monsters for monsters in EntitySubType]
        else:
            types = [
                monsters
                for monsters in EntitySubType
                if monsters.name not in ("GOBLIN_KING")
            ]
        # Create decreasing weights based on position
        weights = list(range(len(types), 0, -1))
        for num in range(DIFFICULTY_EXP[game.difficulty]):
            # Select one random enum member favoring earlier items
            chosen_type = random.choices(types, weights=weights, k=1)[0]
            monster = Monster(game, game.random_position(), chosen_type)
            monster.set_reference_id(num)
            self.add_entities(monster)

    def monsters_attack(self, player: Player) -> None:
        """Each Monster has a turn to attack the player."""
        player_pos: tuple[int, int] = player.position
        for monster in self.entities_list:
            if monster.check_player_distance(player_pos, 2):
                monster.attack_player(player)

    def move_monsters(self, player: Player) -> None:
        """Move all monsters to new valid grid coordinates."""
        player_pos: tuple[int, int] = player.position
        for monster in self.entities_list:
            filled_positions = self.list_taken_positions()
            valid_movement = False
            bfs = False
            if monster.check_player_distance(player_pos, PLAYER_CHASE_DISTANCE):
                monster.visible = True
                bfs = True
            if bfs:
                path = monster.bfs_pathfinder(player_pos)
                next_pos = monster.position
                if path is not None:
                    result = path[-2:-1]
                    check_next_pos = result[0] if result else None
                    if (
                        isinstance(check_next_pos, (tuple))
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
                            if (
                                self.game.validate_nonplayer_update(new_row, new_col)
                                and (new_row, new_col) not in filled_positions
                            ):
                                monster.position = (new_row, new_col)
                                valid_movement = True
                    if not valid_movement:
                        # give the whileloop a way out if there are no feasible moves
                        break

    def monster_stats(self) -> str:
        """Generate a list of the monster stats."""
        stats: str = ""
        for mon in self.entities_list:
            if mon.visible:
                name = mon.monster_type.value[0]
                hp = mon.monster_type.value[1]
                hp_remaining = mon.hit_points
                stats = stats + (
                    f"\n    ID:  {mon.id_refererence}    {name}\n"
                    f"        - HP: {hp_remaining} / {hp}\n"
                )
        return stats

    def check_monsters_health(self) -> None:
        """Ensure all monsters health is still valid."""
        for mon in self.entities_list:
            if mon.hit_points <= 0:
                self.entities_list.remove(mon)
