import csv
import datetime
import itertools
import time
from copy import deepcopy
from pathlib import Path
from typing import TextIO

from f1_fantasy.consts import MAX_CONSTRUCTORS_COST, MAX_DRIVERS_COST, MAX_TOTAL_COST, ROOT_DIR
from f1_fantasy.game_objects import (
    CONSTRUCTORS_IGNORE_LIST,
    DRIVERS_IGNORE_LIST,
    Constructor,
    Constructors,
    Driver,
    Drivers,
    Team,
)
from f1_fantasy.models import ConstructorPriceModel, DriverPriceModel, FinishingPositionModel, SpecialPoints, \
    DriversEnum, ConstructorsEnum
from f1_fantasy.settings import SETTINGS


def check_drivers_qualifying_positions():
    used_positions = set()
    for driver in Drivers.all():
        if driver.qualifying_position is None:
            continue
        if driver.qualifying_position in used_positions:
            print(f"Position {driver.qualifying_position} is already used by another driver")
            raise ValueError
        else:
            used_positions.add(driver.qualifying_position)


def check_drivers_race_positions():
    used_positions = set()
    for driver in Drivers.all():
        if driver.race_position is None:
            continue
        if driver.race_position in used_positions:
            print(f"Position {driver.race_position} is already used by another driver. {driver.name}")
            raise ValueError
        else:
            used_positions.add(driver.race_position)


def set_drivers_positions(
    qualifying_finishing_positions: FinishingPositionModel, racing_finishing_positions: FinishingPositionModel
):
    for i, driver_name in enumerate(qualifying_finishing_positions.drivers):
        drivers_name = driver_name
        driver = Drivers.get(drivers_name)
        driver.qualifying_position = int(i + 1)

    for i, driver_name in enumerate(racing_finishing_positions.drivers):
        drivers_name = driver_name
        driver = Drivers.get(drivers_name)
        driver.race_position = int(i + 1)

    check_drivers_qualifying_positions()
    check_drivers_race_positions()


def compute_driver_combinations():
    all_drivers = set(Drivers.all()).difference(set(DRIVERS_IGNORE_LIST))
    all_driver_combos = itertools.combinations(all_drivers, 5)
    all_driver_set = set()
    for combo in all_driver_combos:
        driver_cost = sum(driver.price for driver in combo)
        if driver_cost <= MAX_DRIVERS_COST:
            all_driver_set.add(combo)
    return all_driver_set


def compute_constructor_combinations():
    all_constructors = set(Constructors.all()).difference(set(CONSTRUCTORS_IGNORE_LIST))
    all_constructor_combos = itertools.combinations(all_constructors, 2)
    all_constructor_set = set()
    for combo in all_constructor_combos:
        constructor_cost = sum(constructor.price for constructor in combo)
        if constructor_cost <= MAX_CONSTRUCTORS_COST:
            all_constructor_set.add(combo)
    return all_constructor_set


def compute_driver_constructor_combinations(drivers_set: set[Driver], constructors_set: set[Constructor]):
    all_combinations = itertools.product(drivers_set, constructors_set)
    all_teams_set = set()
    highest_score = 0
    for combo in all_combinations:
        driver_cost = sum(driver.price for driver in combo[0])
        constructor_cost = sum(constructor.price for constructor in combo[1])
        cost = driver_cost + constructor_cost
        if cost > MAX_TOTAL_COST:
            continue
        team = Team(drivers=list(combo[0]), constructors=list(combo[1]))
        team.compute_points()
        if team.points >= highest_score:
            highest_score = team.points
            all_teams_set.add(team)

    highest_score_set = set()
    for team in all_teams_set:
        if team.points >= highest_score:
            team_copy = Team(drivers=deepcopy(team.drivers), constructors=deepcopy(team.constructors))
            team_copy.compute_points()
            highest_score_set.add(team_copy)
    return highest_score_set


def set_special_points(special_points: SpecialPoints):
    if special_points.fastest_lap is not None:
        driver = Drivers.get(special_points.fastest_lap)
        driver.fastest_lap = True
    if special_points.driver_of_the_day is not None:
        driver = Drivers.get(special_points.driver_of_the_day)
        driver.driver_of_the_day = True

    if special_points.fastest_pitstop is not None:
        constructor = Constructors.get(special_points.fastest_pitstop)
        constructor.fastest_pitstop = True
    if special_points.second_fastest_pitstop is not None:
        constructor = Constructors.get(special_points.second_fastest_pitstop)
        constructor.second_fastest_pitstop = True
    if special_points.third_fastest_pitstop is not None:
        constructor = Constructors.get(special_points.third_fastest_pitstop)
        constructor.third_fastest_pitstop = True


def calculations(
    driver_prices: list[DriverPriceModel],
    constructor_prices: list[ConstructorPriceModel],
    qualifying_finishing_positions: FinishingPositionModel,
    racing_finishing_positions: FinishingPositionModel,
    special_points: SpecialPoints,
) -> set[Team]:
    Drivers.load_prices(driver_prices)
    Constructors.load_prices(constructor_prices)

    set_drivers_positions(qualifying_finishing_positions, racing_finishing_positions)
    set_special_points(special_points)

    for constructor in Constructors.all():
        constructor.compute_points()
    drivers_set = compute_driver_combinations()
    constructors_set = compute_constructor_combinations()
    max_score_teams = compute_driver_constructor_combinations(drivers_set, constructors_set)
    return max_score_teams


def drivers_prices_from_csv(driver_prices_csv: Path) -> list[DriverPriceModel]:
    with driver_prices_csv.open() as f:
        reader = csv.DictReader(f)
        return [DriverPriceModel.model_validate(row) for row in reader]


def constructors_prices_from_csv(constructor_prices_csv: Path) -> list[ConstructorPriceModel]:
    with constructor_prices_csv.open() as f:
        reader = csv.DictReader(f)
        return [ConstructorPriceModel.model_validate(row) for row in reader]


def finishing_positions_from_csv(qualifying_finishing_positions_csv: Path) -> FinishingPositionModel:
    with qualifying_finishing_positions_csv.open() as f:
        reader = csv.DictReader(f)
        driver_list = []
        for driver in reader:
            driver_list.append(driver["name"])
        return FinishingPositionModel(drivers=driver_list)


def special_points_from_csv(special_points_csv: Path) -> SpecialPoints:
    with special_points_csv.open() as f:
        reader = csv.DictReader(f)
        special_points_dict = {}
        for row in reader:
            special_points_dict[row["category"]] = row["recipient"]
    return SpecialPoints.model_validate(special_points_dict)


def set_chips_from_csv(chips_csv: Path):
    with chips_csv.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["chip_to_enable"] == "extra_drs":
                SETTINGS.chips.extra_drs = True


def set_ignores_from_csvs(ignore_constructors: Path, ignore_drivers: Path):
    with ignore_constructors.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            constructor = ConstructorsEnum[row["name"].strip().upper()]
            constructor = Constructors.get(constructor)
            CONSTRUCTORS_IGNORE_LIST.append(constructor)

    with ignore_drivers.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            driver_enum = DriversEnum[row["name"].strip().upper()]
            driver = Drivers.get(driver_enum)
            DRIVERS_IGNORE_LIST.append(driver)


def write_csv_to_output(f: TextIO, csv_path: Path):
    with csv_path.open() as cp_csv:
        reader = csv.DictReader(cp_csv)
        f.write(f"\n{csv_path.name}:\n")
        for row in reader:
            f.write(str(row) + "\n")

def main(
    chips_path: Path,
    finishing_positions_qualifying_path: Path,
    finishing_positions_race_path: Path,
    ignore_constructors_path: Path,
    ignore_drivers_path: Path,
    price_constructors_path: Path,
    price_drivers_path: Path,
    special_points_path: Path,
    output_file_path: Path,
):
    driver_prices = drivers_prices_from_csv(price_drivers_path)
    constructor_prices = constructors_prices_from_csv(price_constructors_path)
    finishing_positions_qualifying = finishing_positions_from_csv(finishing_positions_qualifying_path)
    finishing_positions_race = finishing_positions_from_csv(finishing_positions_race_path)
    special_points = special_points_from_csv(special_points_path)
    set_chips_from_csv(chips_path)
    set_ignores_from_csvs(ignore_constructors=ignore_constructors_path, ignore_drivers=ignore_drivers_path)

    _max_score_teams = calculations(
        driver_prices=driver_prices,
        constructor_prices=constructor_prices,
        qualifying_finishing_positions=finishing_positions_qualifying,
        racing_finishing_positions=finishing_positions_race,
        special_points=special_points,
    )
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    with output_file_path.open("w+") as f:
        print(f"Total teams: {len(_max_score_teams)}")
        f.write(f"Total teams: {len(_max_score_teams)}\n")
        for team in _max_score_teams:
            print(team)
            f.write(f"{team}\n")

        f.write("\n" + "#" * 120)
        f.write("\n" + "#" * 120)
        f.write("\nOutput generated using the following input:\n")

        write_csv_to_output(f, chips_path)
        write_csv_to_output(f, finishing_positions_qualifying_path)
        write_csv_to_output(f, finishing_positions_race_path)
        write_csv_to_output(f, ignore_constructors_path)
        write_csv_to_output(f, ignore_drivers_path)
        write_csv_to_output(f, price_constructors_path)
        write_csv_to_output(f, price_drivers_path)
        write_csv_to_output(f, special_points_path)

    print(f"Output written to {output_file_path}")



if __name__ == "__main__":
    main(chips_path=Path(ROOT_DIR / "data" / "input" / "chips.csv"),
         finishing_positions_qualifying_path=Path(ROOT_DIR / "data" / "input" / "finishing_positions_qualifying.csv"),
         finishing_positions_race_path=Path(ROOT_DIR / "data" / "input" / "finishing_positions_race.csv"),
         ignore_constructors_path=Path(ROOT_DIR / "data" / "input" / "ignore_constructors.csv"),
         ignore_drivers_path=Path(ROOT_DIR / "data" / "input" / "ignore_drivers.csv"),
         price_constructors_path=Path(ROOT_DIR / "data" / "input" / "price_constructors.csv"),
         price_drivers_path=Path(ROOT_DIR / "data" / "input" / "price_drivers.csv"),
         special_points_path=Path(ROOT_DIR / "data" / "input" / "special_points.csv"),
         output_file_path=Path(ROOT_DIR / "data" / "output" / f"{time.time()}"))
