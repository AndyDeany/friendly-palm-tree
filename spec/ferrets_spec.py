"""File containing unit tests for the functionality of the /ferrets endpoint."""
# pylint: disable=invalid-name

from expects import expect, equal
from mamba import context, it
import requests

from spec.helper import (BASE_URL,
                         get_ciri_dict, get_georgia_dict, get_slinky_dict, get_cerberus_dict)


noodle_json = {"name": "Noodle", "dob": "2022-02-26", "color": "Silver"}


with context("/ferrets base endpoint"):
    with it("should return all ferrets, in alphabetical order by name"):
        response = requests.get(BASE_URL + "/ferrets")
        expect(response.json()).to(equal({"ferrets": [get_cerberus_dict(), get_ciri_dict(),
                                                       get_georgia_dict(), get_slinky_dict()]}))
        expect(response.status_code).to(equal(200))

    with it("should return all ferrets that match a given search parameter"):
        response = requests.get(BASE_URL + "/ferrets", params={"color": "Chocolate"})
        expect(response.json()).to(equal({"ferrets": [get_cerberus_dict(), get_georgia_dict()]}))
        expect(response.status_code).to(equal(200))

    with it("should gracefully return no ferrets when none match a given search parameter"):
        response = requests.get(BASE_URL + "/ferrets", params={"color": "Silver"})
        expect(response.json()).to(equal({"ferrets": []}))
        expect(response.status_code).to(equal(200))

    with it("should return an appropriate 400 message if an unknown search parameter is given"):
        response = requests.get(BASE_URL + "/ferrets", params={"length": "32"})
        expect(response.json()).to(equal({"message": "Bad Request. Unknown parameter 'length'."}))
        expect(response.status_code).to(equal(400))

    with it("should do this even if a valid parameter is also given"):
        response = requests.get(BASE_URL + "/ferrets", params={"color": "Albino", "length": "32"})
        expect(response.json()).to(equal({"message": "Bad Request. Unknown parameter 'length'."}))
        expect(response.status_code).to(equal(400))

    with it("should return 501 Not Implemented if a POST request is made"):
        noodle_json = {"name": "Noodle", "dob": "2022-02-26", "color": "Silver"}
        expected_message = "POST requests are not implemented for this resource."
        response = requests.post(BASE_URL + "/ferrets", json=noodle_json)
        expect(response.json()).to(equal({"message": expected_message}))
        expect(response.status_code).to(equal(501))

    with it("should return 403 Forbidden if a PUT request is made"):
        expected_message = "PUT requests are not allowed on this resource."
        response = requests.put(BASE_URL + "/ferrets", json={})
        expect(response.json()).to(equal({"message": expected_message}))
        expect(response.status_code).to(equal(403))

    with it("should return 403 Forbidden if a DELETE request is made"):
        expected_message = "DELETE requests are not allowed on this resource."
        response = requests.delete(BASE_URL + "/ferrets")
        expect(response.json()).to(equal({"message": expected_message}))
        expect(response.status_code).to(equal(403))


with context("/ferrets/{name} endpoint"):
    with it("should return a specific ferret's information when given their name"):
        for name, get_ferret_dict in (("Ciri", get_ciri_dict),
                                      ("Slinky", get_slinky_dict),
                                      ("Cerberus", get_cerberus_dict),
                                      ("Georgia", get_georgia_dict)):
            response = requests.get(BASE_URL + f"/ferrets/{name}")
            expect(response.json()).to(equal(get_ferret_dict()))
            expect(response.status_code).to(equal(200))

    with it("should do so in a case-insenstive manner"):
        for name in ("ciri", "CIRI", "cIrI"):
            response = requests.get(BASE_URL + f"/ferrets/{name}")
            expect(response.json()).to(equal(get_ciri_dict()))
            expect(response.status_code).to(equal(200))

    with it("should return an appropriate 404 message if a requested ferret can't be found"):
        expected_message = "Ferret not found. No ferret with the name 'Noodle' exists."
        response = requests.get(BASE_URL + "/ferrets/Noodle")
        expect(response.json()).to(equal({"message": expected_message}))
        expect(response.status_code).to(equal(404))

    with it("should return 403 Forbidden if a POST request is made"):
        expected_message = "POST requests are not allowed on this resource."
        response = requests.post(BASE_URL + "/ferrets/Ciri", json={})
        expect(response.json()).to(equal({"message": expected_message}))
        expect(response.status_code).to(equal(403))

    with it("should return 501 Not Implemented if a PUT request is made"):
        new_ciri_json = {"name": "Ciri", "dob": "2019-09-13", "color": "Silver"}
        expected_message = "PUT requests are not implemented for this resource."
        response = requests.put(BASE_URL + "/ferrets/Ciri", json=new_ciri_json)
        expect(response.json()).to(equal({"message": expected_message}))
        expect(response.status_code).to(equal(501))

    with it("should return 501 Not Implemented if a DELETE request is made"):
        expected_message = "DELETE requests are not implemented for this resource."
        response = requests.post(BASE_URL + "/ferrets/Ciri", json=noodle_json)
        expect(response.json()).to(equal({"message": expected_message}))
        expect(response.status_code).to(equal(501))
