# W' & CP calculator

This command-line tool helps you to determine your W'(w prime) and CP (critical power) values. These parameter can be helpful for your cycling training.

To use the script, you have to synchronize you data with [intervals.icu](https://www.intervals.icu/). Then download you power curve data as csv [[Link to power data](https://intervals.icu/power)].

## Instructions

First, consider if you want to setup an virtual environment.

```{bash}
python3 -m venv venv
source  source  ./venv/bin/activate
```

Then install the required packages

```{bash}
python -m pip install -r requirements.txt 
```

To finally run the program run

```{bash}
python main.py path
```

where `path` is the path the csv-file you downloaded before that contains your power data (e.g.: `athlete_i00000_power_curves.csv`)