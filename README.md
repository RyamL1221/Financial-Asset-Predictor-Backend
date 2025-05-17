# Financial Asset Predictor Backend

## Cloning the Repository:

`git clone https://github.com/RyamL1221/The-Game-Counter-Backend`

## Setting up Virtual Environment

1. Go to your project’s root directory, then: `python -m venv venv` 
2. Prepare the virtual environment: `venv\Scripts\activate.bat`
3. Activate the virtual environment: `venv\Scripts\Activate.ps1`
4. Use pip like usual: `pip install -r requirements.txt`

## Running the App

### Before you run the app, make sure to set up your .env file.

1. Run the app `python -m flask run`
2. Run a specific unit test: `python -m unittest tests.[filename minus .py]`
3. Run all unit tests: `python -m unittest discover -s tests`

`$env:PYTHONPATH = "."`
