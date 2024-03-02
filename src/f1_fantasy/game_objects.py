from f1_fantasy.consts import RACE_PLACE_POINTS, QUALIFYING_PLACE_POINTS


class Driver:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self._points = 0
        self.fastest_lap = False
        self.driver_of_the_day = False

        self.qualifying_position: int | None = None
        self.race_position: int | None = None

        self.drs = False
        self.extra_drs = False

    @property
    def points(self):
        if self.drs:
            return self._points * 2
        elif self.extra_drs:
            return self._points * 3
        return self._points

    @points.setter
    def points(self, value: int):
        self._points = value

    @property
    def constructors_points(self):
        return self._points

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
        self._race_position = value

    def compute_points(self):
        self._points = 0
        self._compute_qualifying_points()
        self._compute_race_points()
        self._compute_race_position_points()

    def _compute_qualifying_points(self):
        if self.qualifying_position is not None and self.qualifying_position <= 10:
            self._points += QUALIFYING_PLACE_POINTS[self.qualifying_position - 1]
        elif self.qualifying_position is None:
            self._points -= 20

    def _compute_race_points(self):
        if self.race_position is not None and self.race_position <= 10:
            self._points += RACE_PLACE_POINTS[self.race_position - 1]
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

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.name} - {self.points} points"


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
            self._points += driver.constructors_points
            if driver.driver_of_the_day is True:
                self._points -= 10  # constructors do not get driver of the day bonuses

        if self.fastest_pitstop:
            self._points += 10
        if self.second_fastest_pitstop:
            self._points += 5
        if self.third_fastest_pitstop:
            self._points += 3
        self.compute_constructors_qualifying_extra_points()

    def compute_constructors_qualifying_extra_points(self):
        qualifying_positions = [driver.qualifying_position for driver in self.drivers]

        # None into q2 or q3
        if all(qualifying_position > 15 for qualifying_position in qualifying_positions):
            self._points -= 1
            return

        # Both into q1
        if all(qualifying_position < 10 for qualifying_position in qualifying_positions):
            self._points += 10
            return

        # One in q1
        if any(qualifying_position < 10 for qualifying_position in qualifying_positions):
            self._points += 5
            return

        # One into q2
        if any(qualifying_position > 15 for qualifying_position in qualifying_positions):
            self._points += 2
            return

        # Both into q2
        if any(qualifying_position < 15 for qualifying_position in qualifying_positions):
            self._points += 3
            return

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.name} - {self.points} points"


class Team:
    def __init__(self, drivers, constructors):
        self.drivers = drivers
        self.constructors = constructors
        self.points = 0
        self.price = sum(driver.price for driver in self.drivers) + sum(
            constructor.price for constructor in self.constructors
        )

    def compute_points(self):
        self.points = 0
        # get driver with most points and second most points
        for driver in self.drivers:
            driver.extra_drs = False
            driver.drs = False
            driver.compute_points()
        drivers_list = sorted(self.drivers, key=lambda x: x.points, reverse=True)
        drivers_list[0].extra_drs = True
        drivers_list[1].drs = True
        self.points += sum(driver.points for driver in self.drivers)
        for constructor in self.constructors:
            constructor.compute_points()
            self.points += constructor.points

    def __repr__(self):
        drivers_ordered = sorted(self.drivers, key=lambda x: x.points, reverse=True)
        constructors_ordered = sorted(self.constructors, key=lambda x: x.points, reverse=True)
        return f"Total: {self.points}  Drivers: {drivers_ordered}  Constructors: {constructors_ordered}"


class Drivers:
    MAX = Driver(name="Max Verstappen", price=30.0)
    CHARLES = Driver(name="Charles Leclerc", price=19.1)
    GEORGE = Driver(name="George Russell", price=18.8)
    CARLOS = Driver(name="Carlos Sainz", price=18.5)
    SERGIO = Driver(name="Sergio Perez", price=20.8)
    FERNANDO = Driver(name="Fernando Alonso", price=15.8)
    LANDO = Driver(name="Lando Norris", price=23.0)
    OSCAR = Driver(name="Oscar Piastri", price=19.0)
    LEWIS = Driver(name="Lewis Hamilton", price=19.3)
    NICO = Driver(name="Nico Hulkenberg", price=6.4)
    YUKI = Driver(name="Yuki Tsunoda", price=8.0)
    LANCE = Driver(name="Lance Stroll", price=10.7)
    ALEXANDER = Driver(name="Alexander Albon", price=7.0)
    DANIEL = Driver(name="Daniel Ricciardo", price=9.0)
    KEVIN = Driver(name="Kevin Magnussen", price=6.2)
    VALTTERI = Driver(name="Valtteri Bottas", price=6.4)
    ZHOU = Driver(name="Zhou Guanyu", price=6.6)
    LOGAN = Driver(name="Logan Sargeant", price=5.5)
    ESTEBAN = Driver(name="Esteban Ocon", price=7.8)
    PIERRE = Driver(name="Pierre Gasly", price=7.8)

    @classmethod
    def all(cls):
        return [
            cls.MAX,
            cls.CHARLES,
            cls.GEORGE,
            cls.CARLOS,
            cls.SERGIO,
            cls.FERNANDO,
            cls.LANDO,
            cls.OSCAR,
            cls.LEWIS,
            cls.NICO,
            cls.YUKI,
            cls.LANCE,
            cls.ALEXANDER,
            cls.DANIEL,
            cls.KEVIN,
            cls.VALTTERI,
            cls.ZHOU,
            cls.LOGAN,
            cls.ESTEBAN,
            cls.PIERRE,
        ]


class Constructors:
    RED_BULL = Constructor(
        name="Red Bull Racing",
        price=27.9,
        drivers=[Drivers.MAX, Drivers.SERGIO],
    )
    MCLAREN = Constructor(
        name="McLaren",
        price=23.2,
        drivers=[Drivers.LANDO, Drivers.OSCAR],
    )
    MERCEDES = Constructor(
        name="Mercedes",
        price=20.1,
        drivers=[Drivers.LEWIS, Drivers.GEORGE],
    )
    FERRARI = Constructor(
        name="Ferrari",
        price=19.3,
        drivers=[Drivers.CHARLES, Drivers.CARLOS],
    )
    ASTON_MARTIN = Constructor(
        name="Aston Martin",
        price=13.6,
        drivers=[Drivers.FERNANDO, Drivers.LANCE],
    )
    RB = Constructor(
        name="RB",
        price=8.5,
        drivers=[Drivers.DANIEL, Drivers.YUKI],
    )
    ALPINE = Constructor(
        name="Alpine",
        price=8.4,
        drivers=[Drivers.PIERRE, Drivers.ESTEBAN],
    )
    WILLIAMS = Constructor(
        name="Williams",
        price=6.3,
        drivers=[Drivers.ALEXANDER, Drivers.LOGAN],
    )
    SAUBER = Constructor(
        name="Sauber",
        price=6.6,
        drivers=[Drivers.ZHOU, Drivers.VALTTERI],
    )
    HAAS = Constructor(
        name="Haas",
        price=6.3,
        drivers=[Drivers.NICO, Drivers.KEVIN],
    )

    @classmethod
    def all(cls):
        return [
            cls.RED_BULL,
            cls.MCLAREN,
            cls.MERCEDES,
            cls.FERRARI,
            cls.ASTON_MARTIN,
            cls.RB,
            cls.ALPINE,
            cls.WILLIAMS,
            cls.SAUBER,
            cls.HAAS,
        ]

DRIVERS_IGNORE_LIST = [
    Drivers.MAX,
]

CONSTRUCTORS_IGNORE_LIST = [
    Constructors.RED_BULL,
]
