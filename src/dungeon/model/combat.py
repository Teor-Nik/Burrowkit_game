"""Burrowkit Game Dungeon combat."""


from dungeon.model.level import GameLevel


class Combat:
    """The base Combat class for entities to use for combat."""

    def __init__(self, game: GameLevel) -> None:
        """Initialise Combat."""
        self.game = game
