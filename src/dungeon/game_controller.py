"""Burrowkit Game: Dungeon Controller."""

import pygame

from dungeon.model import entities, entities_monster, entities_player, level
from dungeon.view import renderer

DIRECTION_MAP: dict[int, entities.Direction] = {
    pygame.K_UP: entities.Direction.UP,
    pygame.K_w: entities.Direction.UP,
    pygame.K_DOWN: entities.Direction.DOWN,
    pygame.K_s: entities.Direction.DOWN,
    pygame.K_LEFT: entities.Direction.LEFT,
    pygame.K_a: entities.Direction.LEFT,
    pygame.K_RIGHT: entities.Direction.RIGHT,
    pygame.K_d: entities.Direction.RIGHT,
}

ATTACK_MAP: dict[int, entities.EntityAttack] = {
   pygame.K_1: entities.EntityAttack.PUNCH,
   pygame.K_KP1: entities.EntityAttack.PUNCH,
   pygame.K_2: entities.EntityAttack.STAB,
   pygame.K_KP2: entities.EntityAttack.STAB,
   pygame.K_3: entities.EntityAttack.SLASH,
   pygame.K_KP3: entities.EntityAttack.SLASH,
   pygame.K_4: entities.EntityAttack.IRON_JAB,
   pygame.K_KP4: entities.EntityAttack.IRON_JAB,
   pygame.K_5: entities.EntityAttack.BLADE_RUSH,
   pygame.K_KP5: entities.EntityAttack.BLADE_RUSH,
}

class GameController:
    """Class responsible for controlling the game flow."""

    def __init__(
        self, level_model: level.GameLevel, view_renderer: renderer.GameRenderer
    ) -> None:
        """Initialize the game controller."""
        self.level_model = level_model
        self.view = view_renderer
        self.monsters_list: list[entities_monster.Monster] = []
        self.entities_list: list[entities.Entity] = []
        self.player = entities_player.Player(
            self.level_model, self.level_model.start_position, len(self.entities_list)
        )
        self.entities_list.append(self.player)
        self.generate_monsters()
        self.current_turn = 1
        self.monster_turn = None

    def list_taken_positions(self) -> list[tuple[int, int]]:
        """Provide a list of every filled position by a Monster."""
        filled_positions: list[tuple[int, int]] = []
        for mon in self.monsters_list:
            filled_positions.append(mon.position)
        return filled_positions

    def check_monsters_health(self) -> None:
        """Ensure all monsters health is still valid."""
        for mon in self.monsters_list:
            if mon.hp <= 0:
                self.monsters_list.remove(mon)

    def generate_monsters(self) -> None:
        """Generate the monsters needed for that level."""
        self.monsters_list.clear()
        current_difficulty = self.level_model.difficulty
        for num_monsters in range(level.DIFFICULTY_EXP[current_difficulty]):
            monster = entities_monster.Monster(
                self.level_model,
                self.level_model.random_position(),
                len(self.entities_list)
            )
            self.monsters_list.append(monster)
            self.entities_list.append(monster)

    def get_next_monster(
            self, current_mon: entities_monster.Monster | None
    ) -> None:
        """Get the next monster to move."""
        max_mons = len(self.monsters_list) - 1
        print ("max monsters: " , max_mons)
        self.monster_turn = next(
            (mon for mon in self.monsters_list if not mon.move_processed),
            None
        )
        for idx, current in enumerate(self.monsters_list):
            print ("idx monster: " , idx)
            if current == self.monster_turn and max_mons == idx:
                self.current_turn = 3

    def reset_all_monster_turns(self) -> None:
        """Reset all of the monster moves to process next turn."""
        for idx, current in enumerate(self.monsters_list):
            print ("resetting: " , idx)
            current.move_processed = False

    def start_game(self) -> None:
        """Start the game."""
        try:
            clock = pygame.time.Clock()
            while not self.level_model.game_finished:
                clock.tick(60)
                # Draw Quadrants
                self.view.draw_quadrants()
                # Draw Level
                self.view.draw_level(self.level_model.level)
                # Draw the Player
                self.view.draw_entity(self.player.creature, self.player.position)
                # Check the monsters heath before possibly starting their turn
                self.check_monsters_health()
                print("Current Turn:   ", self.current_turn)
                # If it is not the players turn run thropgh the next monsters turn
                if self.current_turn >= 2:
                    self.get_next_monster(self.monster_turn)
                    print("Monster check:   ", self.monster_turn)
                    # Move the Monster to a non-taken position is possible
                    if self.player.turn > 5 and self.monster_turn is not None:
                        self.monster_turn.move_monster(
                            self.player.position, self.list_taken_positions()
                        )
                        # Get the monsters attack attempt if possible
                        attack: int = self.monster_turn.attack_player(self.player.position)
                        # Process the players damage
                        self.player.damage += attack
                    # If there's no monster actions to process move to Player
                    else:
                        self.current_turn = 1
                        print ("PLAYERS TURN AGAIN")
                # If there's no more monsters left to process move to Player
                if self.current_turn == 3:
                    self.current_turn = 1
                    self.reset_all_monster_turns()
                # Draw the monsters
                for mon in self.monsters_list:
                    # print(mon.creature.name)
                    if mon.visible:
                        self.view.draw_entity(
                            mon.creature, mon.position
                        )
                # Get and render the current player status
                player_stats_text = (
                    f"{self.player.player_stats()}"
                )
                self.view.render_panel(
                    self.view.panel.PLAYER_STATS, "Player", player_stats_text
                )
                # Get and render the Kits status
                self.view.render_panel(
                    self.view.panel.KIT_STATS,
                    "Kit",
                    "Kit details will go here for stats.",
                )
                # For each monster, get their status
                status_text: str = ""
                for mon in self.monsters_list:
                    if mon.visible:
                        status_text += mon.monster_stats()
                # Get and render the game/monster status
                game_progress_text = (
                    f"\nGame Level:   {self.level_model.current_level}\n"
                    f"Level Difficulty Rating:   "
                    f"{self.level_model.difficulty.value[1]}"
                    f"\n\nMonster(s):{status_text}"
                )
                self.view.render_panel(
                    self.view.panel.PROGRESS, "Game Progress", game_progress_text
                )
                # Render the game window
                self.view.reload_game_window()
                # Enter the players turn
                while self.current_turn == 1:
                    # Get the input key from the user
                    player_moved = False
                    player_attacked = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.level_model.end_game()
                        elif event.type == pygame.KEYDOWN:
                            # If a key is pressed then attempt move
                            try:
                                # check if the key is a directional move
                                pressed_key = DIRECTION_MAP[event.key]
                                curr_level = self.level_model.current_level
                                taken = self.list_taken_positions()
                                self.player.move_direction(pressed_key, taken)
                                if curr_level != self.level_model.current_level:
                                    self.generate_monsters()
                                player_moved = True
                            except KeyError as x:
                                # This block runs if the key is missing
                                self.view.show_log(f"Key not mapped to movement:"
                                                f" {str(x)}")
                            try:
                                # check if the key is an attack move
                                attack_key = ATTACK_MAP[event.key]
                                taken = self.list_taken_positions()
                                self.player.attack_monster(
                                    attack_key, self.monsters_list
                                )
                                self.check_monsters_health()
                                player_attacked = True
                            except KeyError as x:
                                # This block runs if the key is missing
                                self.view.show_log(
                                    f"Attack Key not mapped to movement:"
                                    f" {str(x)}"
                                )
                    if player_moved or player_attacked:
                            self.current_turn += 1

        except ValueError as e:
            self.view.show_error(str(e))
        # Quit Pygame
