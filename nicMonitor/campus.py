# -*- coding: utf-8 -*-

import threading
import time
from json import JSONDecoder

from nicMonitor.host import Host
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
