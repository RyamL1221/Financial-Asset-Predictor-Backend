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

## Adding new feature

1. Create a new branch and switch to it `git checkout -b feature/{new_feature_name}
2. Develop the feature, and add it to codebase with `git add *`, `git commit -m "{message}"`, and `git push`
3. After finishing the feature, create a pull request to merge with the **dev** branch
