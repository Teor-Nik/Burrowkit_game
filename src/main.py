"""Main entry point for the game application."""

# import section
from dungeon import game_controller
from dungeon.model import level
from dungeon.view import renderer


def main() -> None:
    """Burrowkit Game program."""
    # Create a new game instance
    model_level = level.GameLevel(1)
    view_renderer = renderer.GameRenderer()
    controller = game_controller.GameController(model_level, view_renderer)
    controller.start_game()


# True only when this file is run directly
if __name__ == "__main__":
    main()
