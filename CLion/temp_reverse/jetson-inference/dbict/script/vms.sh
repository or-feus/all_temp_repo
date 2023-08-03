#!/bin/bash

prev_vms=`ps -ef | grep 'python3 /home/user/det_to_vms.py' | grep -v 'grep' | awk '{print $2}'`



if [[ -z $prev_vms ]]; then
    echo "start vms program"
    echo "123" | sudo -S nohup python3 /home/user/det_to_vms.py &
else
    exit 0
fi

while true
do
    vms=`ps -ef | grep 'python3 /home/user/det_to_vms.py' | grep -v 'grep' | awk '{print $2}'`
    if [[ -z $vms ]]; then
        echo "restart vms program"
        echo "123" | sudo -S nohup python3 /home/user/det_to_vms.py &
    fi
    sleep 2
done
