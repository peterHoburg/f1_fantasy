from f1_fantasy.main import *


def test_driver_of_the_day():
    MAX.qualifying_position = 1
    MAX.race_position = 1
    MAX.fastest_lap = False
    MAX.driver_of_the_day = True

    SERGIO.qualifying_position = 20
    SERGIO.race_position = 20
    SERGIO.fastest_lap = False
    SERGIO.driver_of_the_day = False

    RED_BULL.compute_points()
    assert MAX.points == 45
    assert RED_BULL.points == 35


def test_fastest_lap():
    MAX.qualifying_position = 1
    MAX.race_position = 1
    MAX.fastest_lap = True
    MAX.driver_of_the_day = False

    SERGIO.qualifying_position = 20
    SERGIO.race_position = 20
    SERGIO.fastest_lap = False
    SERGIO.driver_of_the_day = False

    RED_BULL.compute_points()
    assert MAX.points == 45
    assert RED_BULL.points == 45


def test_fastest_pitstops():
    MAX.qualifying_position = 19
    MAX.race_position = 19
    MAX.fastest_lap = False
    MAX.driver_of_the_day = False

    SERGIO.qualifying_position = 20
    SERGIO.race_position = 20
    SERGIO.fastest_lap = False
    SERGIO.driver_of_the_day = False

    RED_BULL.fastest_pitstop = True
    RED_BULL.second_fastest_pitstop = True
    RED_BULL.third_fastest_pitstop = True

    RED_BULL.compute_points()
    assert MAX.points == 0
    assert SERGIO.points == 0
    assert RED_BULL.points == 18

