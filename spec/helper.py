"""File containing general information shared between multiple tests."""
from datetime import date as _date


BASE_URL = "http://127.0.0.1:5000"


def make_ferret_dict(ferret_name, dob, color):
    """Create the expect ferret dict for the ferret with the given information."""
    today = _date.today()
    return {
        "name": ferret_name,
        "age": today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)),
        "color": color,
    }


# Create dicts when requests are made (instead of now) so age is accurate.
get_ciri_dict = lambda: make_ferret_dict("Ciri", _date(2019, 9, 13), "Albino")
get_slinky_dict = lambda: make_ferret_dict("Slinky", _date(2021, 4, 6), "Black Sable")
get_cerberus_dict = lambda: make_ferret_dict("Cerberus", _date(2015, 12, 31), "Chocolate")
get_georgia_dict = lambda: make_ferret_dict("Georgia", _date(2017, 1, 1), "Chocolate")
