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


class GameController:
    """Class responsible for controlling the game flow."""

    def __init__(
        self, level_model: level.GameLevel, view_renderer: renderer.GameRenderer
    ) -> None:
        """Initialize the game controller."""
        self.level_model = level_model
        self.view = view_renderer
        self.monster_tracker = entities.EntityModel()
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
                self.view.draw_entity(self.player.creature, self.player.position)
                if not self.player.player_turn:
                    for pos, entity in enumerate(self.monster_tracker.entities_list):
                        entity.move_direction()
                for mon in self.monster_tracker.entities_list:
                    self.view.draw_entity(mon.creature, mon.position)
                self.player.player_turn = True
                player_stats_text = (
                    "Player details will go here for stats.\n"
                    f"Player turn counter: {self.player.turn}. "
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
                    f"Difficulty Rating: {self.level_model.difficulty}"
                    f"Monster Positions: {self.monster_tracker.monster_stats()}"
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
                            self.player.move_direction(pressed_key)
                        except KeyError as x:
                            # This block runs if the key is missing
                            self.view.show_log(f"Key not mapped to movement: {str(x)}")
        except ValueError as e:
            self.view.show_error(str(e))
        # Quit Pygame
        pygame.quit()
