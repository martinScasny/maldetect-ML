@echo off

:: Create a new virtual environment
python -m venv env

:: Activate the virtual environment
.\env\Scripts\activate.bat

:: Upgrade pip to the latest version
pip install --upgrade pip

:: Install required packages using pip
pip install -r requirements.txt

:: Additional commands to run after installation (if any)

:: Deactivate the virtual environment
deactivate
