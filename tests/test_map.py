"""GUI tests: checks the maps build."""

import pytest

from dungeon.model.level import GameLevel


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_row_length_all_maps(level: int) -> None:
    """Test that each row has the same length for all maps."""
    game = GameLevel(level)
    lengths = {len(game.level)}
    print(lengths)
    assert lengths == {20}


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_full_size_all_maps(level: int) -> None:
    """Test that each map has the same overall size."""
    game = GameLevel(level)
    lengths = 0
    for w in game.level:
        lengths += len(w)
    assert lengths == 400


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_all_cells_all_maps(level: int):
    """Test that all tiles in the maps are legitemate tiles."""
    game = GameLevel(level)
    match_tile: int = -1
    for row in game.level:
        for tile in row:
            match_tile = tile.value
    assert match_tile in {0, 1, 2, 3, 4}


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_one_goal_all_maps(level: int) -> None:
    """Test that the final level has a goal, but all others do not."""
    game = GameLevel(level)
    level_map = game.check_level()
    expected_result = []
    if game.check_max_level() == level:
        expected_result = ["GOAL"]
    goals = []
    for row in level_map:
        for tile in row:
            if tile.name == "GOAL":
                goals.append(tile.name)
    assert goals == expected_result


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_one_entrance_per_map(level: int) -> None:
    """Test that each map has an entrance."""
    level_map = GameLevel(level).check_level()
    entrances = []
    for row in level_map:
        for tile in row:
            if tile.name == "ENTRANCE":
                entrances.append(tile.name)
    assert entrances == ["ENTRANCE"]


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_one_stairs_per_map(level: int) -> None:
    """Test that each map has a set of stairs to the next map, excluding final level."""
    game = GameLevel(level)
    level_map = game.check_level()
    expected_result = ["STAIR"]
    if game.check_max_level() == level:
        expected_result = []
    stairs = []
    for row in level_map:
        for tile in row:
            if tile.name == "STAIR":
                stairs.append(tile.name)
    assert stairs == expected_result
