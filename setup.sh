#!/bin/bash

#Configure variables here
GITHUB_PROJECT="the-amaya/secbot"
INSTALL_DIR="secbot"

#Check if project is already downloaded, if not, download it
cd ~
if [ -d "$INSTALL_DIR" ]; then
    cd $INSTALL_DIR
    git pull
else
    git clone https://github.com/$GITHUB_PROJECT $INSTALL_DIR
fi

# Check if python3 and python3-venv are installed
if ! [ -x "$(command -v python3)" ]; then
  sudo apt install python3 -y
fi
if ! [ -x "$(command -v python3-venv)" ]; then
  sudo apt install python3-venv -y
fi

# Create virtual environment and install requirements
cd $INSTALL_DIR
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Run main.py
python main.py