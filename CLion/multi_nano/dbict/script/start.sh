#!/bin/bash

pid1=`ps -ef | grep  "detectnet-camera" | grep -v "grep" | awk '{print $2}'`

if [[ -z $pid1 ]]
then
    echo '123' | sudo -S /home/user/jetson-inference/build/aarch64/bin/detectnet-camera --network coco-chair
else
    exit 0
fi

while [ 1 ]
do
    pid=`ps -ef | grep "detectnet-camera" | grep -v 'grep' | awk '{print $2}'`

    if [[ -z $pid ]]
    then
        echo '123' | sudo -S /home/user/jetson-inference/build/aarch64/bin/detectnet-camera --network coco-chair
    fi
    sleep 2
done
