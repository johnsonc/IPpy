# Python script to check if IP address is working or not.

import sys
import os
import platform
import subprocess
import threading
import queue
import pingparsing

def worker_func(ping_args, pending, done):
    try:
        while True:
            # Get the next address to ping.
            address = pending.get_nowait()

            ping = subprocess.Popen(ping_args + [address],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
            out, error = ping.communicate()

            # Output the result to the 'done' queue.
            done.put(({'result':out, 'ip': address}, error))
    except queue.Empty:
        # No more addresses.
        pass
    finally:
        # Tell the main thread that a worker is about to terminate.
        done.put(None)

# The number of workers.
NUM_WORKERS = 4

verbose = True

plat = platform.system()
scriptDir = sys.path[0]
hosts = os.path.join(scriptDir, 'ip_list.csv')

# The arguments for the 'ping', excluding the address.
if plat == "Windows":
    ping_args = ["ping", "-n", "2", "-l", "1", "-w", "2000"]
elif plat == "Linux":
    ping_args = ["ping", "-c", "2", "-l", "1", "-s", "1", "-W", "2"]
else:
    raise ValueError("Unknown platform")

# The queue of addresses to ping.
pending = queue.Queue()

# The queue of results.
done = queue.Queue()

# Create all the workers.
workers = []
for _ in range(NUM_WORKERS):
    workers.append(threading.Thread(target=worker_func, args=(ping_args, pending, done)))

# Put all the addresses into the 'pending' queue.
with open(hosts, "r") as hostsFile:
    for line in hostsFile:
        pending.put(line.strip())

# Start all the workers.
for w in workers:
    w.daemon = True
    w.start()

results = []
working = []
not_working = []
ping_parser = pingparsing.PingParsing()

# Get the results as they arrive.
numTerminated = 0
while numTerminated < NUM_WORKERS:
    result = done.get()
    if result is None:
        # A worker is about to terminate.
        numTerminated += 1
    else:
        # Print as soon as results arrive
        if(result[1].decode("utf-8")==''): # Error is empty string
            if verbose:
                print("IP", result[0]['ip'])
                print(result[0]['result'].decode("utf-8") )
            ping_parser.parse(result[0]['result'].decode("utf-8"))
            if(int(ping_parser.packet_loss) == 100): # All packets are lost
                not_working.append(result[0]['ip'])
            else:
                working.append(result[0]['ip'])
        else:
            if verbose:
                print(result[1].decode("utf-8"))
        results.append(result)

# Wait for all the workers to terminate.
for w in workers:
    w.join()

# Print all the results at the end
"""
for result in results:
    if(result[0]!=''):
        print("IP", result[0]['ip'])
        print(result[0]['result'].decode("utf-8") )
    else:
        print(result[1].decode("utf-8"))
"""        
print("Working")
print(working)
print("\nNot Working")
print(not_working)