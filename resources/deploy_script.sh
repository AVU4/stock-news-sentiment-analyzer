#!/bin/bash

PID_FILE=/tmp/flask_app_pid
if [ -f "$PID_FILE" ]; then
    echo "$PID_FILE exists."
    kill $(cat PID_FILE)
fi

nohup python3 app.py &
pid=$?
echo "$pid" > $PID_FILE