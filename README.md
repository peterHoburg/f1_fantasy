# F1 Fantasy Utilities
I am really lazy, so I built a util that when given an expected qualifying and race result tell you the best team that
stays within the $100m budget.

THIS IS SUPER DUMB. No AI, no, ML. You pick the order the driver will finish in, the script brute forces a good team.

THIS IS A PERSONAL PROJECT. I spent a few hours working on this on and off. If you have any issues feel free to open
a PR or an issue. I will get around to making this more user-friendly at some point. Or not.

## Installation
Install poetry https://python-poetry.org/docs/#installation
run `poetry install` in the root directory

## Usage
### Data files
#### Pricing
All pricing is in `f1_fantasy/src/f1_fantasy/data/<constructors_prices,driver_prices>/<yyymmdd>.csv`.
Example files are provided.

#### Input
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
