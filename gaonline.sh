#!/usr/bin/env bash
python3 ${BASH_SOURCE%/*}/main.py &
echo "booting in 3"
sleep 1
echo 2
sleep 1
echo 1
sleep 1
pid=$!
python3 ${BASH_SOURCE%/*}/cef_gui.py
kill ${pid}

