"""Entities of a Player Sub-Class."""

from dungeon.model import entities
from dungeon.model.entities import (
    Entity,
    EntityAttack,
    EntityType,
)
from dungeon.model.entities_monster import Monster
from dungeon.model.level import GameLevel


class Player(Entity):
    """Class representing a player in the dungeon game."""

    creature = EntityType.PLAYER

    def __init__(self, game: GameLevel, position: tuple[int, int], id: int) -> None:
        """Initialise the Player."""
        super().__init__(game, position, id)
        self.creature = EntityType.PLAYER
        self.position = position

    def player_stats(self) -> str:
        """Generate a list of the monster stats."""
        required_exp = self.level * entities.EXP_MULTIPLIER
        current_damage = self.max_hp - self.damage
        attackmoves: str = ""
        filtered_list = self.attack_moves()
        if filtered_list is not None:
            for attack in filtered_list:
                attackmoves += (
                    f"    - {attack.value[0]}  "
                    f"({attack.value[1]})\n"
                )
        stats: str = (
            f"\nLevel:   {self.level}\n"
            f"\n    Exp:   {self.experience} / {required_exp}.\n"
            f"\n    Health:   {current_damage} / {self.max_hp}\n"
            f"\nAttack Moves   (damage):\n{attackmoves}"
        )
        return stats

    def attack_monster(
            self, attack_key: EntityAttack, monsters: list["Monster"]
    ) -> bool:
        """Attack the nearest adjacent Monster."""
        print("Attack!")
        attack_made = False
        filtered_list = self.attack_moves()
        if filtered_list is not None:
            for move in filtered_list:
                monsters.sort(key=lambda obj: obj.hp)
                for mon in monsters:
                    if not attack_made:
                        if self.check_distance(mon.position):
                            # print(mon.monster_type.value[0], mon.hp)
                            mon.take_damage(attack_key.value[1])
                            attack_made = True
                            if mon.fainted:
                                self.increase_exp(mon.monster_type.value[2])
        return attack_made

