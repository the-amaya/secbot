# secbot

<p align="center">
	<img alt="GitHub language count" src="https://img.shields.io/github/languages/count/the-amaya/secbot?style=plastic">
	<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/the-amaya/secbot?style=plastic">
	<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/the-amaya/secbot?style=plastic">
	<img alt="GitHub" src="https://img.shields.io/github/license/the-amaya/secbot?style=plastic">
	<img alt="GitHub contributors" src="https://img.shields.io/github/contributors/the-amaya/secbot?style=plastic">
	<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/the-amaya/secbot?style=plastic">
	<img alt="Scrutinizer code quality (GitHub/Bitbucket)" src="https://img.shields.io/scrutinizer/quality/g/the-amaya/secbot?style=plastic">
</p>

## A discord bot that does things for me. Maybe it can do things for you too.

<img src="https://raw.githubusercontent.com/the-amaya/secbot/main/assets/cam.png"  width="128" height="128">

## setup/install

#### automatic install:

###### ubuntu 22.04:

1. Log in as the user you want the bot to run as. the bot will be installed in `~/secbot`
2. run the installation script with `bash <(curl https://raw.githubusercontent.com/the-amaya/secbot/main/setup.sh)`
3. the setup script will check to see if you have python3 and python3-venv available, and if not will attempt to install
   them (the script will prompt for a sudo password to perform the `apt` install)
4. the script will then clone the github project or update it if it is already downloaded and then run main.py
5. for subsequent runs of the bot run `bash ~/secbot/setup.sh` this will check for updates and start the bot.

#### manual install:

###### any os with python3 available:

1. ensure you have python3 and (optionally) python3-venv installed and available to the user you want to run the bot
   under.
2. as the user you want to run the bot under, clone this repository. on ubuntu this
   is `git clone https://github.com/the-amaya/secbot secbot`
3. (optionally) create a python venv in the secbot folder. on ubuntu `cd secbot` `python3 -m venv env`
4. install the requirements from requirements.txt. on ubuntu activate the environment `source env/bin/activate` then
   install the requirements with pip 'pip install -r requirements.txt'
5. run `main.py` however is appropriate for your system, possibly `python main.py` or `python3 main.py`

## requirements

- python3
- packages listed in requirements.txt
- some cogs depend on additional settings and external APIs
    - generate - relies on a private hosted stable diffusion api. disabled by default. if you provide an api url during
      setup or in setting.ini this cog will be enabled on bot startup.
      see https://github.com/AUTOMATIC1111/stable-diffusion-webui
    - sump - relies on my sump pump monitoring project. disabled by default. if you provide an api url during setup or
      in setting.ini this cog will be enabled on bot startup. https://github.com/the-amaya/sumpPump (which is likely not
      updated)
    - weather - the weather cog now requires you to set a user-agent string in the settings. (this cog is disabled if
      the user agent is left blank. see [the cameras cog](#the-cameras-cog))
    - textgpt - relies on a private hosted LLM, I am using https://github.com/oobabooga/text-generation-webui

## Cogs

- botsettings
- cameras
- custom_reactions
- cute
- eco
- games
- generate
- loadunloadcogs
- stats
- sump
- textgpt
- weather

### The `BotSettings` cog

this cog includes functions to view/edit bot settings (the edit settings command currently does not work)

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/botsettings.png)

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/botsettings2.png)

### The `cameras` cog

grab still images from a reolink camera. this cog is disabled by default and requires manual configuration. you will
need to create `cameras.ini` see `example_cameras.ini` for the basic layout. if `cameras.ini` exists the cog is loaded.

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/cameras.png)

### The `custom_reactions` cog

this cog provides custom reactions on trigger words and includes commands to set up and manage the custom reactions

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/custom_reactions.png)

### The `cute` cog

this cog will rate how 'cute' a user is

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/cute.png)

### The `eco` cog

this cog provides the basis for the economy. Currently it supports the following commands:
- balance: check your balance or the balance of another user
- transfer: transfer coins from your balance to another user
- earn: earn coins (mostly for testing, this command will go away as more function is implemented)

The economy data is stored in a database for use with other cogs.

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/economy.png)

### The `games` cog

this cog currently just has the 8ball but will eventually have other games

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/games.png)

### The `generate` cog

this cog interfaces with a stable diffusion API to generate images from prompts. This cog is disabled by default but if
you provide your API url during setup or set it in settings.ini this cog will be enabled on bot startup automatically

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/generate.png)

### The `loadunloadcogs` cog

this cog provides functions to load, unload and reload other cogs. this can be useful on settings changes or if making
changes to the cog code itself.

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/loadunloadcogs.png)

### The `stats` cog

This cog tracks user and bot stats

The following commands are provided:

- about
- botstats
- ping
- user_stats

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/stats.png)

### The `sump` cog

This cog is designed to interface with https://github.com/the-amaya/sumpPump -that page likely needs updated to include
what this interfaces with. if someone is actually interested in building the sumpPump project and interfacing a version
of this bot with it let me know, otherwise I will get to it when I get to it. This cog is disabled by default but if you
provide your API url during setup or set it in settings.ini this cog will be enabled on bot startup automatically

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/sump.png)

### The `textgpt` cog

This cog provides an interface for a self-hosted LLM
currently only offers `gpt` command, which is a one-shot interaction. future updates will add contextual conversations.

this cog requires you configure the url for the API in settings.ini

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/textgpt.png)

### The `weather` cog

This cog provides weather related commands including radar and forecast. this cog now requires a user-agent string be
set. you can do this during setup or set it manually in the settings.ini file. you only need to provide the string,
i.e. "my_discord_bot.example.com, contact@example.com" without any prefix

This cog will now take a US postal code or city name to determine location, and should be much faster finding the
closest radar.

more information about the user-agent string
from [the weather.gov api documentation](https://www.weather.gov/documentation/services-web-api#:~:text=Request%20new%20features-,Authentication,-A%20User%20Agent)

`
A User Agent is required to identify your application. This string can be anything, and the more unique to your application the less likely it will be affected by a security event. If you include contact information (website or email), we can contact you if your string is associated to a security event. This will be replaced with an API key in the future.
User-Agent: (myweatherapp.com, contact@myweatherapp.com)
`

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/weather.png)

Special thanks to [@xcjs](https://github.com/xcjs) for help with the radar locations
