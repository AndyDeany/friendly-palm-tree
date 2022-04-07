"""Module containing the main API."""

import sys
import signal
from time import time, sleep
from threading import Lock

from flask import Flask
from flask_restful import Api, abort
from werkzeug.exceptions import HTTPException

from ferrets import FerretsBase, Ferrets


class GracefulShutdown:
    """Class for handling a graceful shutdown of the API."""

    MAX_TIMEOUT = 60

    shutdown_requested = False
    current_requests = 0
    lock = Lock()

    @classmethod
    def handle_sigint(cls, _signal, _frame):
        """Handle a SIGINT command by finishing serving ongoing requests, then shutting down."""
        if cls.shutdown_requested:  # Check shutdown isn't already in progress
            return

        print("SIGINT received. Shutting down gracefully.")
        cls.shutdown_requested = True   # Stop accepting new requests
        start_time = time()
        while time() - start_time < cls.MAX_TIMEOUT:    # Wait for ongoing requests to finish
            if cls.current_requests == 0:
                sleep(1)    # Ensure responses have time to be returned
                sys.exit(0)
            sleep(1)
        sys.exit(0)     # Exit after MAX_TIMEOUT regardless

    @classmethod
    def add_request(cls):
        """Track a new request."""
        with cls.lock:
            cls.current_requests += 1

    @classmethod
    def remove_request(cls):
        """Track a completed request."""
        with cls.lock:
            cls.current_requests -= 1


signal.signal(signal.SIGINT, GracefulShutdown.handle_sigint)


app = Flask(__name__)


@app.before_request
def before_request():
    """Set up before every request."""
    GracefulShutdown.add_request()
    if GracefulShutdown.shutdown_requested:
        abort(503, message="The API is offline.")


@app.teardown_request
def teardown_request(_error=None):
    """Tear down after every request, including those that throw an exception."""
    GracefulShutdown.remove_request()  # Ensure requests that error are also removed


@app.errorhandler(404)
def not_found(_error):
    """Handle all uncaught 404s from incorrect URLs."""
    return {"message": "The URL could not be found. Try '/ferrets'."}, 404


class EnhancedApi(Api):
    """Class enhancing the basic flask_restful.Api class."""

    def handle_error(self, e):
        """Handle errors thrown by API calls."""
        if isinstance(e, HTTPException):
            return super().handle_error(e)  # Handle abort() calls normally
        # And catch other thrown Exceptions to give a custom 500 payload.
        return {"message": "There was an Internal Server Error. Oh no."}, 500


if __name__ == '__main__':
    api = EnhancedApi(app)
    api.add_resource(FerretsBase, "/ferrets")
    api.add_resource(Ferrets, "/ferrets/<name>")
    app.run(debug=True)
