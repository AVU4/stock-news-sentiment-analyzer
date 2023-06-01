#!/bin/bash

PID_FILE=/tmp/flask_app_pid
if [ -f "$PID_FILE" ]; then
    echo "$PID_FILE exists."
    kill $(cat PID_FILE)
fi

python3 app.py 1> log.txt &
pid=$?
echo "$pid" > $PID_FILE

disown