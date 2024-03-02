from pathlib import Path

from f1_fantasy.consts import ROOT_DIR
from f1_fantasy.main import (
    calculations,
    constructors_prices_from_csv,
    drivers_prices_from_csv,
    finishing_positions_from_csv,
)
from f1_fantasy.models import SpecialPoints
from f1_fantasy.settings import SETTINGS


def test_main():
    SETTINGS.chips.extra_drs = True
    SETTINGS.qualifying_only = False
    test_data_root = ROOT_DIR.parent.parent / "tests" / "test_data"

    driver_prices = drivers_prices_from_csv(Path(test_data_root / "driver_prices" / "20240301.csv"))
    constructor_prices = constructors_prices_from_csv(Path(test_data_root / "constructor_prices" / "20240301.csv"))
    qualifying_finishing_positions = finishing_positions_from_csv(
        Path(test_data_root / "input" / "20240301_qualifying_finishing_positions.csv")
    )
    racing_finishing_positions = finishing_positions_from_csv(
        Path(test_data_root / "input" / "20240301_race_finishing_positions.csv")
    )

    max_score_teams = calculations(
        driver_prices=driver_prices,
        constructor_prices=constructor_prices,
        qualifying_finishing_positions=qualifying_finishing_positions,
        racing_finishing_positions=racing_finishing_positions,
        special_points=SpecialPoints(),
    )
    assert len(max_score_teams) == 1
    team = max_score_teams.pop()
    assert team.points == 235


def test_main_qualifying_only():
    SETTINGS.chips.extra_drs = True
    SETTINGS.qualifying_only = True
    test_data_root = ROOT_DIR.parent.parent / "tests" / "test_data"

    driver_prices = drivers_prices_from_csv(Path(test_data_root / "driver_prices" / "20240301.csv"))
    constructor_prices = constructors_prices_from_csv(Path(test_data_root / "constructor_prices" / "20240301.csv"))
    qualifying_finishing_positions = finishing_positions_from_csv(
        Path(test_data_root / "input" / "20240301_qualifying_finishing_positions.csv")
    )
    racing_finishing_positions = finishing_positions_from_csv(
        Path(test_data_root / "input" / "20240301_race_finishing_positions.csv")
    )

    max_score_teams = calculations(
        driver_prices=driver_prices,
        constructor_prices=constructor_prices,
        qualifying_finishing_positions=qualifying_finishing_positions,
        racing_finishing_positions=racing_finishing_positions,
        special_points=SpecialPoints(),
    )
    assert len(max_score_teams) == 34
    team = max_score_teams.pop()
    assert team.points == 90
