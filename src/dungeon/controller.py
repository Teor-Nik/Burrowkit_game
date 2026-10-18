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
        self.init_level(self.return_to_prev_map)
        self.start_game()

    def init_level(self, movement: bool) -> None:
        """Initialise the level."""
        # Create a GameRenderer instance
        self.game_renderer = renderer.GameRenderer()
        # Create a GameLevel instance with the first level map
        self.game_model = level.GameLevel(self.current_level)
        self.game_model.determain_start_position(self.current_level, movement)
        self.game_model.build_grid_initial(
            self.current_level
        )
        self.game_renderer.draw_level(self.game_model.level)
        self.player = entities.Player(self.game_model, self.game_model.coordinates)
        self.return_to_prev_map = False  # reset value

    def start_game(self) -> None:
        """Start the game."""
        # Main game loop
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(60)
            if self.game_model.level_number != self.current_level:
                self.init_level(self.return_to_prev_map)
            self.game_renderer.draw_entity(self.player.type, self.player.position)
            # Render the game window
            self.game_renderer.reload_game_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    self.player.player_move_coords(self.player.position, key_name)
                    if self.game_model.is_returned_to_entrace(self.player.position):
                        if self.game_model.returned_to_entrace():
                            # player returning to previous map
                            self.return_to_prev_map = True
                            self.current_level -= 1
                    if self.game_model.is_stairs(self.player.position):
                        if self.game_model.stairs_reached():
                            self.current_level += 1
                    if self.game_model.is_goal(self.player.position):
                        if self.game_model.goal_reached():
                            print("END GAME!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    self.game_renderer.draw_level(self.game_model.level)
        # Quit Pygame
        pygame.quit()
