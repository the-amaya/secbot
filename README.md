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

### Features
- Track user stats in a sqlite3 database, respond with various stats on command `stats`
- Grab and reply with a still image from a reolink camera on command `camera`
- Check various RAID and drive health details using tw-cli (more info in the `server_stuff` cog section below)


### Upcoming features
- more function to the stats commands
- more camera support, or at least, easier support for other cameras
- support for more RAID controllers


## Cogs

\# TODO update the cogs section.


### The `general` cog
![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/general_cog.png)

This cog contains general commands and functions, currently the stats command and the event listener for it.
Eventually this will be split off into a `stats` cog.

#### Commands:
`stats`
* takes no arguments.
* replies with the number of messages the calling user has sent.


### The `management` cog
![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/management_cog.png)

This cog performs 'management' functions, this is currently limited to the camera frame grabber,
but will eventually include other network/control/iot/automation functions

#### Commands:
`camera`
* takes one argument {camera name}
* if called with 'list' as the argument (or without any argument) will return a list of valid cameras


### the `server_stuff` cog
![usage example](https://raw.githubusercontent.com/the-amaya/secbot/main/demo/server_cog.png)

This cog retrieves RAID and drive status information from a remote server (using fabric for ssh)

Currently this supports getting drive status from servers using 3ware raid controllers compatible with `tw-cli`

tw-cli is available for linux systems from the folks over at https://hwraid.le-vert.net/ -
I have plans to add support for megaRAID cards soon™

#### Commands:
`servers`
* takes no arguments
* prints a formatted table of the physical layout of the drives in each server
with the drive temperature and reallocated sector count

`racsec`
* takes one argument {server name}
* get a list of drives with reallocated sectors on a specified server

`badarray`
* takes no arguments
* get a list of non-OK arrays from all the servers

`baddrive`
* takes one argument {server name}
* get a list of non-OK drives from one of the servers


## requirements
Beyond the required packages listed in requirements.txt in order to use the `server_stuff` cog the remote server(s)
need `tw-cli` installed. You can get it for debian/ubuntu here https://hwraid.le-vert.net/

I am using private keys for SSH access with fabric,
and I added tw-cli to the sudo file so it can be run without a password prompt.


## external attributions
<div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a>
from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>