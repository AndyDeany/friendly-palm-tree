"""Module containing classes that represent the /ferrets endpoints."""

from datetime import date
from time import sleep
import subprocess

from flask import request
from flask_restful import Resource, abort
from marshmallow import Schema, fields


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

    @staticmethod
    def post(name):
        abort(405, message="POST requests are not supported for this resource.")

    @staticmethod
    def put(name):
        abort(501, message="PUT requests are not implemented for this resource.")

    @staticmethod
    def delete(name):
        abort(501, message="DELETE requests are not implemented for this resource.")


class FerretsBase(Resource):
    """Class representing the base /ferrets endpoint."""

    class FerretFilterSchema(Schema):
        color = fields.Str()

    ferret_filter_schema = FerretFilterSchema()

    def get(self):
        """Get the information on all known ferrets."""
        parameters = request.args
        errors = self.ferret_filter_schema.validate(parameters)
        parameters = parameters.to_dict()
        if errors:
            message = "Bad Request."
            for error in errors:
                message += f" Unknown parameter '{error}'."
            abort(400, message=message)

        ferrets = []
        for ferret in Ferrets.all_ferrets:
            if self.ferret_is_valid(ferret, parameters):
                ferrets.append({"name": ferret.name, "age": ferret.age, "color": ferret.color})
        ferrets.sort(key=lambda f: f["name"])
        return {"ferrets": ferrets}

    @staticmethod
    def ferret_is_valid(ferret, search_parameters) -> bool:
        """Return whether or not the given ferret fulfils the given search parameters."""
        for parameter, value in search_parameters.items():
            if getattr(ferret, parameter) != value:
                return False
        return True

    @staticmethod
    def post():
        abort(501, message="POST requests are not implemented for this resource.")

    @staticmethod
    def put():
        abort(405, message="PUT requests are not supported for this resource.")

    @staticmethod
    def delete():
        sleep(5)    # For testing API's concurrent performance during blocking calls
        abort(405, message="DELETE requests are not supported for this resource.")
