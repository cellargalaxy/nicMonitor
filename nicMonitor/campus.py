# -*- coding: utf-8 -*-

import threading
import time
from json import JSONDecoder, JSONEncoder

from nicMonitor.host import Host
from nicMonitor.monitor import Monitor
from nicMonitor.ping import ping


# ping parameters
TIME_OUT = 1000
PACKET_SIZE = 64


class Campus(threading.Thread):
    def __init__(self, jsonString, monitor, sleepTime, timeout=TIME_OUT, packet_size=PACKET_SIZE):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.changeHosts(jsonString, monitor)
        self.sleepTime = sleepTime
        self.timeout = timeout
        self.packet_size = packet_size
        self.runAble = True

    def ping(self):
        for host in self.hosts:
            delay = int(ping(host.address, self.timeout, self.packet_size))
            host.addDelay(delay)
            if not self.runAble:
                return

    def run(self):
        while self.runAble:
            self.lock.acquire()
            try:
                self.ping()
            finally:
                self.lock.release()
            time.sleep(self.sleepTime)

    def stop(self):
        self.runAble = False

    def changeHosts(self, jsonString, monitor):
        self.lock.acquire()
        try:
            array = JSONDecoder().decode(jsonString)
            self.hosts = []
            for mapHost in array:
                self.hosts.append(Host(mapHost, monitor))
        finally:
            self.lock.release()





if __name__ == '__main__':
    o = [
        {'address': '192.168.123.1', 'area': 'D1', 'floor': '319', 'model': 'abcd', 'name': '第1台'},
        {'address': '114.114.114.114', 'area': 'D1', 'floor': '319', 'model': 'abcd', 'name': '第2台'},
        {'address': 'baidu.com', 'area': 'D1', 'floor': '319', 'model': 'abcd', 'name': '第3台'},
        {'address': '192.168.123.4', 'area': 'D1', 'floor': '319', 'model': 'abcd', 'name': '第4台'}
    ]
    string = JSONEncoder().encode(o)
    monitor=Monitor()

    campus = Campus(string, monitor, 1)
    campus.start()
    time.sleep(10)
    campus.changeHosts(string, monitor)
    print('change')
    time.sleep(10)
    campus.stop()
    print('stop')
