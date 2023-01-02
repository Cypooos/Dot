#!/bin/bash
tmux has-session -t dot_bot 2>/dev/null
if [ $? != 0]; then
    git pull
    tmux new-session -d -s dot_bot
    tmux send-keys -t dot_bot "python3 main.py" Enter
fi