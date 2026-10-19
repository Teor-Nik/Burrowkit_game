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
        self.game_model.determain_start_position(
            self.current_level, self.return_to_prev_map
        )
        self.game_model.build_grid_initial(self.current_level)
        self.game_renderer.draw_level(self.game_model.level)
        self.player = entities.Player(self.game_model, self.game_model.coordinates)
        self.return_to_prev_map = False  # reset value
        self.redraw_map = False

    def start_game(self) -> None:
        """Start the game."""
        # Main game loop
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            if self.redraw_map:
                self.init_level()
            self.game_renderer.draw_entity(self.player.type, self.player.position)
            # Render the game window
            self.game_renderer.reload_game_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    if self.player.player_move_coords(self.player.position, key_name):
                        if self.game_model.tile_at(
                            self.player.position[0],
                            self.player.position[1],
                            self.game_model.tiles.ENTRANCE
                        ):
                            if self.game_model.returned_to_entrace(self.current_level):
                                # player returning to previous map
                                self.return_to_prev_map = True
                                self.current_level -= 1
                                self.redraw_map = True
                        if self.game_model.tile_at(
                            self.player.position[0],
                            self.player.position[1],
                            self.game_model.tiles.STAIR
                        ):
                            if self.game_model.stairs_reached(self.current_level):
                                self.current_level += 1
                                self.redraw_map = True
                        if self.game_model.tile_at(
                            self.player.position[0],
                            self.player.position[1],
                            self.game_model.tiles.GOAL
                        ):
                            if self.game_model.goal_reached(self.current_level):
                                print("END GAME!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                running = False
                    self.game_renderer.draw_level(self.game_model.level)
        # Quit Pygame
        pygame.quit()
