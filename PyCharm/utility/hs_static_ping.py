#!/usr/bin/env python
# ping a list of host with threads for increase speed
# use standard linux /bin/ping utility

from threading import Thread
import subprocess

try:
    import queue
except ImportError:
    import Queue as queue
import re

# some global vars
num_threads = 20
ips_q = queue.Queue()
out_q = queue.Queue()

# build IP array

ips = ["20.2.10.3", "20.2.10.4", "20.2.10.5", "20.2.10.6", "20.2.11.3", "20.2.11.4", "20.2.11.5", "20.2.11.6",
       "20.2.12.3", "20.2.12.4", "20.2.12.5", "20.2.12.6", "20.2.13.3", "20.2.13.4", "20.2.13.5", "20.2.13.6",
       "20.2.14.3", "20.2.14.4", "20.2.14.5", "20.2.14.6", "20.2.15.3", "20.2.15.4", "20.2.15.5", "20.2.15.6",
       "20.2.16.3", "20.2.16.4", "20.2.17.3", "20.2.17.4", "20.2.18.3", "20.2.18.4", "20.2.18.5", "20.2.18.6",
       "20.2.19.3", "20.2.19.4", "20.2.20.3", "20.2.20.4", "20.2.21.3", "20.2.21.4",
       "20.3.10.3", "20.3.10.4",
       "20.3.11.3", "20.3.11.4", "20.3.11.5", "20.3.11.6", "20.3.11.7", "20.3.11.8", "20.3.11.9", "20.3.11.10",
       "20.3.12.3", "20.3.12.4", "20.3.13.3", "20.3.13.4", "20.3.13.5", "20.3.13.6", "20.3.14.3", "20.3.14.4",
       "20.3.15.3", "20.3.15.4", "20.3.15.5", "20.3.15.6", "20.3.16.3", "20.3.16.4", "20.3.16.5", "20.3.16.6",
       "20.3.17.3", "20.3.17.4", "20.3.18.3", "20.3.18.4", "20.3.18.5", "20.3.18.6", "20.3.18.7", "20.3.18.8",
       "20.3.19.3", "20.3.19.4", "20.3.19.5", "20.3.19.6", "20.3.19.7", "20.3.19.8", "20.3.19.9", "20.3.19.10",
       "20.3.20.3", "20.3.20.4", "20.3.20.5", "20.3.20.6", "20.3.20.7", "20.3.20.8", "20.3.20.9", "20.3.20.10",
       "20.3.21.3", "20.3.21.4", "20.3.21.5", "20.3.21.6", "20.3.22.3", "20.3.22.4", "20.3.22.5", "20.3.22.6",
       "20.3.23.3", "20.3.23.4", "20.3.23.5", "20.3.23.6"
       ]


# thread code : wraps system ping command
def thread_pinger(i, q):
    """Pings hosts in queue"""
    while True:
        # get an IP item form queue
        ip = q.get()
        # ping it
        args = f"ping -c 1 -W 1 {str(ip)}"
        p_ping = subprocess.Popen(args,
                                  shell=True,
                                  stdout=subprocess.PIPE)
        # save ping stdout
        if (p_ping.wait() != 0):
            out_q.put("FAIL " + str(ip))
        # else:
        #     out_q.put("FAIL " + str(ip))

        # update queue : this ip is processed
        q.task_done()


# start the thread pool
for i in range(num_threads):
    worker = Thread(target=thread_pinger, args=(i, ips_q))
    worker.setDaemon(True)
    worker.start()

# fill queue
for ip in ips:
    ips_q.put(ip)

# wait until worker threads are done to exit
ips_q.join()

# print result
while True:
    try:
        msg = out_q.get_nowait()
    except queue.Empty:
        break
    print(msg)
