"""Burrowkit Game: Dungeon Controller."""

import pygame

from dungeon.model import entities, level
from dungeon.view import renderer


class GameController:
    """Class responsible for controlling the game flow."""

    def __init__(self) -> None:
        """Initialize the game controller."""
        self.current_level = 1
        self.return_to_prev_map = False
        self.redraw_map = False
        self.init_level()
        self.start_game()

    def init_level(self) -> None:
        """Initialise the level."""
        # Create a GameRenderer instance
        self.game_renderer = renderer.GameRenderer()
        # Create a GameLevel instance with the first level map
        self.game_model = level.GameLevel()
        coordinates = self.game_model.start_position(
            self.current_level, self.return_to_prev_map
        )
        self.game_model.build_grid(self.current_level)
        self.game_renderer.draw_level(self.game_model.level)
        self.player = entities.Player(self.game_model, coordinates)
        self.game_renderer.render_panel(self.game_renderer.panel.PLAYER_STATS, "Player", "Player details will go here for stats.")
        self.game_renderer.render_panel(self.game_renderer.panel.KIT_STATS, "Kit", "Kit details will go here for stats.")
        self.game_renderer.render_panel(self.game_renderer.panel.PROGRESS, "Game Progress", f"Game progress so far - Level: {self.current_level}.")

        self.return_to_prev_map = False  # reset value
        self.redraw_map = False

    def start_game(self) -> None:
        """Start the game."""
        # Main game loop
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            if self.redraw_map or self.return_to_prev_map:
                self.init_level()
            self.game_renderer.draw_EntityType(self.player.type, self.player.position)
            # Render the game window
            self.game_renderer.reload_game_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    if self.player.player_move_coords(self.player.position, key_name):
                        level_check = self.game_model.progress_valid(
                            self.current_level,
                            self.player.position[0],
                            self.player.position[1],
                        )
                        if level_check > 0 and level_check < self.current_level:
                            self.current_level = level_check
                            self.return_to_prev_map = True
                        elif level_check == self.current_level:
                            print("END GAME!!")
                            running = False
                        elif level_check > 0:
                            self.current_level = level_check
                            self.redraw_map = True
                    self.game_renderer.draw_level(self.game_model.level)
        # Quit Pygame
        pygame.quit()
