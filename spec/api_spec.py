"""File containing unit tests for functionality of the API as a whole."""
from threading import Thread
from time import time, sleep

from expects import expect, equal, be_below
from mamba import context, it
import requests

from spec.helper import BASE_URL, get_ciri_dict


response_dict = {}  # For passing info between threads


def make_blocking_request():
    """Make a request that is slow as to test that other requests made simultaneously succeed."""
    response_dict["response"] = requests.delete(BASE_URL + "/ferrets")  # Takes 5 seconds


with context("simultaenous requests"):
    with it("should handle a second request whilst handling a blocking request"):
        start_time = time()
        blocking_process = Thread(target=make_blocking_request)
        blocking_process.start()

        sleep(1)    # Ensure the first request has time to start
        response = requests.get(BASE_URL + "/ferrets/Ciri")
        expect(response.json()).to(equal(get_ciri_dict()))
        expect(response.status_code).to(equal(200))
        # Check that the request was completed whilst the blocking request was ongoing (within 1s)
        expect(time() - start_time).to(be_below(2))

        blocking_process.join()
        slow_response = response_dict["response"]
        expected_json = {"message": "DELETE requests are not supported for this resource."}
        expect(slow_response.json()).to(equal(expected_json))
        expect(slow_response.status_code).to(equal(405))
