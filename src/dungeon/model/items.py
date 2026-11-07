"""Burrowkit Game Dungeon items."""


import random
from enum import Enum

from dungeon.model import entities_player
from dungeon.model.level import GameLevel


class ItemClass(Enum):
    """Item Class and Name."""

    FOOD = "Food"  ##  Both Health and EXP
    HEALTH = "Health"  ##  Just Health
    EXP = "EXP Boost"  ##  Just EXP
    DAMAGE = "Damage Dealer"  ##  Deals Damage

class ItemTypes(Enum):
    """Item Name, Type, Effect."""

    RED_BERRY = ("a Red Berry", ItemClass.FOOD, 5)
    YELLOW_BERRY = ("a Yellow Berry", ItemClass.EXP,  5)
    BREAD = ("Bread", ItemClass.FOOD,  10)
    POITION = ("a Poition", ItemClass.EXP,  10)
    GREEN_BERRY = ("a Green Berry", ItemClass.DAMAGE,  5)
    TRAP = ("a Trap Item", ItemClass.DAMAGE,  15)


EXP_MULTIPLIER: int = 8

class Item:
    """Class representing an Item within the dungeon game."""

    def __init__(self, game: GameLevel, position: tuple[int, int]) -> None:
        """Initialise an Entity."""
        self.game = game
        self.position = position
        self.item_type = self.item_generator()
        self.visible = False
        self.item_class = self.item_type.value[1]
        self.used = False

    def item_generator(self) -> ItemTypes:
        """Generate a item type/class needed for this level."""
        types = [
            item
            for item in ItemTypes
        ]
        weights = list(range(len(types), 0, -1))
        chosen_type = random.choices(types, weights=weights, k=1)[0]
        return chosen_type

    def status_check(self, player: entities_player.Player) -> str | None:
        """If the player has stepped on Item check impact."""
        player_impact: str | None = None
        if self.position == player.position and not self.used:
            player_impact = (
                f"You have picked up {self.item_type.value[0]}."
                f"This is a {self.item_class.value} class item. "
            )
            self.used = True
            self.visible = False
            exp_calc = self.item_type.value[2] * EXP_MULTIPLIER
            change_calc = self.item_type.value[2]
            print("AHH NO YOU STEPPED ON ME!!!")
            if self.item_class == ItemClass.FOOD:
                player.remove_damage(change_calc)
                player.increase_exp(exp_calc)
                player_impact += (
                    f"\n Your Health has gone up {change_calc} "
                    f"and your EXP has gone up {exp_calc}"
                )
            if self.item_class == ItemClass.HEALTH:
                player.remove_damage(change_calc)
                player_impact += (
                    f"\n Your Health has gone up {change_calc} "
                )
            if self.item_class == ItemClass.EXP:
                player.increase_exp(exp_calc)
                player_impact += (
                    f"\n Your EXP has gone up {exp_calc} "
                )
            if self.item_class == ItemClass.DAMAGE:
                player.take_damage(change_calc)
                player_impact += (
                    f"\n Your Health has gone down {change_calc} "
                )
        return player_impact
