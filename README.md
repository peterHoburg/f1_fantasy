# F1 Fantasy Utilities
I am really lazy, so I built a util that when given an expected qualifying and race result tell you the best team that
stays within the $100m budget.

THIS IS SUPER DUMB. No AI, no, ML. You pick the order the driver will finish in, the script brute forces a good team.

THIS IS A PERSONAL PROJECT. I spent a few hours working on this on and off. If you have any issues feel free to open
a PR or an issue. I will get around to making this more user-friendly at some point. Or not.

## Installation
### Via pip
`pip install f1-fantasy`

### Via GitHub
Install poetry https://python-poetry.org/docs/#installation
run `poetry install` in the root directory

## Usage
After installing via pip or poetry navigate to a directory that you want to contain the `data` directory. This will be
referred to as the <running_dir> from now on. The data dir is a generated directory that contains the input and output
files. Run `f1-fantasy setup` to generate those files.

NOTE:

If you ever want to revert to the original input files simply run `f1-fantasy setup` again.

### Input
#### Chips
`<running_dir>/data/chips.csv`

This file contains the chips you have available. The format is:

```
chips_to_enable
<list of chips to enable one per line>
...
```
Chips available are:
```
extra_drs
```

#### Ignore constructors/drivers
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
Total: 302  Drivers: [Max Verstappen - 135 points, Carlos Sainz - 68 points, Zhou Guanyu - 12 points, Kevin Magnussen - 6 points, Lance Stroll - 5 points]  Constructors: [Ferrari - 68 points, Sauber - 8 points]
1
```

Output with ignored drivers/constructors:
```
Total: 290  Drivers: [Carlos Sainz - 102 points, Sergio Perez - 60 points, Zhou Guanyu - 12 points, Kevin Magnussen - 6 points, Pierre Gasly - 4 points]  Constructors: [Ferrari - 68 points, Mercedes - 38 points]
Total: 290  Drivers: [Carlos Sainz - 102 points, Sergio Perez - 60 points, Zhou Guanyu - 12 points, Kevin Magnussen - 6 points, Esteban Ocon - 4 points]  Constructors: [Ferrari - 68 points, Mercedes - 38 points]
2
```

Notice how neither Max nor Redbull are in the second output.

All pricing is in `f1_fantasy/src/f1_fantasy/data/<constructors_prices,driver_prices>/<yyymmdd>.csv`.
Example files are provided.



Input files are where you specify what you think the qualifying and race finishing positions will be.
These are:
```
f1_fantasy/src/f1_fantasy/data/input/qualifying_finishing_positions.csv
f1_fantasy/src/f1_fantasy/data/input/race_finishing_positions.csv
```
Example files are provided.

The positions are inferred by the order the drivers are listed in the file. The top driver is p1, last driver is p20.

#### Output
This is where the output will be written to
`f1_fantasy/src/f1_fantasy/data/output/<yyyy-mm-dd hh:mm:ss.ms>`

### Running
Run `poetry run python src/f1_fantasy/main.py`

## Known limitations
* Tokens are not really taken into account
* The 3x DRS token is always applied
* DNF/DNS are not taken into account

I have only tested this on Linux with python 3.10. Let me know if there are any issues on other platforms.


# Disclaimer
THIS IS NOT AN OFFICIAL F1 PRODUCT. I AM NOT AFFILIATED WITH F1 IN ANY WAY.

I don't know what I am doing, so this might go horribly wrong and make a terrible team. Use your brain.
