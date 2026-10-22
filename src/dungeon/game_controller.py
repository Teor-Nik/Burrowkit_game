"""Burrowkit Game: Dungeon Controller."""

import pygame

from dungeon.model import entities, level
from dungeon.view import renderer


class GameController:
    """Class responsible for controlling the game flow."""

    def __init__(
        self, level_model: level.GameLevel, view_renderer: renderer.GameRenderer
    ) -> None:
        """Initialize the game controller."""
        self.level_model = level_model
        self.view = view_renderer
        self.player = entities.Player(self.level_model, self.level_model.start_position)

    def init_level(self) -> None:
        """Initialise the level."""
        self.view.draw_level(self.level_model.level)
        self.player = entities.Player(self.level_model, self.player.position)
        self.view.render_panel(
            self.view.panel.PLAYER_STATS,
            "Player",
            "Player details will go here for stats.",
        )
        self.view.render_panel(
            self.view.panel.KIT_STATS,
            "Kit",
            "Kit details will go here for stats.",
        )
        self.view.render_panel(
            self.view.panel.PROGRESS,
            "Game Progress",
            f"Game progress so far - Level: {self.level_model.current_level}.",
        )
        self.level_model.changed_level = False
        self.view.reload_game_window()

    def start_game(self) -> None:
        """Start the game."""
        try:
            clock = pygame.time.Clock()
            self.init_level()
            while not self.level_model.game_finished:
                clock.tick(60)
                if self.level_model.changed_level:
                    self.init_level()
                self.view.draw_entity_type(self.player.type, self.player.position)
                # Render the game window
                self.view.reload_game_window()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.level_model.end_game()
                    elif event.type == pygame.KEYDOWN:
                        key_name = pygame.key.name(event.key)
                        self.player.player_move_coords(self.player.position, key_name)
                        self.view.draw_level(self.level_model.level)
        except ValueError as e:
            self.view.show_error(str(e))
        # Quit Pygame
        pygame.quit()
