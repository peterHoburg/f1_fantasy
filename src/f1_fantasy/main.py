import csv
import datetime
import itertools
from copy import deepcopy
from pathlib import Path

from f1_fantasy.consts import MAX_CONSTRUCTORS_COST, MAX_DRIVERS_COST, MAX_TOTAL_COST
from f1_fantasy.game_objects import (
    CONSTRUCTORS_IGNORE_LIST,
    DRIVERS_IGNORE_LIST,
    Constructor,
    Constructors,
    Driver,
    Drivers,
    Team,
)


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


def set_drivers_qualifying_positions(qualifying_finishing_positions_csv: Path):
    with qualifying_finishing_positions_csv.open() as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            drivers_name = row["drivers_name"]
            driver = Drivers.get(drivers_name)
            driver.qualifying_position = int(i + 1)



def set_drivers_race_positions(race_finishing_positions_csv: Path):
    with race_finishing_positions_csv.open() as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            drivers_name = row["drivers_name"]
            driver = Drivers.get(drivers_name)
            driver.race_position = int(i + 1)



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
        team = Team(drivers=deepcopy(list(combo[0])), constructors=deepcopy(list(combo[1])))
        team.compute_points()
        if team.points >= highest_score:
            highest_score = team.points
            all_teams_set.add(team)

    highest_score_set = set()
    for team in all_teams_set:
        if team.points >= highest_score:
            highest_score_set.add(team)
            print(team)
    return highest_score_set


def main():
    Drivers.load_prices(Path("./data/driver_prices/20240301.csv"))
    Constructors.load_prices(Path("./data/constructor_prices/20240301.csv"))

    set_drivers_qualifying_positions(Path("./data/input/qualifying_finishing_positions.csv"))
    check_drivers_qualifying_positions()
    set_drivers_race_positions(Path("./data/input/race_finishing_positions.csv"))
    check_drivers_race_positions()

    for constructor in Constructors.all():
        constructor.compute_points()
    drivers_set = compute_driver_combinations()
    constructors_set = compute_constructor_combinations()
    max_score_teams = compute_driver_constructor_combinations(drivers_set, constructors_set)
    output_file = Path(f"./data/output/{datetime.datetime.utcnow()}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w+") as f:
        for team in max_score_teams:
            f.write(f"{team}\n")
        f.write(str(len(max_score_teams)))


if __name__ == "__main__":
    main()
