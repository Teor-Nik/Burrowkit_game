"""GUI tests: checks the maps build."""

import pytest

from dungeon.model.level import GameLevel, Tile


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_row_length_all_maps(level: int) -> None:
    """Test that each row has the same length for all maps."""
    game = GameLevel()
    all_lengths = []
    for row in game.rawlevel_list[level]:
        row_length = len(row)
        all_lengths.append(row_length)
    unique_values = list(set(all_lengths))
    assert unique_values == [20]


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_full_size_all_maps(level: int) -> None:
    """Test that each map has the same overall size."""
    game = GameLevel()
    all_lengths = 0
    for row in game.rawlevel_list[level]:
        all_lengths += len(row)
    assert all_lengths == 400


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_all_cells_all_maps(level: int):
    """Test that all tiles in the maps are legitemate tiles."""
    game = GameLevel()
    match_tile: int = -1
    for row in game.rawlevel_list[level]:
        for col in row:
            match_tile = game.tiles(col).value
    assert match_tile in {0, 1, 2, 3, 4}


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_one_goal_all_maps(level: int) -> None:
    """Test that the final level has a goal, but all others do not."""
    game = GameLevel()
    expected_result = []
    if len(game.rawlevel_list) == level:
        expected_result = [Tile.GOAL]
    game.current_level = level
    game.build_grid()
    goals = []
    for row in game.level:
        for col in row:
            if col == Tile.GOAL:
                goals.append(col)
    assert goals == expected_result


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_one_entrance_per_map(level: int) -> None:
    """Test that each map has an entrance."""
    game = GameLevel()
    level_map = game.rawlevel_list[level]
    entrances = []
    for row in level_map:
        for col in row:
            if col == Tile.ENTRANCE.value:
                entrances.append(Tile.ENTRANCE)
    assert entrances == [Tile.ENTRANCE]


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_one_stairs_per_map(level: int) -> None:
    """Test that each map has a set of stairs to the next map, excluding final level."""
    game = GameLevel()
    level_map = game.rawlevel_list[level]
    expected_result = [Tile.STAIR]
    if len(game.rawlevel_list) == level:
        expected_result = []
    stairs = []
    for row in level_map:
        for col in row:
            if col == Tile.STAIR.value:
                stairs.append(Tile.STAIR)
    assert stairs == expected_result
