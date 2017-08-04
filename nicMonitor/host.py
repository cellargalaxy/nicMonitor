# -*- coding: utf-8 -*-

DELATS_LEN = 5


class Host(object):
    '''
    交换机类
    '''

    def __init__(self, address, area, floor, model, monitor, name=None, delaysLen=DELATS_LEN):
        self.address = address
        self.area = area
        self.floor = floor
        self.model = model
        self.name = name
        self.monitor = monitor
        self.delaysLen = delaysLen
        self.delays = []
        self.status = True

    def __init__(self, hostMap, monitor, delaysLen=DELATS_LEN):
        self.address = hostMap['address']
        self.area = hostMap['area']
        self.floor = hostMap['floor']
        self.model = hostMap['model']
        self.name = hostMap['name']
        self.monitor = monitor
        self.delaysLen = delaysLen
        self.delays = []
        self.status = True

    def addDelay(self, delay):
        delays = self.delays
        if delays.__len__() >= self.delaysLen:
            delays.pop()
        delays.append(delay)

        if self.status:
            for d in delays:
                if d >= 0:
                    return
            self.status = False
            self.monitor.statusFunc(self)
        else:
            if delay >= 0:
                self.status = True
                self.monitor.statusFunc(self)

    def print(self):
        print('address:%s area:%s floor:%s model:%s name:%s' % (
            self.address, self.area, self.floor, self.model, self.name))
