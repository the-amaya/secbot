#!/bin/bash

#set install path
INSTALL_PATH=~/secbot

#clone project if not already done
if [ ! -d $INSTALL_PATH ]; then
   git clone https://github.com/the-amaya/secbot $INSTALL_PATH
fi

#check for updates
cd $INSTALL_PATH
git pull

#create virtual environment if not already done
if [ ! -d $INSTALL_PATH/venv ]; then
   python -m venv $INSTALL_PATH/venv
fi

#activate virtual environment
source $INSTALL_PATH/venv/bin/activate

#install requirements
pip install -r $INSTALL_PATH/requirements.txt

#check for settings.ini
if [ ! -f $INSTALL_PATH\settings.ini ]; then
    echo you need to configure your settings before you can run the bot
    echo you can rename example_settings.ini to settings.ini
    echo and then edit settings.ini with at least your bot token. all other settings use sane values
    exit
fi

#launch main.py
python $INSTALL_PATH/main.py