#!/usr/bin/env python
"""
Produces load on all available CPU cores

Updated with suggestion to prevent Zombie processes
Linted for Python 3
Source: 
insaner @ https://danielflannery.ie/simulate-cpu-load-with-python/#comment-34130
"""
from multiprocessing import Pool
from multiprocessing import cpu_count
import time
import signal
from flask import request

stop_loop = 0

from flask import Flask

app = Flask(__name__)

@app.route('/')
def status():
    return 'OK!'

@app.route('/cpuload')
def cpuload():
    duration = int(request.args.get('duration')) or 10
    load_cpu(duration)

    return 'CPU load generated for ' + str(duration) + ' seconds'



def exit_chld(x, y):
    global stop_loop
    stop_loop = 1


def f(x):
    global stop_loop
    while not stop_loop:
        x*x

def load_cpu(duration):
    processes = cpu_count()
    print('-' * 20)
    print('Running load on CPU(s) for %d seconds' % duration)
    print('Utilizing %d cores' % processes)
    print('-' * 20)
    pool = Pool(processes)
    pool.map_async(f, range(processes))
    time.sleep(duration)
    pool.terminate()
    pool.join()

    return 1

signal.signal(signal.SIGINT, exit_chld)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)