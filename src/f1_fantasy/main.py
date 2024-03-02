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


def set_drivers_qualifying_positions():
    Drivers.MAX.qualifying_position = 1
    Drivers.CHARLES.qualifying_position = 2
    Drivers.GEORGE.qualifying_position = 3
    Drivers.CARLOS.qualifying_position = 4
    Drivers.SERGIO.qualifying_position = 5
    Drivers.FERNANDO.qualifying_position = 6
    Drivers.LANDO.qualifying_position = 7
    Drivers.OSCAR.qualifying_position = 8
    Drivers.LEWIS.qualifying_position = 9
    Drivers.NICO.qualifying_position = 10

    Drivers.YUKI.qualifying_position = 11
    Drivers.LANCE.qualifying_position = 12
    Drivers.ALEXANDER.qualifying_position = 13
    Drivers.DANIEL.qualifying_position = 14
    Drivers.KEVIN.qualifying_position = 15
    Drivers.VALTTERI.qualifying_position = 16
    Drivers.ZHOU.qualifying_position = 17
    Drivers.LOGAN.qualifying_position = 18
    Drivers.ESTEBAN.qualifying_position = 19
    Drivers.PIERRE.qualifying_position = 20


def set_drivers_race_positions():
    """
    - is better
    + is worse
    """
    Drivers.MAX.race_position = Drivers.MAX.qualifying_position
    Drivers.CHARLES.race_position = Drivers.CHARLES.qualifying_position

    Drivers.GEORGE.race_position = Drivers.GEORGE.qualifying_position + 2
    Drivers.CARLOS.race_position = Drivers.CARLOS.qualifying_position - 1
    Drivers.SERGIO.race_position = Drivers.SERGIO.qualifying_position - 1

    Drivers.FERNANDO.race_position = Drivers.FERNANDO.qualifying_position + 1
    Drivers.LANDO.race_position = Drivers.LANDO.qualifying_position - 1

    Drivers.OSCAR.race_position = Drivers.OSCAR.qualifying_position + 1
    Drivers.LEWIS.race_position = Drivers.LEWIS.qualifying_position - 1

    Drivers.NICO.race_position = Drivers.NICO.qualifying_position

    Drivers.YUKI.race_position = Drivers.YUKI.qualifying_position + 1
    Drivers.LANCE.race_position = Drivers.LANCE.qualifying_position - 1

    Drivers.ALEXANDER.race_position = Drivers.ALEXANDER.qualifying_position + 1
    Drivers.DANIEL.race_position = Drivers.DANIEL.qualifying_position - 1

    Drivers.KEVIN.race_position = Drivers.KEVIN.qualifying_position + 1
    Drivers.VALTTERI.race_position = Drivers.VALTTERI.qualifying_position - 1

    Drivers.ZHOU.race_position = Drivers.ZHOU.qualifying_position
    Drivers.LOGAN.race_position = Drivers.LOGAN.qualifying_position
    Drivers.ESTEBAN.race_position = Drivers.ESTEBAN.qualifying_position
    Drivers.PIERRE.race_position = Drivers.PIERRE.qualifying_position


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

    set_drivers_qualifying_positions()
    check_drivers_qualifying_positions()
    set_drivers_race_positions()
    check_drivers_race_positions()

    for constructor in Constructors.all():
        constructor.compute_points()
    drivers_set = compute_driver_combinations()
    constructors_set = compute_constructor_combinations()
    max_score_teams = compute_driver_constructor_combinations(drivers_set, constructors_set)
    print(len(max_score_teams))
    # print(ALL_DRIVERS)
    # print(ALL_CONSTRUCTORS)


if __name__ == "__main__":
    main()
