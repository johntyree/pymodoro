#!/bin/bash

PID=$(pgrep -f "pymodoro.py")

if [[ $PID ]]; then
    kill $PID
else
    touch $HOME/.pomodoro_session
    pymodoro.py -l 0 > $HOME/.pymodoro/fifo
    echo ' ' > $HOME/.pymodoro/fifo
fi
