# -*- coding: utf-8 -*-
from nicMonitor.monitor import Monitor
from wechat.handler import TestAliveHandler, XiaoDouHandler
from wechat.xiaodou import jsonHost

if __name__ == '__main__':
    friendHandlers = [TestAliveHandler()]
    chatroomHandlers = [XiaoDouHandler()]
    heartbeatFriendNames = ['孵化种子']

    monitor = Monitor(jsonHost(), 1, friendHandlers, chatroomHandlers, 10, heartbeatFriendNames, 60 * 30)
    monitor.start()