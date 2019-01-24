#!/bin/bash

PID=$(pgrep -f "pymodoro.py")

if [[ $PID ]]; then
    echo "Killing existing pymodoro process: $PID"
    kill $PID
else
    touch $HOME/.pomodoro_session
    $HOME/projects/pymodoro/pymodoro.py -l 0 > $HOME/.pymodoro/fifo
    echo ' ' > $HOME/.pymodoro/fifo
fi
