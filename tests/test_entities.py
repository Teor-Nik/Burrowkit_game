"""Burrowkit Game: Tests the entities functionality."""

import pygame
import pytest

from dungeon.model import entities
from dungeon.model.level import GameLevel, Tile

MOVEMENT_TESTING_MAP = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 3, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

LVL2_TESTING_MAP = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 3, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

LVLFIN_TESTING_MAP = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 3, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

INVALIDMOVEMENT_TESTING_MAP = [
    [1, 1, 1],
    [1, 3, 1],
    [1, 1, 1],
]

NOSIDES_TESTING_MAP = [
    [0, 0, 0],
    [0, 3, 0],
    [0, 0, 0],
]

map_list: dict[int, list[list[int]]] = {
    1: MOVEMENT_TESTING_MAP,
    2: LVL2_TESTING_MAP,
    3: LVLFIN_TESTING_MAP,
}


invalid_map_list: dict[int, list[list[int]]] = {1: INVALIDMOVEMENT_TESTING_MAP}


nosides_map_list: dict[int, list[list[int]]] = {1: NOSIDES_TESTING_MAP}


goalmap_list: dict[int, list[list[int]]] = {1: LVLFIN_TESTING_MAP}


@pytest.fixture
def custom_goalmap_game() -> GameLevel:
    """Load the game for the Goal testin custom maps."""
    game = GameLevel(1, goalmap_list)
    return game


@pytest.fixture
def custom_goalplayer(custom_goalmap_game) -> entities.Player:
    """Load the player for the Goal testin custom maps."""
    player = entities.Player(custom_goalmap_game, custom_goalmap_game.start_position)
    return player


@pytest.fixture
def custom_nosides_game() -> GameLevel:
    """Load the game for the custom map with no sides."""
    game = GameLevel(1, nosides_map_list)
    return game


@pytest.fixture
def custom_nosidesplayer(custom_nosides_game) -> entities.Player:
    """Load the player for the custom map with no sides."""
    player = entities.Player(custom_nosides_game, custom_nosides_game.start_position)
    return player


@pytest.fixture
def custom_map_game() -> GameLevel:
    """Load the game for the standard custom maps."""
    game = GameLevel(1, map_list)
    return game


@pytest.fixture
def custom_player(custom_map_game) -> entities.Player:
    """Load the player for the standard custom maps."""
    player = entities.Player(custom_map_game, custom_map_game.start_position)
    return player


@pytest.fixture
def custom_map5_game() -> GameLevel:
    """Load the game for the invalid map."""
    game = GameLevel(1, invalid_map_list)
    return game


@pytest.fixture
def custom_player_map5(custom_map5_game) -> entities.Player:
    """Load the player for the invalid map."""
    player = entities.Player(custom_map5_game, custom_map5_game.start_position)
    return player


@pytest.fixture
def custom_premax_level_game() -> GameLevel:
    """Load the game for the pre-max level test case."""
    game = GameLevel(2, map_list)
    return game


@pytest.fixture
def custom_player_premax(custom_premax_level_game) -> entities.Player:
    """Load the player for the pre-max level test case."""
    player = entities.Player(
        custom_premax_level_game, custom_premax_level_game.start_position
    )
    return player


@pytest.mark.parametrize(
    "movement",
    [
        entities.Direction.DOWN,
        entities.Direction.UP,
        entities.Direction.LEFT,
        entities.Direction.RIGHT,
    ],
)
def test_basic_movement(custom_player, movement: int) -> None:
    """Test that all basic movement is a valid move on map with space."""
    valid = custom_player.move_direction(movement)
    assert valid


@pytest.mark.parametrize(
    "movement",
    [
        entities.Direction.DOWN,
        entities.Direction.UP,
        entities.Direction.LEFT,
        entities.Direction.RIGHT,
    ],
)
def test_movement_into_wall(custom_player_map5, movement: int) -> None:
    """Test that all movement into a wall is invalid."""
    valid = custom_player_map5.move_direction(movement)
    assert not valid


def test_level_up(custom_player, custom_map_game) -> None:
    """Test moving the playing into Stairs levels up the game."""
    curr_level_check = custom_map_game.current_level
    for _ in range(1, 3):
        custom_player.move_direction(entities.Direction.LEFT)

    tile = custom_map_game.tile_at(custom_player.position[0], custom_player.position[1])
    new_level = custom_map_game.current_level - 1
    assert new_level == curr_level_check and tile == Tile.ENTRANCE


def test_goal_reached(custom_goalplayer, custom_goalmap_game) -> None:
    """Test that moving the player into the Goal finishes the game."""
    for _ in range(1, 12):
        custom_goalplayer.move_direction(entities.Direction.LEFT)
    result = custom_goalmap_game.game_finished
    assert result


def test_entrance_first_level(custom_player, custom_map_game) -> None:
    """Test that the first level entrance holds no functionality."""
    curr_level_check = custom_map_game.current_level
    moved = False
    while not moved:
        moved = custom_player.move_direction(entities.Direction.LEFT)
        moved = custom_player.move_direction(entities.Direction.RIGHT)
        moved = custom_player.move_direction(entities.Direction.UP)
        moved = custom_player.move_direction(entities.Direction.DOWN)

    while custom_player.position != custom_map_game.start_position:
        if custom_player.position[0] > custom_map_game.start_position[0]:
            custom_player.move_direction(entities.Direction.UP)
        if custom_player.position[0] < custom_map_game.start_position[0]:
            custom_player.move_direction(entities.Direction.DOWN)
        if custom_player.position[1] > custom_map_game.start_position[1]:
            custom_player.move_direction(entities.Direction.LEFT)
        if custom_player.position[1] < custom_map_game.start_position[1]:
            custom_player.move_direction(entities.Direction.RIGHT)
    tile = custom_map_game.tile_at(custom_player.position[0], custom_player.position[1])
    new_level = custom_map_game.current_level
    assert new_level == curr_level_check and tile == Tile.ENTRANCE


def test_all_levels_usable(custom_player_premax, custom_premax_level_game) -> None:
    """Test that each level can be traversed."""
    curr_level = custom_premax_level_game.current_level
    for _ in range(1, 3):
        custom_player_premax.move_direction(entities.Direction.LEFT)
    assert custom_premax_level_game.current_level > curr_level


@pytest.mark.parametrize(
    "movement",
    [
        entities.Direction.DOWN,
        entities.Direction.UP,
        entities.Direction.LEFT,
        entities.Direction.RIGHT,
    ],
)
def test_emptysides_reached(custom_nosidesplayer, movement: int) -> None:
    """Test that moving the player into the Goal finishes the game."""
    with pytest.raises(ValueError, match="Error: Map out of bounds error occurred."):
        for _ in range(1, 6):
            custom_nosidesplayer.move_direction(movement)
