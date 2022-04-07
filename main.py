"""Module containing the main API."""

import sys
import signal
from time import time, sleep

from flask import Flask
from flask_restful import Api, abort

from ferrets import FerretsBase, Ferrets


class GracefulShutdown:
    """Class for handling a graceful shutdown of the API."""

    MAX_TIMEOUT = 60

    shutdown_requested = False
    current_requests = []   # Thread safe counting of current requests

    @classmethod
    def handle_sigint(cls, sig, frame):
        """Handle a SIGINT command by finishing serving ongoing requests, then shutting down."""
        if cls.shutdown_requested:  # Check shutdown isn't already in progress
            return

        print("SIGINT received. Shutting down gracefully.")
        cls.shutdown_requested = True   # Stop accepting new requests
        start_time = time()
        while time() - start_time < cls.MAX_TIMEOUT:    # Wait for ongoing requests to finish
            if not cls.current_requests:
                sleep(1)    # Ensure responses have time to be returned
                sys.exit(0)
            sleep(1)
        sys.exit(0)     # Exit after MAX_TIMEOUT regardless

    @classmethod
    def add_request(cls):
        """Track a new request."""
        cls.current_requests.append(0)

    @classmethod
    def remove_request(cls):
        """Track a completed request."""
        cls.current_requests.pop()


signal.signal(signal.SIGINT, GracefulShutdown.handle_sigint)


if __name__ == '__main__':
    app = Flask(__name__)

    @app.before_request
    def before_request():
        GracefulShutdown.add_request()
        if GracefulShutdown.shutdown_requested:
            abort(503, message="The API is offline.")

    @app.after_request
    def after_request(response):
        GracefulShutdown.remove_request()
        return response

    @app.teardown_request
    def teardown_request(error=None):
        if error is not None:
            GracefulShutdown.remove_request()   # Ensure requests that error are also removed


    api = Api(app)
    api.add_resource(FerretsBase, "/ferrets")
    api.add_resource(Ferrets, "/ferrets/<name>")
    app.run(debug=True)
