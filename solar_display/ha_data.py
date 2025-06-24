from collections import namedtuple

HaData = namedtuple("HaData", [
    "battery_level",
    "battery_charge_discharge_rate",
    "inverter_output",
    "grid_power",
    "house_consumption"
])