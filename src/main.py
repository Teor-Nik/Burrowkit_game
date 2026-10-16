"""Main entry point for the game application."""

# import section
from dungeon import controller


def main() -> None:
    """Burrowkit Game program."""
    # Create a new game instance
    controller.GameController()


# True only when this file is run directly
if __name__ == "__main__":
    main()
