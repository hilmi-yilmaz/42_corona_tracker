# codam_corona_tracker

This application tracks people who sat close to a recently infected person. It can be used to immediately notify students that may be at risk.
Getting the security footage and looking through it may take a longer time, so an initial check on who sat close to the infected person could save potential infections.

## Description

This program makes use of the 42 API. It asks data from the API to which people sat close to the infected person and also for how long.

## Installation and setup


## Usage
---

Run:

```sh
python3 run.py login_name date_infected how_many_days_to_check
```

- login_name: the intra login name of the infected person
- date_infected: the date the person got infected in the format day-month-year (e.g. 15-01-2021).
- how_many_days_to_check: how many days to check.

### Example

If you run:

```sh
python3 run.py hyilmaz 19-09-2021 2
```

the program will output the data for 18-09-2021 and 17-09-2021 (2 days).

## Roadmap
- Create a GUI for Codam (42 Amsterdam) specific.

## Contribute


## License
