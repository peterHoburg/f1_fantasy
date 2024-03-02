qualifying_place_points = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

race_place_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]


class Driver:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self._points = 0
        self.fastest_lap = False
        self.driver_of_the_day = False

        self.qualifying_position: int | None = None
        self.race_position: int | None = None

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value: int):
        self._points = value

    @property
    def qualifying_position(self):
        return self._qualifying_position

    @qualifying_position.setter
    def qualifying_position(self, value: int):
        assert value is None or 1 <= value <= 20, "Qualifying position must be between 1 and 20"
        self._qualifying_position = value

    @property
    def race_position(self):
        return self._race_position

    @race_position.setter
    def race_position(self, value: int):
        assert value is None or 1 <= value <= 20, "Race position must be between 1 and 20"
        self._race_position = self._qualifying_position

    def compute_points(self):
        self._points = 0
        self._compute_qualifying_points()
        self._compute_race_points()
        self._compute_race_position_points()

    def _compute_qualifying_points(self):
        if self.qualifying_position is not None and self.qualifying_position <= 10:
            self._points += qualifying_place_points[self.qualifying_position - 1]
        elif self.qualifying_position is None:
            self._points -= 20

    def _compute_race_points(self):
        if self.race_position is not None and self.race_position <= 10:
            self._points += race_place_points[self.race_position - 1]
            if self.fastest_lap:
                self._points += 10
        if self.driver_of_the_day:
            self._points += 10

    def _compute_race_position_points(self):
        position_delta = self.qualifying_position - self.race_position
        if position_delta > 0:
            self._points += position_delta * 2
        elif position_delta < 0:
            self._points += position_delta

    def __repr__(self):
        return f"{self.name} - {self._points} points"


class Constructor:
    def __init__(self, name, price, drivers):
        self.name = name
        self.price = price
        self.drivers: list[Driver] = drivers
        self._points = 0
        self.fastest_pitstop = False
        self.second_fastest_pitstop = False
        self.third_fastest_pitstop = False

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value: int):
        self._points = value

    def compute_points(self):
        self._points = 0
        for driver in self.drivers:
            driver.compute_points()
            self._points += driver.points
            if driver.driver_of_the_day is True:
                self._points -= 10  # constructors do not get driver of the day bonuses

        if self.fastest_pitstop:
            self._points += 10
        if self.second_fastest_pitstop:
            self._points += 5
        if self.third_fastest_pitstop:
            self._points += 3


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
            print(f"Position {driver.race_position} is already used by another driver")
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
    ESTEBAN.qualifying_position = 18
    PIERRE.qualifying_position = 19


def set_drivers_race_positions():
    MAX.race_position = MAX.qualifying_position
    CHARLES.race_position = CHARLES.qualifying_position
    GEORGE.race_position = GEORGE.qualifying_position - 2
    CARLOS.race_position = CARLOS.qualifying_position + 1
    SERGIO.race_position = SERGIO.qualifying_position + 1
    FERNANDO.race_position = FERNANDO.qualifying_position
    LANDO.race_position = LANDO.qualifying_position
    OSCAR.race_position = OSCAR.qualifying_position - 1
    LEWIS.race_position = LEWIS.qualifying_position + 1
    NICO.race_position = NICO.qualifying_position

    YUKI.race_position = YUKI.qualifying_position
    LANCE.race_position = LANCE.qualifying_position
    ALEXANDER.race_position = ALEXANDER.qualifying_position
    DANIEL.race_position = DANIEL.qualifying_position
    KEVIN.race_position = KEVIN.qualifying_position
    VALTTERI.race_position = VALTTERI.qualifying_position
    ZHOU.race_position = ZHOU.qualifying_position
    ESTEBAN.race_position = ESTEBAN.qualifying_position
    PIERRE.race_position = PIERRE.qualifying_position


def main():
    set_drivers_qualifying_positions()
    check_drivers_qualifying_positions()
    set_drivers_race_positions()
    check_drivers_race_positions()



if __name__ == "__main__":
    main()
