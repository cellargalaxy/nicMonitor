# -*- coding: utf-8 -*-
import threading

import time

from wechat.AliveTHread import AliveThread
from wechat.handler import XiaoDouHandler, TestAliveHandler
from wechat.robot import WxRobot
from wechat.xiaodou import jsonHost

qunName = '网管'


class Monitor(threading.Thread):
    def __init__(self, jsonString, sleepTime, friendHandlers, chatroomHandlers, checkTime, heartbeatFriendNames,
                 heartbeatSleepTime):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        from nicMonitor.campus import Campus
        self.campus = Campus(jsonString, self, sleepTime)
        self.wxRobot = WxRobot(friendHandlers, chatroomHandlers)
        self.aliveThread = AliveThread(self.wxRobot, heartbeatFriendNames, heartbeatSleepTime)
        self.checkTime = checkTime
        self.runAble = True
        self.status = ''

    def run(self):
        self.wxRobot.start()
        self.campus.start()
        self.aliveThread.start()
        time.sleep(60)
        while self.runAble:
            time.sleep(self.checkTime)
            if not self.wxRobot.alive():
                self.stop()
                return
            if self.status:
                self.lock.acquire()
                try:
                    if self.wxRobot.sendTextToChatroom(self.status, qunName):
                        self.status = ''
                    else:
                        print('找不到群:' + qunName)
                finally:
                    self.lock.release()

    def stop(self):
        self.runAble = False
        self.aliveThread.stop()
        self.wxRobot.logout()
        self.campus.stop()
        print('退出监控和微信机器人')

    def statusFunc(self, host):
        self.lock.acquire()
        try:
            if host.status:
                self.status += time.strftime("%m-%d %H:%M:%S",
                                             time.localtime()) + ' 通 ' + host.building + '-' + host.floor + '-' + host.model + '-' + host.name + '\n'
            else:
                self.status += time.strftime("%m-%d %H:%M:%S",
                                             time.localtime()) + ' 挂 ' + host.building + '-' + host.floor + '-' + host.model + '-' + host.name + '\n'
            print(host.address, '状态转：', host.status)
        finally:
            self.lock.release()


if __name__ == '__main__':
    friendHandlers = [TestAliveHandler()]
    chatroomHandlers = [XiaoDouHandler()]
    heartbeatFriendNames = ['孵化种子']

    monitor = Monitor(jsonHost(), 1, friendHandlers, chatroomHandlers, 10, heartbeatFriendNames, 60 * 30)
    monitor.start()
