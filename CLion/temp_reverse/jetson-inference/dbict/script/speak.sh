#!/bin/bash

prev_tts=`ps -ef | grep 'python3 /home/user/jetson-inference/dbict/python/tts_speak.py' | grep -v 'grep' | awk '{print $2}'`



if [[ -z $prev_tts ]]; then
    echo "start tts program"
    python3 /home/user/jetson-inference/dbict/python/tts_speak.py &
else
    exit 0
fi

while true
do
    tts=`ps -ef | grep 'python3 /home/user/jetson-inference/dbict/python/tts_speak.py' | grep -v 'grep' | awk '{print $2}'`
    if [[ -z $tts ]]; then
        echo "restart tts program"
        python3 /home/user/jetson-inference/dbict/python/tts_speak.py &
    fi
    sleep 2
done
