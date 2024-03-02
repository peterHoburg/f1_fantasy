import itertools
from copy import deepcopy

from f1_fantasy.consts import MAX_DRIVERS_COST, MAX_CONSTRUCTORS_COST, MAX_TOTAL_COST
from f1_fantasy.game_objects import Driver, Constructor, Team






MAX = Driver(name="Max Verstappen", price=30.0)
SERGIO = Driver(name="Sergio Perez", price=20.8)
RED_BULL = Constructor(
    name="Red Bull Racing",
    price=27.9,
    drivers=[MAX, SERGIO],
)

LANDO = Driver(name="Lando Norris", price=23.0)
OSCAR = Driver(name="Oscar Piastri", price=19.0)
MCLAREN = Constructor(
    name="McLaren",
    price=23.2,
    drivers=[LANDO, OSCAR],
)

LEWIS = Driver(name="Lewis Hamilton", price=19.3)
GEORGE = Driver(name="George Russell", price=18.8)
MERCEDES = Constructor(
    name="Mercedes",
    price=20.1,
    drivers=[LEWIS, GEORGE],
)

CHARLES = Driver(name="Charles Leclerc", price=19.1)
CARLOS = Driver(name="Carlos Sainz", price=18.5)
FERRARI = Constructor(
    name="Ferrari",
    price=19.3,
    drivers=[CHARLES, CARLOS],
)

FERNANDO = Driver(name="Fernando Alonso", price=15.8)
LANCE = Driver(name="Lance Stroll", price=10.7)
ASTON_MARTIN = Constructor(
    name="Aston Martin",
    price=13.6,
    drivers=[FERNANDO, LANCE],
)

DANIEL = Driver(name="Daniel Ricciardo", price=9.0)
YUKI = Driver(name="Yuki Tsunoda", price=8.0)
RB = Constructor(
    name="RB",
    price=8.5,
    drivers=[DANIEL, YUKI],
)

PIERRE = Driver(name="Pierre Gasly", price=7.8)
ESTEBAN = Driver(name="Esteban Ocon", price=7.8)
ALPINE = Constructor(
    name="Alpine",
    price=8.4,
    drivers=[PIERRE, ESTEBAN],
)

ALEXANDER = Driver(name="Alexander Albon", price=7.0)
LOGAN = Driver(name="Logan Sargeant", price=5.5)
WILLIAMS = Constructor(
    name="Williams",
    price=6.3,
    drivers=[ALEXANDER, LOGAN],
)

ZHOU = Driver(name="Zhou Guanyu", price=6.6)
VALTTERI = Driver(name="Valtteri Bottas", price=6.4)
SAUBER = Constructor(
    name="Sauber",
    price=6.6,
    drivers=[ZHOU, VALTTERI],
)

NICO = Driver(name="Nico Hulkenberg", price=6.4)
KEVIN = Driver(name="Kevin Magnussen", price=6.2)
HAAS = Constructor(
    name="Haas",
    price=6.3,
    drivers=[NICO, KEVIN],
)

ALL_DRIVERS = [
    MAX,
    SERGIO,
    LANDO,
    OSCAR,
    LEWIS,
    GEORGE,
    CHARLES,
    CARLOS,
    FERNANDO,
    LANCE,
    DANIEL,
    YUKI,
    PIERRE,
    ESTEBAN,
    ALEXANDER,
    LOGAN,
    ZHOU,
    VALTTERI,
    NICO,
    KEVIN,
]

ALL_CONSTRUCTORS = [
    RED_BULL,
    MCLAREN,
    MERCEDES,
    FERRARI,
    ASTON_MARTIN,
    RB,
    ALPINE,
    WILLIAMS,
    SAUBER,
    HAAS,
]

BLACK_LIST_DRIVERS = [
    MAX,
]

BLACK_LIST_CONSTRUCTORS = [
    RED_BULL,
]


def check_drivers_qualifying_positions():
    used_positions = set()
    for driver in ALL_DRIVERS:
        if driver.qualifying_position is None:
            continue
        if driver.qualifying_position in used_positions:
            print(f"Position {driver.qualifying_position} is already used by another driver")
            raise ValueError
        else:
            used_positions.add(driver.qualifying_position)


def check_drivers_race_positions():
    used_positions = set()
    for driver in ALL_DRIVERS:
        if driver.race_position is None:
            continue
        if driver.race_position in used_positions:
            print(f"Position {driver.race_position} is already used by another driver. {driver.name}")
            raise ValueError
        else:
            used_positions.add(driver.race_position)


def set_drivers_qualifying_positions():
    MAX.qualifying_position = 1
    CHARLES.qualifying_position = 2
    GEORGE.qualifying_position = 3
    CARLOS.qualifying_position = 4
    SERGIO.qualifying_position = 5
    FERNANDO.qualifying_position = 6
    LANDO.qualifying_position = 7
    OSCAR.qualifying_position = 8
    LEWIS.qualifying_position = 9
    NICO.qualifying_position = 10

    YUKI.qualifying_position = 11
    LANCE.qualifying_position = 12
    ALEXANDER.qualifying_position = 13
    DANIEL.qualifying_position = 14
    KEVIN.qualifying_position = 15
    VALTTERI.qualifying_position = 16
    ZHOU.qualifying_position = 17
    LOGAN.qualifying_position = 18
    ESTEBAN.qualifying_position = 19
    PIERRE.qualifying_position = 20


def set_drivers_race_positions():
    """
    - is better
    + is worse
    """
    MAX.race_position = MAX.qualifying_position
    CHARLES.race_position = CHARLES.qualifying_position

    GEORGE.race_position = GEORGE.qualifying_position + 2
    CARLOS.race_position = CARLOS.qualifying_position - 1
    SERGIO.race_position = SERGIO.qualifying_position - 1

    FERNANDO.race_position = FERNANDO.qualifying_position + 1
    LANDO.race_position = LANDO.qualifying_position - 1

    OSCAR.race_position = OSCAR.qualifying_position + 1
    LEWIS.race_position = LEWIS.qualifying_position - 1

    NICO.race_position = NICO.qualifying_position

    YUKI.race_position = YUKI.qualifying_position + 1
    LANCE.race_position = LANCE.qualifying_position - 1

    ALEXANDER.race_position = ALEXANDER.qualifying_position + 1
    DANIEL.race_position = DANIEL.qualifying_position - 1

    KEVIN.race_position = KEVIN.qualifying_position + 1
    VALTTERI.race_position = VALTTERI.qualifying_position - 1

    ZHOU.race_position = ZHOU.qualifying_position
    LOGAN.race_position = LOGAN.qualifying_position
    ESTEBAN.race_position = ESTEBAN.qualifying_position
    PIERRE.race_position = PIERRE.qualifying_position


def compute_driver_combinations():
    all_drivers = set(ALL_DRIVERS).difference(set(BLACK_LIST_DRIVERS))
    all_driver_combos = itertools.combinations(all_drivers, 5)
    all_driver_set = set()
    for combo in all_driver_combos:
        driver_cost = sum(driver.price for driver in combo)
        if driver_cost <= MAX_DRIVERS_COST:
            all_driver_set.add(combo)
    return all_driver_set


def compute_constructor_combinations():
    all_constructors = set(ALL_CONSTRUCTORS).difference(set(BLACK_LIST_CONSTRUCTORS))
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
    set_drivers_qualifying_positions()
    check_drivers_qualifying_positions()
    set_drivers_race_positions()
    check_drivers_race_positions()

    for constructor in ALL_CONSTRUCTORS:
        constructor.compute_points()
    drivers_set = compute_driver_combinations()
    constructors_set = compute_constructor_combinations()
    max_score_teams = compute_driver_constructor_combinations(drivers_set, constructors_set)
    print(len(max_score_teams))
    # print(ALL_DRIVERS)
    # print(ALL_CONSTRUCTORS)


if __name__ == "__main__":
    main()
