"""Burrowkit Game: Tests the level/map functionality and validation."""

import pytest

from dungeon.model.level import GameLevel, Tile

LEVEL_TESTING_MAP = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 9, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

map_list: dict[int, list[list[int]]] = {1: LEVEL_TESTING_MAP}


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_map_rows(level: int) -> None:
    """Test that each row has the same length for all maps."""
    game = GameLevel(level, None)
    all_lengths = []
    for row_pos, row in enumerate(game.level):
        row_length = len(row)
        all_lengths.append(row_length)
    unique_values = list(set(all_lengths))
    assert unique_values == [20]


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_map_sizes(level: int) -> None:
    """Test that each map has the same overall size."""
    game = GameLevel(level, None)
    all_lengths = 0
    for row_pos, row in enumerate(game.level):
        all_lengths += len(row)
    assert all_lengths == 400


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_cells_in_maps(level: int) -> None:
    """Test that all tiles in the maps are legitimate tiles."""
    game = GameLevel(level, None)
    match = all(
        isinstance(tile, Tile) for row_tiles in game.level for tile in row_tiles
    )
    assert match


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_maxlevel_has_goals(level: int) -> None:
    """Test that the final level has a goal, but all others do not."""
    game = GameLevel(level, None)
    expected_result = []
    if game.max_level == level:
        expected_result = [Tile.GOAL]
    goals = []
    for row_pos, row_tiles in enumerate(game.level):
        for col_pos, tile in enumerate(row_tiles):
            if tile == Tile.GOAL:
                goals.append(tile)
    assert goals == expected_result


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_every_level_has_entrance(level: int) -> None:
    """Test that each map has an entrance."""
    game = GameLevel(level, None)
    entrances = []
    for row_pos, row_tiles in enumerate(game.level):
        for col_pos, tile in enumerate(row_tiles):
            if tile == Tile.ENTRANCE:
                entrances.append(Tile.ENTRANCE)
    assert entrances == [Tile.ENTRANCE]


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_every_level_has_stairs(level: int) -> None:
    """Test that each map has a set of stairs to the next map, excluding final level."""
    game = GameLevel(level, None)
    expected_result = [Tile.STAIR]
    if game.max_level == level:
        expected_result = []
    stairs = []
    for row_pos, row_tiles in enumerate(game.level):
        for col_pos, tile in enumerate(row_tiles):
            if tile == Tile.STAIR:
                stairs.append(Tile.STAIR)
    assert stairs == expected_result


def test_cells_in_malformed_map() -> None:
    """Test that a malformed map is flagged."""
    with pytest.raises(ValueError, match="not found"):
        GameLevel(1, map_list)
