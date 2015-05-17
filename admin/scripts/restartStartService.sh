#!/bin/bash
killall python
python ./main.py >> /home/ubuntu/logs/`date +\%m-\%d-\%Y`.txt 2>&1 &
disown
