"""Game Manager of all Entities and Items for the Controller."""

import itertools

from dungeon.model import (
    entities,
    entities_kit,
    entities_monster,
    entities_player,
    items,
    level,
)
from dungeon.model.level import GameLevel

FIRST_ENTITY_ID: int = 101

class Game:
    """Class that manages Entities in the dungeon."""

    def __init__(self, game: GameLevel) -> None:
        """Initialise an Entity."""
        self.game = game
        self._ids = itertools.count(FIRST_ENTITY_ID)
        self.monsters_list: list[entities_monster.Monster] = []
        self.items_list: list[items.Item] = []
        self.kit = entities_kit.Kit(
            self.game, self.game.start_position, next(self._ids)
        )
        self.player = entities_player.Player(
            self.game, self.game.start_position, next(self._ids)
        )
        self.turn = 0
        self.turns_since_spawn = 0
        self._generate_monsters()
        self._generate_items()

    def check_monsters_health(self) -> None:
        """Ensure all monsters health is still valid."""
        for mon in self.monsters_list:
            if mon.fainted:
                self.monsters_list.remove(mon)

    def list_taken_positions(self, exclude: entities.Entity | None = None) -> list[tuple[int, int]]:
        """Provide a list of every filled position by a Monster."""
        filled_positions: list[tuple[int, int]] = []
        filled_positions.clear()
        self.check_monsters_health()
        if self.kit is not exclude:
            filled_positions.append(self.kit.position)
        if self.player is not exclude:
            filled_positions.append(self.player.position)
        for mon in self.monsters_list:
            if mon is not exclude:
                filled_positions.append(mon.position)
        return filled_positions

    def reset_monster_turns_and_visibility(self, player_pos: tuple[int, int]) -> None:
        """Reset all of the monster moves to process next turn."""
        for idx, monster in enumerate(self.monsters_list):
            monster.move_processed = False
            monster.determine_visibility(player_pos)

# -- --------------------------------------------------------------------------
# -- Generation of entities and items, manage visibility
# -- --------------------------------------------------------------------------
    def _add_monster(self, monster:entities_monster.Monster) -> None:
        """Add an monster to the master lists."""
        self.monsters_list.append(monster)
        self.monster_count = len(self.monsters_list)

    def _add_item(self, item:items.Item) -> None:
        """Add an item to the master lists."""
        self.items_list.append(item)

    def _generate_monsters(self) -> None:
        """Generate the monsters needed for that level."""
        self.monsters_list.clear()
        current_difficulty = self.game.difficulty
        for _ in range(level.DIFFICULTY_EXP[current_difficulty]):
            monster = entities_monster.Monster(
                self.game,
                self.game.random_position(),
                next(self._ids)
            )
            self._add_monster(monster)

    def _generate_items(self) -> None:
        """Generate the items needed for that level."""
        self.items_list.clear()
        current_difficulty = self.game.difficulty
        for _ in range(level.DIFFICULTY_EXP[current_difficulty]):
            item = items.Item(
                self.game,
                self.game.random_position()
            )
            self._add_item(item)

    def _update_visibility(self) -> None:
        """Reveal monsters and items near the player."""
        for monster in self.monsters_list:
            monster.determine_visibility(self.player.position)
        for item in self.items_list:
            near = entities.grid_distance(item.position, self.player.position) <= entities_monster.PLAYER_CHASE_DISTANCE
            if not item.used and near:
                item.visible = True
            else:
                item.visible = False

# -- --------------------------------------------------------------------------
# -- External turn mangement and processing of the game is handled in the controller.
# -- --------------------------------------------------------------------------
    def player_move(self, direction: entities.Direction) -> bool:
        """Move the player one tile. Returns True if a turn was used."""
        floor_before = self.game.current_level
        moved = self.player.move_direction(
            direction, self.list_taken_positions(exclude=self.player)
        )
        if not moved:
            return False
        if self.game.game_finished:
            return True
        if self.game.current_level != floor_before:
            # self._record(FloorChanged(self.game.current_level))
            self.kit.position = self.player.position
            self._generate_monsters()
            self._generate_items()
        else:
            for item in self.items_list:
                if not item.used and item.position == self.player.position:
                    item.status_check(self.player)
            self.kit.move_kit(self.player.position, self.list_taken_positions())
        self._end_player_turn()
        return True

    def player_attack(self, attack: entities.EntityAttack) -> bool:
        """Attack an adjacent monster. Returns True if a turn was used."""
        result = self.player.attack_monster(attack, self.monsters_list)
        if result is None:
            return False
        self._end_player_turn()
        return True

# -- --------------------------------------------------------------------------
# -- Internal turn mangement and processing of the game is handled in the controller.
# -- --------------------------------------------------------------------------
    def _end_player_turn(self) -> None:
        """Finish the player's turn: faint check, monsters act, update visibility."""
        self.turn += 1
        self.turns_since_spawn += 1
        if self.player.fainted:
            self.health_msg = "You FAINTED! Returning to start position."
            self._handle_faint()
        elif self.turns_since_spawn >= 5:
            self._monster_round()
        self._update_visibility()

    def _monster_round(self) -> None:
        """Let every monster move and attack, in order."""
        for monster in list(self.monsters_list):
            monster.take_turn(self.player, self.list_taken_positions())
            if self.player.fainted:
                self.health_msg = "You FAINTED! Returning to start position."
                self._handle_faint()
                return

    def _handle_faint(self) -> None:
        """Send the player back to the entrance and reset the floor."""
        self.player.fainted = False
        self.player.damage = round(self.player.max_hp / 4)
        self.player.position = self.game.start_position
        self.kit.position = self.player.position
        self.turns_since_spawn = 0
