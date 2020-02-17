#!/bin/bash

PID=$(pgrep -f "pymodoro.py")

if [[ $PID ]]; then
    echo "Killing existing pymodoro process: $PID"
    kill $PID
else
    touch $HOME/.config/pymodoro/.pomodoro_session
    pymodoro.py -l 0 > $HOME/.config/pymodoro/fifo
    echo ' ' > $HOME/.config/pymodoro/fifo
fi
