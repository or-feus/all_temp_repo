#!/usr/bin/env python
# ping a list of host with threads for increase speed
# use standard linux /bin/ping utility

import subprocess
from threading import Thread

try:
    import queue
except ImportError:
    import Queue as queue

# some global vars
num_threads = 40
ips_q = queue.Queue()
out_q = queue.Queue()

# build IP array
ips = []
for i in range(1, 200):
    ips.append("192.168.1." + str(i))


# thread code : wraps system ping command
def thread_pinger(i, q):
    """Pings hosts in queue"""
    while True:
        # get an IP item form queue
        ip = q.get()
        # ping it
        # args = ['/bin/ping', '-c', '1', '-W', '1', str(ip)]
        cli = f"sudo hping3 -c 1 -S {ip} -p 22"

        p_ping = subprocess.Popen(cli,
                                shell = True,
                                stdout = subprocess.PIPE,
                                encoding = 'utf-8')

        # save ping stdout
        p_ping_out = str(p_ping.communicate())
        # print(p_ping.stdout)
        # ssh_exist = "flags=SA" in p_ping.stdout
        #
        # if ssh_exist:
        #     print(f"exist ip : {ip}")
        # else :
        #     print(f"not exist ip : {ip}")
        # if p_ping.wait() == 0:

        #     # print(f"exist ip : {ip}")
        #     out_q.put("OK " + str(ip) + "--> " + str(i))
        # else:
        #     out_q.put("NO " + str(ip) + "--> " + str(i))

        # update queue : this ip is processed
        # q.task_done()


# start the thread pool
for i in range(num_threads):
    worker = Thread(target = thread_pinger, args = (i, ips_q))
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
    # print(msg)
