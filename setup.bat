//Batch File

@echo off

::set install path
set INSTALL_PATH=C:\secbot

::clone project if not already done
if not exist %INSTALL_PATH% (
   git clone https://github.com/the-amaya/secbot %INSTALL_PATH%
)

::check for updates
cd /d %INSTALL_PATH%
git pull

::create virtual environment if not already done
if not exist %INSTALL_PATH%\venv (
   python -m venv %INSTALL_PATH%\venv
)

::activate virtual environment
call %INSTALL_PATH%\venv\Scripts\activate

::install requirements
pip install -r %INSTALL_PATH%\requirements.txt

::check for settings.ini
if not exist %INSTALL_PATH%\settings.ini (
    echo you need to configure your settings before you can run the bot
    echo you can rename example_settings.ini to settings.ini
    echo and then edit settings.ini with at least your bot token. all other settings use sane values
    EXIT
)

::launch main.py
python %INSTALL_PATH%\main.py