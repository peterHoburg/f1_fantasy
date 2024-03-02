from f1_fantasy.main import Driver


def test_driver_first():
    driver = Driver("example", 8.0)
    driver.qualifying_position = 1
    driver.race_position = 1
    driver.compute_points()
    assert driver.points == 35


def test_driver_last():
    driver = Driver("example", 8.0)
    driver.qualifying_position = 20
    driver.race_position = 20
    driver.compute_points()
    assert driver.points == 0


def test_driver_last_to_first():
    driver = Driver("example", 8.0)
    driver.qualifying_position = 20
    driver.race_position = 1
    driver.compute_points()
    assert driver.points == 63


def test_driver_first_to_last():
    driver = Driver("example", 8.0)
    driver.qualifying_position = 1
    driver.race_position = 20
    driver.compute_points()
    assert driver.points == -9


def test_driver_first_fastest_lap():
    driver = Driver("example", 8.0)
    driver.qualifying_position = 1
    driver.race_position = 1
    driver.fastest_lap = True
    driver.driver_of_the_day = True
    driver.compute_points()
    assert driver.points == 55


def test_driver_fastest_lap_out_of_points():
    driver = Driver("example", 8.0)
    driver.qualifying_position = 20
    driver.race_position = 20
    driver.fastest_lap = True
    driver.compute_points()
    assert driver.points == 0


def test_driver_fastest_lap_10th():
    driver = Driver("example", 8.0)
    driver.qualifying_position = 10
    driver.race_position = 10
    driver.fastest_lap = True
    driver.compute_points()
    assert driver.points == 12
