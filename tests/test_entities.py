"""Burrowkit Game: Tests the entities functionality."""

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

map_list: dict[int, list[list[int]]] = {
    1: MOVEMENT_TESTING_MAP,
    2: LVL2_TESTING_MAP,
    3: LVLFIN_TESTING_MAP,
}

invalid_map_list: dict[int, list[list[int]]] = {
    1: INVALIDMOVEMENT_TESTING_MAP
}

goalmap_list: dict[int, list[list[int]]] = {
   1: LVLFIN_TESTING_MAP
}


@pytest.fixture
def custom_goalmap_game():
    """Load the game and player."""
    game = GameLevel(1, goalmap_list)
    return game


@pytest.fixture
def custom_goalplayer(custom_goalmap_game):
    """Load the game and player."""
    player = entities.Player(custom_goalmap_game, custom_goalmap_game.start_position)
    return player


@pytest.fixture
def custom_map_game():
    """Load the game and player."""
    game = GameLevel(1, map_list)
    return game


@pytest.fixture
def custom_player(custom_map_game):
    """Load the game and player."""
    player = entities.Player(custom_map_game, custom_map_game.start_position)
    return player

@pytest.fixture
def custom_map5_game():
    """Load the game and player."""
    game = GameLevel(1, invalid_map_list)
    return game


@pytest.fixture
def custom_player_map5(custom_map5_game):
    """Load the game and player."""
    player = entities.Player(custom_map5_game, custom_map5_game.start_position)
    return player

@pytest.mark.parametrize("movement", ['down', 'up', 'left', 'right'])
def test_basic_movement(custom_player, movement: str) -> None:
    """Test that each row has the same length for all maps."""
    valid = custom_player.move_direction(movement)
    assert valid


@pytest.mark.parametrize("movement", ['down', 'up', 'left', 'right'])
def test_movement_into_wall(custom_player_map5, movement: str) -> None:
    """Test that each row has the same length for all maps."""
    valid = custom_player_map5.move_direction(movement)
    assert not valid

def test_level_up(custom_player, custom_map_game) -> None:
    """Test that each row has the same length for all maps."""
    curr_level_check = custom_map_game.current_level
    valid = False
    for x in range(1, 3):
        custom_player.move_direction('left')
    if custom_map_game.tile_at(
        custom_player.position[0],
        custom_player.position[1]
    ) == Tile.ENTRANCE:
        if custom_map_game.current_level -1 == curr_level_check:
            valid = True
    assert valid

def test_goal_reached(custom_goalplayer, custom_goalmap_game) -> None:
    """Test that each row has the same length for all maps."""
    valid = False
    for x in range(1, 12):
        custom_goalplayer.move_direction('left')
    if custom_goalmap_game.game_finished:
        valid = True
    assert valid

def test_entrance_first_level(custom_player, custom_map_game) -> None:
    """Test that each row has the same length for all maps."""
    curr_level_check = custom_map_game.current_level
    valid = False
    moved = False
    while not moved:
        moved = custom_player.move_direction('left')
        moved = custom_player.move_direction('right')
        moved = custom_player.move_direction('up')
        moved = custom_player.move_direction('down')

    while custom_player.position != custom_map_game.start_position:
        if custom_player.position[0] > custom_map_game.start_position[0]:
            custom_player.move_direction('up')
        if custom_player.position[0] < custom_map_game.start_position[0]:
            custom_player.move_direction('down')
        if custom_player.position[1] > custom_map_game.start_position[1]:
            custom_player.move_direction('left')
        if custom_player.position[1] < custom_map_game.start_position[1]:
            custom_player.move_direction('right')
    if custom_map_game.tile_at(
        custom_player.position[0],
        custom_player.position[1]
    ) == Tile.ENTRANCE:
        if custom_map_game.current_level == curr_level_check:
            valid = True
    assert valid

@pytest.mark.parametrize("movement", ['k', 'd', '5', ' '])
def test_other_key_used(custom_player, movement: str) -> None:
    """Test that each row has the same length for all maps."""
    valid = custom_player.move_direction(movement)
    assert not valid
