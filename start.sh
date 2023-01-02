#!/bin/bash
tmux has-session -t dot_bot 2>/dev/null
if [ $? != 0 ]; then
    git reset --hard HEAD
    git pull
    chmod 755 ./start.sh
    chmod 755 ./restart.sh
    tmux new-session -d -s dot_bot
    tmux send-keys -t dot_bot "python3 main.py" Enter
fi