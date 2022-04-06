"""Module containing the main API."""

from flask import Flask
from flask_restful import Api

from ferrets import FerretsBase, Ferrets


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(FerretsBase, "/ferrets")
    api.add_resource(Ferrets, "/ferrets/<name>")
    app.run(debug=True)
