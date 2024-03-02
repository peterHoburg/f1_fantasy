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
        self._race_position = value

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

#
# def get_constructors():
#     constructors = [
#         Constructor(
#             name="Red Bull Racing",
#             price=27.9,
#             drivers=[
#                 Driver(name="Max Verstappen", team="Red Bull Racing", price=30.0),
#                 Driver(name="Sergio Perez", team="Red Bull Racing", price=20.8),
#             ],
#         ),
#         Constructor(
#             name="McLaren",
#             price=23.2,
#             drivers=[
#                 Driver(name="Lando Norris", team="McLaren", price=23.0),
#                 Driver(name="Oscar Piastri", team="McLaren", price=19.0),
#             ],
#         ),
#         Constructor(
#             name="Mercedes",
#             price=20.1,
#             drivers=[
#                 Driver(name="Lewis Hamilton", team="Mercedes", price=19.3),
#                 Driver(name="George Russell", team="Mercedes", price=18.8),
#             ],
#         ),
#         Constructor(
#             name="Ferrari",
#             price=19.3,
#             drivers=[
#                 Driver(name="Charles Leclerc", team="Ferrari", price=19.1),
#                 Driver(name="Carlos Sainz", team="Ferrari", price=18.5),
#             ],
#         ),
#         Constructor(
#             name="Aston Martin",
#             price=13.6,
#             drivers=[
#                 Driver(name="Fernando Alonso", team="Aston Martin", price=15.8),
#                 Driver(name="Lance Stroll", team="Aston Martin", price=10.7),
#             ],
#         ),
#         Constructor(
#             name="RB",
#             price=8.5,
#             drivers=[
#                 Driver(name="Daniel Ricciardo", team="RB", price=9.0),
#                 Driver(name="Yuji Tsunoda", team="RB", price=8.0),
#             ],
#         ),
#         Constructor(
#             name="Alpine",
#             price=8.4,
#             drivers=[
#                 Driver(name="Pierre Gasly", team="Alpine", price=7.8),
#                 Driver(name="Esteban Ocon", team="Alpine", price=7.8),
#             ],
#         ),
#         Constructor(
#             name="Williams",
#             price=6.3,
#             drivers=[
#                 Driver(name="Alexander Albon", team="Williams", price=7.0),
#                 Driver(name="Logan Sargeant", team="Williams", price=5.5),
#             ],
#         ),
#         Constructor(
#             name="Sauber",
#             price=6.6,
#             drivers=[
#                 Driver(name="Zhou Guanyu", team="Sauber", price=6.6),
#                 Driver(name="Valtteri Bottas", team="Sauber", price=6.4),
#             ],
#         ),
#         Constructor(
#             name="Haas",
#             price=6.3,
#             drivers=[
#                 Driver(name="Nico Hulkenberg", team="Haas", price=6.4),
#                 Driver(name="Kevin Magnussen", team="Haas", price=6.2),
#             ],
#         ),
#     ]
#     return constructors
#
#
# def get_driver_quali_order():
#     drivers = [
#         DRIVERS.max,
#         DRIVERS.charles,
#         DRIVERS.george,
#         DRIVERS.carlos,
#         DRIVERS.sergio,
#         DRIVERS.fernando,
#         DRIVERS.lando,
#         DRIVERS.oscar,
#         DRIVERS.lewis,
#         DRIVERS.nico,
#
#         DRIVERS.yuki,
#         DRIVERS.lance,
#         DRIVERS.alexander,
#         DRIVERS.daniel,
#         DRIVERS.kevin,
#
#         DRIVERS.valtteri,
#         DRIVERS.zhou,
#         DRIVERS.logan,
#         DRIVERS.esteban,
#         DRIVERS.pierre,
#     ]
#     return drivers
#
#
# def get_driver_race_order():
#     DRIVERS.max.fastest_lap = True
#     DRIVERS.max.driver_of_the_day = True
#     drivers = [
#         DRIVERS.max,
#         DRIVERS.charles,
#         DRIVERS.george,
#
#         DRIVERS.sergio,  # ++
#         DRIVERS.carlos,
#
#         DRIVERS.lando,  # ++
#         DRIVERS.fernando,
#
#         DRIVERS.lewis,  # ++
#         DRIVERS.oscar,
#
#         DRIVERS.nico,
#
#         DRIVERS.yuki,
#         DRIVERS.lance,
#         DRIVERS.alexander,
#         DRIVERS.daniel,
#         DRIVERS.kevin,
#         DRIVERS.valtteri,
#         DRIVERS.zhou,
#         DRIVERS.logan,
#         DRIVERS.esteban,
#         DRIVERS.pierre,
#     ]
#     return drivers
#
#
# def compute_quali_points(driver_quali_order):
#     for position, driver in enumerate(driver_quali_order):
#         if position < 10:
#             driver.points = 10 - position
#
#
# def compute_race_points(driver_quali_order, driver_race_order):
#     for position_quali, driver_quali in enumerate(driver_quali_order):
#         for position_race, driver_race in enumerate(driver_race_order):
#             if driver_quali.name == driver_race.name:
#                 if position_race < 10:
#                     driver_race.points = driver_race.points + race_place_points[position_race]
#                 position_delta = position_quali - position_race
#                 if position_delta > 0:
#                     driver_race.points = driver_race.points + position_delta * 2
#                 elif position_delta < 0:
#                     driver_race.points = driver_race.points + position_delta
#                 print(position_delta)
#                 break
#
#
# def compute_fastest_lap_points(driver_race_order):
#     for position_race, driver_race in enumerate(driver_race_order):
#         if position_race < 10 and driver_race.fastest_lap is True:
#             driver_race.points = driver_race.points + 10
#             return
#
# def compute_driver_of_the_day_points(driver_race_order):
#     for position_race, driver_race in enumerate(driver_race_order):
#         if driver_race.driver_of_the_day is True:
#             driver_race.points = driver_race.points + 10
#             return
#
# def compute_points(driver_quali_order, driver_race_order):
#     compute_quali_points(driver_quali_order)
#     compute_race_points(driver_quali_order, driver_race_order)
#
#     compute_fastest_lap_points(driver_race_order)
#     compute_driver_of_the_day_points(driver_race_order)
#
#
# def compute_constructor_points():
#     for _, constructor in CONSTRUCTORS:
#         for driver in constructor.drivers:
#             constructor.points = constructor.points + driver.points
#         if constructor.fastest_pitstop:
#             constructor.points = constructor.points + 10
#         if constructor.second_fastest_pitstop:
#             constructor.points = constructor.points + 5
#         if constructor.third_fastest_pitstop:
#             constructor.points = constructor.points + 3
#
#
#
#
# def main():
#     driver_quali_order = get_driver_quali_order()
#     driver_race_order = get_driver_race_order()
#     compute_points(driver_quali_order, driver_race_order)
#     compute_constructor_points()
#     # print(DRIVERS)
#     print(CONSTRUCTORS)
#
#
# if __name__ == "__main__":
#     main()
