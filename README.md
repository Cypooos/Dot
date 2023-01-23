# Hypercube
A simple discord bot that run on a ubuntu server customly hosted, inspired by the game `FEZ`.

You may take a look at the code as every confidential informations is in a `.env`.

## Current setup

Add thoses to the [cron](https://doc.ubuntu-fr.org/cron) entries :
 - `@reboot cd /PATH/TO/FOLDER && ./start.sh`
 - `5 0 * * * cd PATH/TO/FOLDER && ./restart.sh`
 - `0 * * * * cd PATH/TO/FOLDER && ./start.sh`

Thoses will restart the bot on restart, and shutdown + reload the bot's code every day at midnight.

Everything is done in another `tmux` session, CF. [`start.sh`](https://github.com/Cypooos/Dot/blob/main/start.sh)
