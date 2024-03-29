# F1 Fantasy Utilities
I am really lazy, so I built a util that when given an expected qualifying and race result tell you the best team that
stays within the $100m budget.

THIS IS SUPER DUMB. No AI, no, ML. You pick the order the driver will finish in, the script brute forces a good team.

THIS IS A PERSONAL PROJECT. I spent a few hours working on this on and off. If you have any issues feel free to open
a PR or an issue. I will get around to making this more user-friendly at some point. Or not.

# Installation
## Via pip
`pip install f1-fantasy`

## Via GitHub
Install poetry https://python-poetry.org/docs/#installation
run `poetry install` in the root directory

# Usage
After installing via pip or poetry navigate to a directory that you want to contain the `data` directory. This will be
referred to as the <running_dir> from now on. The data dir is a generated directory that contains the input and output
files. Run `f1-fantasy setup` to generate those files.

NOTE:

If you ever want to revert to the original input files simply run `f1-fantasy setup` again.

# Input
## Chips
`<running_dir>/data/chips.csv`

This file contains the chips you have available. The format is:

```
chip_to_enable
<list of chips to enable one per line>
```
Chips available are:
```
extra_drs
```

## Current Team
`<running_dir>/data/current_team.csv`
Your current team. If put all 5 drivers and 2 constructors in the file the transfer costs will be taken into account.


## Finishing Positions qualifying/race
`<running_dir>/data/finishing_positions_qualifying.csv` and `<running_dir>/data/finishing_positions_race.csv`

Input files are where you specify what you think the qualifying and race finishing positions will be.

The positions are inferred by the order the drivers are listed in the file. The top driver is p1, last driver is p20.

The finishing position files contain the results from the first race of the 2024 season.

## Ignore constructors/drivers
`<running_dir>/data/ignore_constructors.csv` and `<running_dir>/data/ignore_drivers.csv`

These files contain the constructors and drivers you want to ignore in the final calculation. For example, if you want
to ignore `Max` and `Redbull` the files would look like

`<running_dir>/data/ignore_constructors.csv`
```
constructor_name
RED_BULL
```

`<running_dir>/data/ignore_drivers.csv`
```
driver_name
MAX
```

Output without ignored drivers/constructors:
```
Team:
Total points: 301

Drivers:
Max Verstappen - 135 points: breakdown: qualifying: 10 race_position: 25 race_position_changed: 0 race_overtake_bonus: 0  fastest_lap: 10  drs_multiplier: 3  total_pre_drs: 45
Carlos Sainz - 68 points: breakdown: qualifying: 7 race_position: 15 race_position_changed: 1 race_overtake_bonus: 1  driver_of_the_day: 10  drs_multiplier: 2  total_pre_drs: 34
Zhou Guanyu - 12 points: breakdown: qualifying: 0 race_position: 0 race_position_changed: 6 race_overtake_bonus: 6  total_pre_drs: 12
Kevin Magnussen - 6 points: breakdown: qualifying: 0 race_position: 0 race_position_changed: 3 race_overtake_bonus: 3  total_pre_drs: 6
Esteban Ocon - 4 points: breakdown: qualifying: 0 race_position: 0 race_position_changed: 2 race_overtake_bonus: 2  total_pre_drs: 4

Constructors:
Ferrari - 68 points breakdown: qualifying: 16 driver_qualifying_bonus: 10 race_position: 27 race_position_changed: -1 race_overtake_bonus: 1  fastest_pitstop: 10  second_fastest_pitstop: 5
Sauber - 8 points breakdown: qualifying: 0 driver_qualifying_bonus: -1 race_position: 0 race_position_changed: 3 race_overtake_bonus: 6
```

Output with ignored drivers/constructors:
```
Total teams: 1
Team:
Total points: 284

Drivers:
Carlos Sainz - 102 points: breakdown: qualifying: 7 race_position: 15 race_position_changed: 1 race_overtake_bonus: 1  driver_of_the_day: 10  drs_multiplier: 3  total_pre_drs: 34
Sergio Perez - 60 points: breakdown: qualifying: 6 race_position: 18 race_position_changed: 3 race_overtake_bonus: 3  drs_multiplier: 2  total_pre_drs: 30
Zhou Guanyu - 12 points: breakdown: qualifying: 0 race_position: 0 race_position_changed: 6 race_overtake_bonus: 6  total_pre_drs: 12
Kevin Magnussen - 6 points: breakdown: qualifying: 0 race_position: 0 race_position_changed: 3 race_overtake_bonus: 3  total_pre_drs: 6
Logan Sargeant - -2 points: breakdown: qualifying: 0 race_position: 0 race_position_changed: -2 race_overtake_bonus: 0  total_pre_drs: -2

Constructors:
Ferrari - 68 points breakdown: qualifying: 16 driver_qualifying_bonus: 10 race_position: 27 race_position_changed: -1 race_overtake_bonus: 1  fastest_pitstop: 10  second_fastest_pitstop: 5
Mercedes - 38 points breakdown: qualifying: 10 driver_qualifying_bonus: 10 race_position: 16 race_position_changed: 0 race_overtake_bonus: 2
```

Notice how neither Max nor Redbull are in the second output.


## Pricing constructors/drivers
`<running_dir>/data/price_constructors.csv` and `<running_dir>/data/price_drivers.csv`
This is where you specify the price of the drivers and constructors. The format is:

```
name,price
<name all caps>,<price>
```

Both files already have all driver and constructors.

WARNING: The current prices might not be correct! Please double-check the prices before running the script.

## Special Points
`<running_dir>/data/special_points.csv`

This is where you specify who will receive the special points for each race. The available special points are:
```
fastest_lap
driver_of_the_day
fastest_pitstop
second_fastest_pitstop
third_fastest_pitstop
```

The file already contains the special points for the first race of 2024.

## Output
This is where the output will be written to
`<running_dir>/data/output/<epoch_time>`

# Running
## Via pip
Run `f1-fantasy run`

## Via poetry
Run `poetry run python src/f1_fantasy/main.py`

# Known limitations
* Tokens are not really taken into account
* The 3x DRS token is always applied
* DNF/DNS are not taken into account

I have only tested this on Linux with python 3.10. Let me know if there are any issues on other platforms.


# Disclaimer
THIS IS NOT AN OFFICIAL F1 PRODUCT. I AM NOT AFFILIATED WITH F1 IN ANY WAY.

I don't know what I am doing, so this might go horribly wrong and make a terrible team. Use your brain.
