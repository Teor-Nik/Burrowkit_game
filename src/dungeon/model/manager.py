"""Manager of all Entities and Items for the Controller."""

from dungeon.model import entities, entities_monster, items, level
from dungeon.model.level import GameLevel


class Manager:
    """Class that manages Entities in the dungeon."""

    def __init__(self, game: GameLevel) -> None:
        """Initialise an Entity."""
        self.game = game
        self.monsters_list: list[entities_monster.Monster] = []
        self.entities_list: list[entities.Entity] = []
        self.items_list: list[items.Item] = []
        self.monster_count = len(self.monsters_list)
        self.entities_count = len(self.entities_list)

    def add_entity(self, entity:entities.Entity) -> None:
        """Add an entity to the master lists."""
        self.entities_list.append(entity)
        self.entities_count = len(self.entities_list)

    def add_monster(self, monster:entities_monster.Monster) -> None:
        """Add an monster to the master lists."""
        self.monsters_list.append(monster)
        self.monster_count = len(self.monsters_list)

    def add_item(self, item:items.Item) -> None:
        """Add an item to the master lists."""
        self.items_list.append(item)

    def check_monsters_health(self) -> None:
        """Ensure all monsters health is still valid."""
        for mon in self.monsters_list:
            if mon.hp <= 0:
                self.monsters_list.remove(mon)
                self.entities_list.remove(mon)

    def list_taken_positions(self) -> list[tuple[int, int]]:
        """Provide a list of every filled position by a Monster."""
        filled_positions: list[tuple[int, int]] = []
        for mon in self.entities_list:
            filled_positions.append(mon.position)
        return filled_positions

    def reset_all_monster_turns(self) -> None:
        """Reset all of the monster moves to process next turn."""
        for idx, current in enumerate(self.monsters_list):
            # print ("resetting: " , idx)
            current.move_processed = False

    def generate_monsters(self) -> None:
        """Generate the monsters needed for that level."""
        self.monsters_list.clear()
        current_difficulty = self.game.difficulty
        for _ in range(level.DIFFICULTY_EXP[current_difficulty]):
            monster = entities_monster.Monster(
                self.game,
                self.game.random_position(),
                len(self.entities_list)
            )
            self.add_monster(monster)
            self.add_entity(monster)

    def generate_items(self) -> None:
        """Generate the items needed for that level."""
        self.items_list.clear()
        current_difficulty = self.game.difficulty
        for _ in range(level.DIFFICULTY_EXP[current_difficulty]):
            item = items.Item(
                self.game,
                self.game.random_position()
            )
            self.add_item(item)
