"""Entities of a Player Sub-Class."""

from dungeon.model.entities import (
    ALLOWED_ATTACKS,
    HEALTH_MULTIPLIER,
    Entity,
    EntityAttack,
    EntityType,
)
from dungeon.model.entities_monster import Monster
from dungeon.model.level import GameLevel

EXP_MULTIPLIER: int = 100


class Player(Entity):
    """Class representing a player in the dungeon game."""

    def __init__(self, game: GameLevel, position: tuple[int, int], id: int) -> None:
        """Initialise the Player."""
        super().__init__(game, position, id)
        self.creature = EntityType.PLAYER
        self.position = position

    def increase_exp(self, monster_value: int) -> None:
        """Increase the player EXP based on level and monster killed."""
        self.experience += self.game.difficulty.value[0] * monster_value
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
            f"\n    Health:   {current_damage} / {self.hp}\n"
            f"\nAttack Moves   (damage):\n{attackmoves}"
        )
        return stats

    def attack_monster(
            self, attack_key: EntityAttack, monsters: list["Monster"]
    ) -> None:
        """Attack the nearest adjacent Monster."""
        print("Attack!")
        attack_made = False
        filtered_list = self.attack_moves()
        if filtered_list is not None:
            for move in filtered_list:
                print(move.value[0], move.value[3] , self.level)
                monsters.sort(key=lambda obj: obj.hp)
                for mon in monsters:
                    if not attack_made:
                        if self.check_distance(mon.position):
                            # print(mon.monster_type.value[0], mon.hp)
                            mon.hp -= attack_key.value[1]
                            attack_made = True
                            if mon.hp <= 0:
                                self.increase_exp(mon.monster_type.value[2])

