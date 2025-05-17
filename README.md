# Financial Asset Predictor Backend

## Make sure to have Python and Git Installed

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
2. Run all unit tests: `pytest`
3. Run a specific unit test: `pytest tests/[file name (including .py)]`

## Running Database Scripts

1. Run time ONE TIME only: `$env:PYTHONPATH = "."`
2. To run scripts:`python -m src.scripts.[filename minus .py]`
