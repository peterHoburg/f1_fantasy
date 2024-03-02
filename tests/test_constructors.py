from f1_fantasy.game_objects import Constructors, Drivers


def test_driver_of_the_day():
    Drivers.MAX.qualifying_position = 1
    Drivers.MAX.race_position = 1
    Drivers.MAX.fastest_lap = False
    Drivers.MAX.driver_of_the_day = True

    Drivers.SERGIO.qualifying_position = 20
    Drivers.SERGIO.race_position = 20
    Drivers.SERGIO.fastest_lap = False
    Drivers.SERGIO.driver_of_the_day = False

    Constructors.RED_BULL.compute_points()
    assert Drivers.MAX.points == 45  # 35 for points + 10 for driver of the day
    assert Constructors.RED_BULL.points == 40  # 35 for max + 5 for 1 in q 3


def test_fastest_lap():
    Drivers.MAX.qualifying_position = 1
    Drivers.MAX.race_position = 1
    Drivers.MAX.fastest_lap = True
    Drivers.MAX.driver_of_the_day = False

    Drivers.SERGIO.qualifying_position = 20
    Drivers.SERGIO.race_position = 20
    Drivers.SERGIO.fastest_lap = False
    Drivers.SERGIO.driver_of_the_day = False

    Constructors.RED_BULL.compute_points()
    assert Drivers.MAX.points == 45
    assert Constructors.RED_BULL.points == 50


def test_fastest_pit_stops():
    Drivers.MAX.qualifying_position = 19
    Drivers.MAX.race_position = 19
    Drivers.MAX.fastest_lap = False
    Drivers.MAX.driver_of_the_day = False

    Drivers.SERGIO.qualifying_position = 20
    Drivers.SERGIO.race_position = 20
    Drivers.SERGIO.fastest_lap = False
    Drivers.SERGIO.driver_of_the_day = False

    Constructors.RED_BULL.fastest_pitstop = True
    Constructors.RED_BULL.second_fastest_pitstop = True
    Constructors.RED_BULL.third_fastest_pitstop = True

    Constructors.RED_BULL.compute_points()
    assert Drivers.MAX.points == 0
    assert Drivers.SERGIO.points == 0
    assert Constructors.RED_BULL.points == 17 # 18 for pit stops but -1 for no q2
