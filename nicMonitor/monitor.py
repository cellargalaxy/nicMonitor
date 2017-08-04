# -*- coding: utf-8 -*-
import threading

import time
from json import JSONEncoder

from wechat.handler import XiaoDouHandler
from wechat.robot import WxRobot

qunName = '测试'
qunName = '网络信息'

class Monitor(threading.Thread):
    def __init__(self, jsonString, sleepTime, friendHandlers, chatroomHandlers, checkTime):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        from nicMonitor.campus import Campus
        self.campus = Campus(jsonString, self, sleepTime)
        self.wxRobot = WxRobot(friendHandlers,chatroomHandlers)
        self.checkTime = checkTime
        self.runAble = True
        self.status = ''

    def run(self):
        self.wxRobot.start()
        self.campus.start()
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
        self.wxRobot.logout()
        self.campus.stop()
        print('退出监控和微信机器人')

    def statusFunc(self, host):
        self.lock.acquire()
        try:
            if host.status:
                self.status += time.strftime("%m-%d %H:%M:%S",
                                             time.localtime()) + ' 通 ' + host.area + '-' + host.floor + '-' + host.model + '-' + host.name + '\n'
            else:
                self.status += time.strftime("%m-%d %H:%M:%S",
                                             time.localtime()) + ' 挂 ' + host.area + '-' + host.floor + '-' + host.model + '-' + host.name + '\n'
            print(host.address, '状态转：', host.status)
        finally:
            self.lock.release()


if __name__ == '__main__':
    o = [
        {'address': '192.168.123.1', 'area': 'D1', 'floor': '319', 'model': 'abcd', 'name': '第1台'},
        {'address': '114.114.114.114', 'area': 'D1', 'floor': '319', 'model': 'abcd', 'name': '第2台'},
        {'address': 'baidu.com', 'area': 'D1', 'floor': '319', 'model': 'abcd', 'name': '第3台'},
        {'address': '192.168.123.4', 'area': 'D1', 'floor': '319', 'model': 'abcd', 'name': '第4台'}
    ]
    jsonString = JSONEncoder().encode(o)
    friendHandlers = []
    chatroomHandlers = [XiaoDouHandler()]

    monitor = Monitor(jsonString, 1, friendHandlers, chatroomHandlers, 10)
    monitor.start()
