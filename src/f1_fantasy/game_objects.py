from dataclasses import dataclass

from f1_fantasy.consts import QUALIFYING_PLACE_POINTS, RACE_PLACE_POINTS
from f1_fantasy.models import ConstructorPriceModel, ConstructorsEnum, DriverPriceModel, DriversEnum
from f1_fantasy.settings import SETTINGS


@dataclass
class DriverPointsBreakdown:
    qualifying_position: int = 0

    race_position: int = 0
    race_positions_changed: int = 0
    race_overtake_bonus: int = 0

    driver_of_the_day: int = 0
    fastest_lap: int = 0
    drs_multiplier: int = 1

    def __repr__(self):
        repr_str = (
            f"qualifying: {self.qualifying_position} "
            f"race_position: {self.race_position} "
            f"race_position_changed: {self.race_positions_changed} "
            f"race_overtake_bonus: {self.race_overtake_bonus} "
        )
        if self.driver_of_the_day != 0:
            repr_str += f" driver_of_the_day: {self.driver_of_the_day} "
        if self.fastest_lap != 0:
            repr_str += f" fastest_lap: {self.fastest_lap} "
        if self.drs_multiplier != 1:
            repr_str += f" drs_multiplier: {self.drs_multiplier} "

        repr_str += f" total_pre_drs: {self.qualifying_position + self.race_position + self.race_positions_changed + self.race_overtake_bonus + self.driver_of_the_day + self.fastest_lap}"
        return repr_str


@dataclass
class ConstructorPointsBreakdown:
    qualifying_position: int = 0
    driver_qualifying_bonus: int = 0

    race_position: int = 0
    race_positions_changed: int = 0
    race_overtake_bonus: int = 0

    fastest_pitstop: int = 0
    second_fastest_pitstop: int = 0
    third_fastest_pitstop: int = 0

    def __repr__(self):
        repr_str = (
            f"qualifying: {self.qualifying_position} "
            f"driver_qualifying_bonus: {self.driver_qualifying_bonus} "
            f"race_position: {self.race_position} "
            f"race_position_changed: {self.race_positions_changed} "
            f"race_overtake_bonus: {self.race_overtake_bonus} "
        )
        if self.fastest_pitstop != 0:
            repr_str += f" fastest_pitstop: {self.fastest_pitstop} "
        if self.second_fastest_pitstop != 0:
            repr_str += f" second_fastest_pitstop: {self.second_fastest_pitstop} "
        if self.third_fastest_pitstop != 0:
            repr_str += f" third_fastest_pitstop: {self.third_fastest_pitstop} "

        return repr_str


class Driver:
    def __init__(self, name: str, price: float = 0.0):
        self.name = name
        self.price = price
        self._points = 0
        self.fastest_lap = False
        self.driver_of_the_day = False

        self.qualifying_position: int | None = None
        self.race_position: int | None = None

        self.points_breakdown: DriverPointsBreakdown = DriverPointsBreakdown()

        self.drs = False
        self.extra_drs = False

    @property
    def points(self):
        if self.drs:
            self.points_breakdown.drs_multiplier = 2
            return self._points * 2
        elif self.extra_drs:
            self.points_breakdown.drs_multiplier = 3
            return self._points * 3
        self.points_breakdown.drs_multiplier = 1
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
        self.points_breakdown: DriverPointsBreakdown = DriverPointsBreakdown()
        self._points = 0
        self._compute_qualifying_points()
        if SETTINGS.qualifying_only is True:
            return
        self._compute_race_points()
        self._compute_race_position_points()

    def _compute_qualifying_points(self):
        points_change = 0
        if self.qualifying_position is not None and self.qualifying_position <= 10:
            points_change = QUALIFYING_PLACE_POINTS[self.qualifying_position - 1]
        elif self.qualifying_position is None:
            points_change = -20
        self.points_breakdown.qualifying_position = points_change
        self._points += points_change

    def _compute_race_points(self):
        if self.race_position is not None and self.race_position <= 10:
            self._points += RACE_PLACE_POINTS[self.race_position - 1]
            self.points_breakdown.race_position = RACE_PLACE_POINTS[self.race_position - 1]
            if self.fastest_lap:
                self._points += 10
                self.points_breakdown.fastest_lap = 10
        if self.driver_of_the_day:
            self._points += 10
            self.points_breakdown.driver_of_the_day = 10

    def _compute_race_position_points(self):
        position_delta = self.qualifying_position - self.race_position
        self.points_breakdown.race_positions_changed = position_delta

        if position_delta > 0:
            self._points += position_delta * 2
            self.points_breakdown.race_overtake_bonus = position_delta
        elif position_delta < 0:
            self._points += position_delta

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"\n{self.name} - {self.points} points: breakdown: {self.points_breakdown}"


class Constructor:
    def __init__(self, name: str, drivers: list[Driver], price: float = 0.0):
        self.name = name
        self.price = price
        self.drivers: list[Driver] = drivers
        self._points = 0
        self.fastest_pitstop = False
        self.second_fastest_pitstop = False
        self.third_fastest_pitstop = False

        self.points_breakdown: ConstructorPointsBreakdown = ConstructorPointsBreakdown()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value: int):
        self._points = value

    def compute_points(self):
        self.points_breakdown: ConstructorPointsBreakdown = ConstructorPointsBreakdown()
        self._points = 0
        for driver in self.drivers:
            driver.compute_points()
            driver_breakdown = driver.points_breakdown

            self.points_breakdown.qualifying_position += driver_breakdown.qualifying_position

            self.points_breakdown.race_position += driver.points_breakdown.race_position
            self.points_breakdown.race_positions_changed += driver.points_breakdown.race_positions_changed
            self.points_breakdown.race_overtake_bonus += driver.points_breakdown.race_overtake_bonus

            self._points += driver.constructors_points
            if driver.driver_of_the_day is True:
                self._points -= 10  # constructors do not get driver of the day bonuses

        if self.fastest_pitstop:
            self.points_breakdown.fastest_pitstop = 10
            self._points += 10
        if self.second_fastest_pitstop:
            self.points_breakdown.second_fastest_pitstop = 5
            self._points += 5
        if self.third_fastest_pitstop:
            self.points_breakdown.third_fastest_pitstop = 3
            self._points += 3
        self.compute_constructors_qualifying_extra_points()

    def compute_constructors_qualifying_extra_points(self):
        qualifying_positions = [driver.qualifying_position for driver in self.drivers]

        # None into q2 or q3
        if all(qualifying_position > 15 for qualifying_position in qualifying_positions):
            self.points_breakdown.driver_qualifying_bonus = -1
            self._points -= 1
            return

        # Both into q1
        if all(qualifying_position < 10 for qualifying_position in qualifying_positions):
            self.points_breakdown.driver_qualifying_bonus = 10
            self._points += 10
            return

        # One in q1
        if any(qualifying_position < 10 for qualifying_position in qualifying_positions):
            self.points_breakdown.driver_qualifying_bonus = 5
            self._points += 5
            return

        # One into q2
        if any(qualifying_position > 15 for qualifying_position in qualifying_positions):
            self.points_breakdown.driver_qualifying_bonus = 2
            self._points += 2
            return

        # Both into q2
        if any(qualifying_position < 15 for qualifying_position in qualifying_positions):
            self.points_breakdown.driver_qualifying_bonus = 3
            self._points += 3
            return

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"\n{self.name} - {self.points} points breakdown: {self.points_breakdown}"


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
        if SETTINGS.chips.extra_drs is True:
            drivers_list[0].extra_drs = True
            drivers_list[1].drs = True
        else:
            drivers_list[0].drs = True
        self.points += sum(driver.points for driver in self.drivers)
        for constructor in self.constructors:
            constructor.compute_points()
            self.points += constructor.points

    def __repr__(self):
        drivers_ordered = sorted(self.drivers, key=lambda x: x.points, reverse=True)
        constructors_ordered = sorted(self.constructors, key=lambda x: x.points, reverse=True)
        driver_str = "".join([f"{driver}" for driver in drivers_ordered])
        constructor_str = "".join([f"{constructor}" for constructor in constructors_ordered])
        return (
            "Team:\n"
            + f"Total points: {self.points}"
            + "\n\n"
            + "Drivers: "
            + driver_str
            + "\n\n"
            + "Constructors: "
            + constructor_str
        )


class Drivers:
    MAX = Driver(name="Max Verstappen")
    CHARLES = Driver(name="Charles Leclerc")
    GEORGE = Driver(name="George Russell")
    CARLOS = Driver(name="Carlos Sainz")
    SERGIO = Driver(name="Sergio Perez")
    FERNANDO = Driver(name="Fernando Alonso")
    LANDO = Driver(name="Lando Norris")
    OSCAR = Driver(name="Oscar Piastri")
    LEWIS = Driver(name="Lewis Hamilton")
    NICO = Driver(name="Nico Hulkenberg")
    YUKI = Driver(name="Yuki Tsunoda")
    LANCE = Driver(name="Lance Stroll")
    ALEXANDER = Driver(name="Alexander Albon")
    DANIEL = Driver(name="Daniel Ricciardo")
    KEVIN = Driver(name="Kevin Magnussen")
    VALTTERI = Driver(name="Valtteri Bottas")
    ZHOU = Driver(name="Zhou Guanyu")
    LOGAN = Driver(name="Logan Sargeant")
    ESTEBAN = Driver(name="Esteban Ocon")
    PIERRE = Driver(name="Pierre Gasly")

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

    @classmethod
    def get(cls, name: DriversEnum):
        return getattr(cls, str(name.value).upper())

    @classmethod
    def load_prices(cls, driver_prices: list[DriverPriceModel]):
        for driver_price in driver_prices:
            cls.get(driver_price.name).price = float(driver_price.price)


class Constructors:
    RED_BULL = Constructor(
        name="Red Bull Racing",
        drivers=[Drivers.MAX, Drivers.SERGIO],
    )
    MCLAREN = Constructor(
        name="McLaren",
        drivers=[Drivers.LANDO, Drivers.OSCAR],
    )
    MERCEDES = Constructor(
        name="Mercedes",
        drivers=[Drivers.LEWIS, Drivers.GEORGE],
    )
    FERRARI = Constructor(
        name="Ferrari",
        drivers=[Drivers.CHARLES, Drivers.CARLOS],
    )
    ASTON_MARTIN = Constructor(
        name="Aston Martin",
        drivers=[Drivers.FERNANDO, Drivers.LANCE],
    )
    RB = Constructor(
        name="RB",
        drivers=[Drivers.DANIEL, Drivers.YUKI],
    )
    ALPINE = Constructor(
        name="Alpine",
        drivers=[Drivers.PIERRE, Drivers.ESTEBAN],
    )
    WILLIAMS = Constructor(
        name="Williams",
        drivers=[Drivers.ALEXANDER, Drivers.LOGAN],
    )
    SAUBER = Constructor(
        name="Sauber",
        drivers=[Drivers.ZHOU, Drivers.VALTTERI],
    )
    HAAS = Constructor(
        name="Haas",
        drivers=[Drivers.NICO, Drivers.KEVIN],
    )

    @classmethod
    def get(cls, name: ConstructorsEnum):
        return getattr(cls, str(name.value).upper())

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

    @classmethod
    def load_prices(cls, constructor_prices: list[ConstructorPriceModel]):
        for constructor_price in constructor_prices:
            cls.get(constructor_price.name).price = float(constructor_price.price)


DRIVERS_IGNORE_LIST = [
    # Drivers.MAX,
]

CONSTRUCTORS_IGNORE_LIST = [
    # Constructors.RED_BULL,
]
