# -*- coding: utf-8 -*-
from wechat.xiaodou import xiaodou


class FriendPrintHandler(object):
    def match(self, msg):
        return True

    def handler(self, msg):
        print(self.wx.search_friends(userName=msg['FromUserName'])['NickName'] + ':' + msg['Text'] + '(' + msg[
            'FromUserName'] + ')')
        print()


class ChatroomPrintHandler(object):
    def match(self, msg):
        return True

    def handler(self, msg):
        print(self.wx.search_chatrooms(userName=msg['FromUserName'])['NickName'] + '(' + msg['FromUserName'] + ')')
        print('\t' + msg['ActualNickName'] + ':' + msg['Text'] + '(' + msg['ToUserName'] + ')')
        print()


class XiaoDouHandler(object):
    def match(self, msg):
        if msg['Text'].startswith('jjr'):
            return True
        else:
            return False

    def handler(self, msg):
        return xiaodou(msg['Text'][3:])
