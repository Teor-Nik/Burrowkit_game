"""Burrowkit Game: Dungeon Controller."""

import pygame

from dungeon.model import entities, level
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


ATTACK_MAP: dict[int, entities.PlayerAttack] = {
   pygame.K_1: entities.PlayerAttack.PUNCH,
   pygame.K_KP1: entities.PlayerAttack.PUNCH,
   pygame.K_2: entities.PlayerAttack.STAB,
   pygame.K_KP2: entities.PlayerAttack.STAB,
   pygame.K_3: entities.PlayerAttack.SLASH,
   pygame.K_KP3: entities.PlayerAttack.SLASH,
   pygame.K_4: entities.PlayerAttack.IRON_JAB,
   pygame.K_KP4: entities.PlayerAttack.IRON_JAB,
   pygame.K_5: entities.PlayerAttack.BLADE_RUSH,
   pygame.K_KP5: entities.PlayerAttack.BLADE_RUSH,
}

class GameController:
    """Class responsible for controlling the game flow."""

    def __init__(
        self, level_model: level.GameLevel, view_renderer: renderer.GameRenderer
    ) -> None:
        """Initialize the game controller."""
        self.level_model = level_model
        self.view = view_renderer
        self.monster_tracker = entities.EntityModel(level_model)
        self.player = entities.Player(self.level_model, self.level_model.start_position)
        self.monster_tracker.generate_monsters(self.level_model)

    def start_game(self) -> None:
        """Start the game."""
        try:
            clock = pygame.time.Clock()
            while not self.level_model.game_finished:
                clock.tick(60)
                self.view.draw_quadrants()
                self.view.draw_level(self.level_model.level)
                self.view.draw_entity(self.player.creature, None, self.player.position)
                if not self.player.player_turn:
                    self.monster_tracker.move_monsters(self.player.position)
                for mon in self.monster_tracker.entities_list:
                    if mon.visible:
                        self.view.draw_entity(
                            mon.creature, mon.monster_type, mon.position
                        )
                self.player.player_turn = True
                player_stats_text = (
                    "Player details will go here for stats.\n"
                    f"Player turn counter: {self.player.turn}. "
                    f"{self.player.player_stats()}"
                )
                self.view.render_panel(
                    self.view.panel.PLAYER_STATS, "Player", player_stats_text
                )
                self.view.render_panel(
                    self.view.panel.KIT_STATS,
                    "Kit",
                    "Kit details will go here for stats.",
                )
                game_progress_test = (
                    f"Game progress so far - Level: {self.level_model.current_level}.\n"
                    f"Difficulty Rating: {self.level_model.difficulty.value[1]}\n"
                    f"Monster(s): {self.monster_tracker.monster_stats()}"
                )
                self.view.render_panel(
                    self.view.panel.PROGRESS, "Game Progress", game_progress_test
                )
                # Render the game window
                self.view.reload_game_window()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.level_model.end_game()
                    elif event.type == pygame.KEYDOWN:
                        try:
                            pressed_key = DIRECTION_MAP[event.key]
                            curr_level = self.level_model.current_level
                            taken = self.monster_tracker.list_taken_positions()
                            self.player.move_direction(pressed_key, taken)
                            if curr_level != self.level_model.current_level:
                                self.monster_tracker.generate_monsters(self.level_model)
                        except KeyError as x:
                            # This block runs if the key is missing
                            self.view.show_log(f"Key not mapped to movement: {str(x)}")
                        try:
                            attack_key = ATTACK_MAP[event.key]
                            taken = self.monster_tracker.list_taken_positions()
                            self.player.attack_monster(attack_key, self.monster_tracker.entities_list)
                            self.monster_tracker.check_monsters_health()
                        except KeyError as x:
                            # This block runs if the key is missing
                            self.view.show_log(f"Attack Key not mapped to movement: {str(x)}")
        except ValueError as e:
            self.view.show_error(str(e))
        # Quit Pygame
        pygame.quit()
