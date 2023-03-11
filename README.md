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

<img src="https://raw.githubusercontent.com/the-amaya/secbot/main/demo/cam.svg"  width="64" height="64">

## setup/install
#### automatic install:
you can try using the included setup scripts, they may or may not work and are untested as of me writing this.

#### manual install:
download this repository, install the requirements from requirements.txt and run main.py

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
this cog includes functions to view/edit bot settings (not fully functional)

### The `cameras` cog
grab still images from a reolink camera

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/camera_cog.png)

### The `custom_reactions` cog
this cog includes commands to setup and manage custom reactions

### The `cute` cog
this cog will rate how 'cute' a user is

### The `economy` cog
this cog doesnt do much yet, but its commands all work

### The `games` cog
this cog currently just has the 8ball but will eventually have other games

### The `generate` cog
this cog interfaces with a stable diffusion API to generate images from prompts

### The `loadunloadcogs` cog
this cog provides functions to load, unload and reload other cogs

### The `stats` cog
This cog tracks user and server stats

### The `sump` cog
This cog is designed to interface with https://github.com/the-amaya/sumpPump

### The `utilities` cog
This cog provides basic utilities, currently ping and the about command

### The `weather` cog
This cog provides weather related commands including radar and forecast

![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/stats_cog.png)


## requirements
Beyond the required packages listed in requirements.txt some cogs depend on additional settings and external APIs
These cogs are disabled by default but can be enabled by editing main.py and simply uncommenting the lines

- cameras - works for reolink cameras
- generate - relies on a private hosted stable diffusion api. see https://github.com/AUTOMATIC1111/stable-diffusion-webui
- sump - relies on my sump pump monitoring project https://github.com/the-amaya/sumpPump (which is likely not updated)


## external attributions
<div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a>
from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>