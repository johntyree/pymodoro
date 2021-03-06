#!/bin/bash

if [[ ! -d $HOME/.config/pymodoro ]]; then
  mkdir $HOME/.config/pymodoro
fi
if [[ ! -p $HOME/.config/pymodoro/fifo ]]; then
    rm -f $HOME/.config/pymodoro/fifo
    mkfifo $HOME/.config/pymodoro/fifo
fi

PID=$(pgrep -f "python.*pymodoro.py")

if [[ $PID ]]; then
    echo "Killing existing pymodoro process: $PID"
    kill $PID
    [[ -a $HOME/.local/bin/focus_time_stop.sh ]] && sh $HOME/.local/bin/focus_time_stop.sh
else
    [[ -a $HOME/.local/bin/focus_time_start.sh ]] && sh $HOME/.local/bin/focus_time_start.sh
    touch $HOME/.config/pymodoro/pomodoro_session
    pymodoro.py -l 0 > $HOME/.config/pymodoro/fifo
    echo ' ' > $HOME/.config/pymodoro/fifo
fi
