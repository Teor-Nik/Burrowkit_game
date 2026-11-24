"""Burrowkit Game: Dungeon Controller."""


import pygame

from dungeon.model import (
    entities,
    entities_kit,
    entities_monster,
    entities_player,
    game,
    level,
)
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

MESSAGE_DISPLAY_TURNS: int = 5


class GameController:
    """Class responsible for controlling the game flow."""

    def __init__(
        self, level_model: level.GameLevel, view_renderer: renderer.GameRenderer
    ) -> None:
        """Initialize the game controller."""
        self.level_model = level_model
        self.view = view_renderer
        self.mgr = game.Game(self.level_model)
        # self.current_turn = 1
        # self.monster_turn = None
        self.game_msg: str = ""
        self.game_msg_counter: int = 0
        self.health_msg: str = ""
        self.health_msg_counter: int = 0
        # self.turn_number: int = 0

    def start_game(self) -> None:
        """Start the game."""
        try:
            clock = pygame.time.Clock()
            while not self.level_model.game_finished:
                self.reset_messages()
                clock.tick(60)
                # Draw Quadrants
                self.view.draw_quadrants()
                # Draw Level
                self.view.draw_level(self.level_model.level)
                # Draw the Player
                for item in self.mgr.items_list:
                    # self.mgr._update_visibility()
                    if item.visible:
                        self.view.draw_item(item.item_type, item.position)
                self.view.draw_entity(self.mgr.player.creature, self.mgr.player.position)
                # # If player not in KIT starting position draw Kit
                # if self.mgr.player.fainted:
                #     self.health_msg = "You FAINTED! Returning to start position."
                #     self.mgr.player.fainted = False
                if self.mgr.player.position != self.mgr.kit.position:
                    self.view.draw_entity(self.mgr.kit.creature, self.mgr.kit.position)
                # Check the monsters heath before possibly starting their turn
                # self.mgr.check_monsters_health()
                # If it is not the players turn run thropgh the next monsters turn
                # if self.current_turn >= 2:
                #     self.process_monsters_turn()
                # If there's no more monsters left to process move to Player
                # if self.current_turn == 3:
                #     self.current_turn = 1
                #     self.turn_number += 1
                #     self.mgr.reset_monster_turns_and_visibility(self.mgr.player.position)
                # Draw the monsters
                for mon in self.mgr.monsters_list:
                    if mon.visible:
                        self.view.draw_entity(
                            mon.creature, mon.position
                        )
                self.render_statuses()
                self.reset_messages()
                # Enter the players turn
                # while self.current_turn == 1:
                    # Get the input key from the user
                    # player_moved = False
                    # player_attacked = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.level_model.end_game()
                    elif event.type == pygame.KEYDOWN:
                        # If a key is pressed then attempt move
                        try:
                            direction = DIRECTION_MAP.get(event.key)
                            if direction is not None:
                                self.mgr.player_move(direction)
                            # player_moved = self.try_directional_move(event.key)
                        except KeyError as x:
                            # This block runs if the key is missing
                            self.view.show_log(f"Key not mapped to movement:"
                                            f" {str(x)}")
                        try:
                            attack = ATTACK_MAP.get(event.key)
                            if attack is not None:
                                self.mgr.player_attack(attack)
                            #   player_attacked = self.try_attack_move(event.key)
                        except KeyError as x:
                            # This block runs if the key is missing
                            self.view.show_log(
                                f"Attack Key not mapped to movement:"
                                f" {str(x)}"
                            )
                    # if player_moved or player_attacked:
                    #     self.mgr._end_player_turn()

        except ValueError as e:
            self.view.show_error(str(e))
        # Quit Pygame

    # def try_attack_move(self, key: int) -> bool:
    #     """Attempt to attack a nearby monster."""
    #     # check if the key is an attack move
    #     attack_key = ATTACK_MAP[key]
    #     attack_check = self.mgr.player.attack_monster(
    #         attack_key, self.mgr.monsters_list
    #     )
    #     self.mgr.check_monsters_health()
    #     return attack_check

    # def try_directional_move(self, key: int) -> bool:
    #     """Attempt to move the player in a direction."""
    #     # check if the key is a directional move
    #     pressed_key = DIRECTION_MAP[key]
    #     curr_level = self.level_model.current_level
    #     taken = self.mgr.list_taken_positions()
    #     player_moved = self.mgr.player.move_direction(
    #         pressed_key, taken
    #     )
    #     item_message: str | None = None
    #     for item in self.mgr.items_list:
    #         item_message = item.status_check(self.mgr.player)
    #         if item_message is not None:
    #             self.game_msg = item_message
    #             self.game_msg_counter = self.turn_number
    #     self.mgr.kit.move_kit(self.mgr.player.position, taken)
    #     if curr_level != self.level_model.current_level:
    #         self.mgr.generate_monsters()
    #         self.mgr.generate_items()
    #         self.mgr.kit.position = self.mgr.player.position
    #     return player_moved

    # def get_next_monster(
    #         self, current_mon: entities_monster.Monster | None
    # ) -> None:
    #     """Get the next monster to move."""
    #     max_mons = len(self.mgr.monsters_list) - 1
    #     self.monster_turn = next(
    #         (mon for mon in self.mgr.monsters_list if not mon.move_processed),
    #         None
    #     )
    #     for idx, current in enumerate(self.mgr.monsters_list):
    #         if current == self.monster_turn and max_mons == idx:
    #             self.current_turn = 3

    # def process_monsters_turn(self) -> None:
    #     """Process the monsters part of this turn."""
    #     self.get_next_monster(self.monster_turn)
    #     # Move the Monster to a non-taken position is possible
    #     if self.monster_turn is not None:
    #         self.monster_turn.move_monster(
    #             self.player.position, self.mgr.list_taken_positions()
    #         )
    #         # Get the monsters attack attempt if possible
    #         attack: int = self.monster_turn.attack_player(
    #             self.player.position
    #         )
    #         # Process the players damage
    #         self.player.take_damage(attack)
    #     # If there's no monster actions to process move to Player
    #     else:
    #         self.current_turn = 1

    def reset_messages(self):
        """Check if any of the game/health messages need to reset."""
        if self.mgr.turns_since_spawn - self.health_msg_counter == MESSAGE_DISPLAY_TURNS:
            self.health_msg = ""
        if self.mgr.turns_since_spawn - self.game_msg_counter == MESSAGE_DISPLAY_TURNS:
            self.game_msg = ""

    def render_statuses(self) -> None:
        """Render all needed stats."""
        # Get and render the current player status
        player_stats_text = (
            f"{self.mgr.player.player_stats()}\n{self.game_msg}\n{self.health_msg}"
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
        for mon in self.mgr.monsters_list:
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
