"""Module containing the main API."""

import sys
import signal
from time import sleep

from flask import Flask
from flask_restful import Api, abort

from ferrets import FerretsBase, Ferrets


class GracefulShutdown:
    """Class for handling a graceful shutdown of the API."""

    shutdown_requested = False
    current_requests = 0

    @classmethod
    def handle_sigint(cls, sig, frame):
        print("SIGINT received. Shutting down gracefully.")
        if not cls.shutdown_requested:  # Check shutdown isn't already in progress
            cls.shutdown_requested = True   # Stop accepting new requests
            sleep(10)
            sys.exit(0)


signal.signal(signal.SIGINT, GracefulShutdown.handle_sigint)


if __name__ == '__main__':
    app = Flask(__name__)

    @app.before_request
    def before_request():
        if GracefulShutdown.shutdown_requested:
            abort(503, message="The API is offline.")

    api = Api(app)
    api.add_resource(FerretsBase, "/ferrets")
    api.add_resource(Ferrets, "/ferrets/<name>")
    app.run(debug=True)
