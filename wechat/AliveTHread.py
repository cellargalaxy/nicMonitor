# -*- coding: utf-8 -*-
import threading

import time


class AliveThread(threading.Thread):
    def __init__(self, wxRobot, heartbeatFriendNames, heartbeatSleepTime):
        threading.Thread.__init__(self)
        self.wxRobot = wxRobot
        self.heartbeatFriendNames = heartbeatFriendNames
        self.heartbeatSleepTime = heartbeatSleepTime
        self.runAble = True

    def stop(self):
        self.runAble = False

    def run(self):
        while self.runAble:
            for name in self.heartbeatFriendNames:
                self.wxRobot.sendTextToFriend(time.strftime("%m-%d %H:%M:%S", time.localtime()), name)
            time.sleep(self.heartbeatSleepTime)
