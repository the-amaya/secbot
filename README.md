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
you can try using the included setup scripts, they may or may not work and are untested as of me writing this.

#### manual install:
download this repository, install the requirements from requirements.txt, rename example_settings.ini to settings.ini and edit accordingly and finally run main.py

## requirements
Beyond the required packages listed in requirements.txt some cogs depend on additional settings and external APIs
These cogs are disabled by default but can be enabled by editing main.py and simply uncommenting the lines

- cameras - works for reolink cameras
- generate - relies on a private hosted stable diffusion api. see https://github.com/AUTOMATIC1111/stable-diffusion-webui
- sump - relies on my sump pump monitoring project https://github.com/the-amaya/sumpPump (which is likely not updated)
- weather - the weather cog now requires you to set a user-agent string in the settings. (this cog is not disabled though)

## Cogs
- botsettings
- cameras
- custom_reactions
- cute
- economy
- games
- generate
- loadunloadcogs
- stats
- sump
- utilities
- weather

### The `BotSettings` cog
this cog includes functions to view/edit bot settings (the edit settings command currently does not work)

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/botsettings.png)

### The `cameras` cog
grab still images from a reolink camera. this cog is disabled by default. to enable it edit main.py and uncomment it.

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/cameras.png)

### The `custom_reactions` cog
this cog provides custom reactions on trigger words and includes commands to setup and manage the custom reactions

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/custom_reactions.png)

### The `cute` cog
this cog will rate how 'cute' a user is

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/cute.png)

### The `economy` cog
this cog doesnt do much yet, but its commands all work

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/economy.png)

### The `games` cog
this cog currently just has the 8ball but will eventually have other games

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/games.png)

### The `generate` cog
this cog interfaces with a stable diffusion API to generate images from prompts. This cog is disabled by default but if you are hosting your own stable diffusion API and want to use this you can edit main.py and uncomment the line for cogs.generate. dont forget to edit settings.ini as well and put in the address for your API.

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/generate.png)

### The `loadunloadcogs` cog
this cog provides functions to load, unload and reload other cogs. this can be useful on settings changes or if making changes to the cog code itself.

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/loadunloadcogs.png)

### The `stats` cog
This cog tracks user and bot stats

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/stats.png)

### The `sump` cog
This cog is designed to interface with https://github.com/the-amaya/sumpPump -that page likely needs updated to include what this interfaces with. if someone is actually interested in building the sumpPump project and interfacing a version of this bot with it let me know, otherwise I will get to it when I get to it.

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/sump.png)

### The `utilities` cog
This cog provides basic utilities, currently ping and the about command

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/utilities.png)

### The `weather` cog
This cog provides weather related commands including radar and forecast. this cog now requires a user-agent string be set in the settings.ini file. you only need to provide the string, i.e. "my_discord_bot.example.com, contact@example.com" without any prefix

This cog will now take a US postal code or city name to determine location, and should be much faster finding the closest radar.

more information about the user-agent string from [the weather.gov api documentation](https://www.weather.gov/documentation/services-web-api#:~:text=Request%20new%20features-,Authentication,-A%20User%20Agent)

`
A User Agent is required to identify your application. This string can be anything, and the more unique to your application the less likely it will be affected by a security event. If you include contact information (website or email), we can contact you if your string is associated to a security event. This will be replaced with an API key in the future.
User-Agent: (myweatherapp.com, contact@myweatherapp.com)
`

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/weather.png)

Special thanks to [@xcjs](https://github.com/xcjs) for help with the radar locations
