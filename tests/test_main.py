from pathlib import Path

from f1_fantasy.consts import QUALIFYING_ONLY, ROOT_DIR
from f1_fantasy.main import main


def test_main():
    test_data_root = ROOT_DIR.parent.parent / "tests" / "test_data"
    max_score_teams = main(
        driver_prices=Path(test_data_root / "driver_prices" / "20240301.csv"),
        constructor_prices=Path(test_data_root / "constructor_prices" / "20240301.csv"),
        qualifying_finishing_positions=Path(test_data_root / "input" / "20240301_qualifying_finishing_positions.csv"),
        racing_finishing_positions=Path(test_data_root / "input" / "20240301_race_finishing_positions.csv"),
    )
    assert len(max_score_teams) == 1
    team = max_score_teams.pop()
    assert team.points == 230


def test_main_qualifying_only():
    QUALIFYING_ONLY["setting"] = True

    test_data_root = ROOT_DIR.parent.parent / "tests" / "test_data"
    max_score_teams = main(
        driver_prices=Path(test_data_root / "driver_prices" / "20240301.csv"),
        constructor_prices=Path(test_data_root / "constructor_prices" / "20240301.csv"),
        qualifying_finishing_positions=Path(test_data_root / "input" / "20240301_qualifying_finishing_positions.csv"),
        racing_finishing_positions=Path(test_data_root / "input" / "20240301_race_finishing_positions.csv"),
    )
    assert len(max_score_teams) == 34
    team = max_score_teams.pop()
    assert team.points == 90
