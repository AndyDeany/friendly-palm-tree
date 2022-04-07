### Running the API and unit tests
* Clone the repository.
* Create a Python virtual environment in the main folder of the repo (`python -m venv venv`).
* Activate this virtual environment
  (`source venv/bin/activate` on UNIX, `.\venv\Scripts\activate\` on Windows).
* Install requirements (`python -m pip install -r test-requirements.txt`).
  If you just want to run the API and not the tests, you can just install `requirements.txt` instead.
* To run the API, use `python main.py`.
* To run the tests, in a separate window run `mamba --format=documentation`.

To browse the API in your browser or manually you can use `http://127.0.0.1:5000/ferrets`.
To get a specific ferret's information try `http://127.0.0.1:5000/ferrets/{name}`.
I'd recommend `Ciri` or `Slinky`.
