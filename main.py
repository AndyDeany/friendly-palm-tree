"""Module containing the main API."""

from datetime import date
import subprocess

from flask import Flask
from flask_restful import Resource, Api, abort


class Ferret:
    """Class for representing a ferret."""

    def __init__(self, name, dob, color):
        self.name = name
        self.dob = dob
        self.color = color

    @property
    def age(self):
        """Property containing the current age of the ferret."""
        try:    # Calling arbritrary external executable :)
            unix_time_now = int(subprocess.run(["date", "+%s"], stdout=subprocess.PIPE).stdout)
            today = date.fromtimestamp(int(unix_time_now))
        except FileNotFoundError:   # Sadly doesn't work on Windows
            today = date.today()
        return (today.year - self.dob.year -
                ((today.month, today.day) < (self.dob.month, self.dob.day)))


class Ferrets(Resource):
    """Class representing the /ferrets/<name> endpoint."""

    all_ferrets = [
        Ferret("Ciri", date(2019, 9, 13), "Albino"),
        Ferret("Slinky", date(2021, 4, 6), "Black Sable"),
        Ferret("Cerberus", date(2015, 12, 31), "Chocolate"),
        Ferret("Georgia", date(2017, 1, 1), "Chocolate"),
    ]

    def get(self, name):
        """Get the information on the ferret with the given name."""
        for ferret in self.all_ferrets:
            if ferret.name.lower() == name.lower():
                return {"name": ferret.name, "age": ferret.age, "color": ferret.color}, 200
        abort(404, message=f"Ferret not found. No ferret with the name '{name}' exists.")


class FerretsBase(Resource):
    """Class representing the base /ferrets endpoint."""


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(FerretsBase, "/ferrets")
    api.add_resource(Ferrets, "/ferrets/<name>")
    app.run(debug=True)
