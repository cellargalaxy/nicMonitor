# -*- coding: utf-8 -*-
import threading
from itchat import Core
from itchat.content import *

saveFilePath = '/home/cellargalaxy/'


class WxRobot(threading.Thread):
    def __init__(self, friendHandlers, chatroomHandlers):
        threading.Thread.__init__(self)
        self.wx = Core()
        self.friendHandlers = friendHandlers
        self.chatroomHandlers = chatroomHandlers

    def handler(self):
        @self.wx.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=False)
        def presonChatTextHandler(msg):
            for handler in self.friendHandlers:
                if handler.match(msg):
                    self.wx.send(handler.handler(msg), msg['FromUserName'])

        @self.wx.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
        def groupChatTextHandler(msg):
            for handler in self.chatroomHandlers:
                if handler.match(msg):
                    self.wx.send(handler.handler(msg), msg['FromUserName'])

        @self.wx.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False)
        def presonChatFileHandler(msg):
            msg['Text'](saveFilePath + msg['FileName'])

        @self.wx.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
        def groupChatFileHandler(msg):
            msg['Text'](saveFilePath + msg['FileName'])

    def run(self):
        self.handler()
        self.wx.auto_login(hotReload=True)
        self.wx.run(debug=False)

    def loginStatus(self):
        return self.wx.check_login(self)

    def alive(self):
        return self.wx.alive

    def logout(self):
        self.wx.logout()

    def sendFileToFriend(self, file, name):
        friends = self.wx.search_friends(name=name)
        if friends:
            self.wx.send_file(fileDir=file, toUserName=friends[0]['UserName'])
            return True
        else:
            return False

    def sendTextToFriend(self, info, name):
        friends = self.wx.search_friends(name=name)
        if friends:
            self.wx.send(msg=info, toUserName=friends[0]['UserName'])
            return True
        else:
            return False

    def sendFileToChatroom(self, file, name):
        chatrooms = self.wx.search_chatrooms(name=name)
        if chatrooms:
            self.wx.send_file(fileDir=file, toUserName=chatrooms[0]['UserName'])
            return True
        else:
            return False

    def sendTextToChatroom(self, info, name):
        chatrooms = self.wx.search_chatrooms(name=name)
        if chatrooms:
            self.wx.send(msg=info, toUserName=chatrooms[0]['UserName'])
            return True
        else:
            return False

    def get_head_img(self, userName=None, chatroomUserName=None, picDir=None):
        self.wx.get_head_img(userName, chatroomUserName, picDir)

    def search_friends(self, name=None, userName=None, remarkName=None, nickName=None, wechatAccount=None):
        return self.wx.search_friends(name, userName, remarkName, nickName, wechatAccount)

    def search_chatrooms(self, name=None, userName=None):
        return self.wx.search_chatrooms(name, userName)

    def search_mps(self, name=None, userName=None):
        return self.wx.search_mps(name, userName)

    def get_friends(self, update=False):
        return self.wx.get_friends(update)

    def get_chatrooms(self, update=False, contactOnly=False):
        return self.wx.get_chatrooms(update, contactOnly)

    def get_mps(self, update=False):
        return self.wx.get_mps(update)


if __name__ == '__main__':
    pass


# # 登录
# def auto_login(self, hotReload=False, statusStorageDir='itchat.pkl', enableCmdQR=False, picDir=None, qrCallback=None, loginCallback=None, exitCallback=None):
#
# # 返回登录状态的字符串 200:登录成功 201:等待登录确认 408:uuid超时 0:未知错误
# # 但是我实际使用无论登录前还是登录成功后他都只返回400，后来我用这个类的alive属性（返回True or False）代替了这个方法
# def check_login(self, uuid=None):
#
# # 退出登录
# def logout(self):
#
# # 启动机器人
# def run(self, debug=True, blockThread=True):
#
# # 获取朋友、群或者群里朋友的头像
# # 获取朋友只需要userName和picDir
# # 群则只需要chatroomUserName和picDir
# # 群里的朋友则需要全部参数
# def get_head_img(self, userName=None, chatroomUserName=None, picDir=None):
#
# # 发送信息
# def send_msg(self, msg='Test Message', toUserName=None):
#
# # 发送信息
# def send(self, msg, toUserName=None, mediaId=None):
#
# # 上传文件
# def upload_file(self, fileDir, isPicture=False, isVideo=False,toUserName='filehelper', file_=None, preparedFile=None):
#
# # 上传文件
# def send_file(self, fileDir, toUserName=None, mediaId=None, file_=None):
#
# # 上传图片
# def send_image(self, fileDir=None, toUserName=None, mediaId=None, file_=None):
#
# # 上传视频
# def send_video(self, fileDir=None, toUserName=None, mediaId=None, file_=None):
#
# # 查找朋友，返回一个匹配列表
# def search_friends(self, name=None, userName=None, remarkName=None, nickName=None,wechatAccount=None):
#     return self.storageClass.search_friends(name, userName, remarkName,nickName, wechatAccount)
#
# # 查找群，返回一个匹配列表
# def search_chatrooms(self, name=None, userName=None):
#     return self.storageClass.search_chatrooms(name, userName)
#
# # 查找公众号，返回一个匹配列表
# def search_mps(self, name=None, userName=None):
#     return self.storageClass.search_mps(name, userName)
#
# # 获取全部朋友，返会一个列表
# def get_friends(update)
#
# # 获取全部群，返会一个列表
# def get_chatrooms(update, contactOnly)
#
# # 获取全部公众号，返会一个列表
# def get_mps(update)
#
#
#
# # 群聊的msg
# msg['MemberCount'] : 群的人数
# msg['ToUserName'] : 接受者（自己）id
# msg['Text'] : 发送的信息
# msg['Type'] : 信息类型
# msg['Content'] : 发送的信息
# msg['ActualNickName'] : 发送信息的人的群昵称
# msg['ActualUserName'] : 发送信息的人的id
# msg['FromUserName'] : 群id
# {'MemberCount': 50, 'ToUserName': '@4a54b18c874f8d8158f5f03dda524f7e4348603ece9e0ec460cf',
# 'Text': '师弟们好', 'Type': 'Text', 'Content': '师弟们好',
#  'ActualNickName': '何部长',  'ActualUserName': '@6859d300155a8e70b570af3c5',  'FromUserName': '@@5e4f977c45d4d883dda1c9aba6aa1d282094fb3b6fdd8c759374d28be'}
#
# # 私聊msg
# msg['Text'] : 发送的信息
# msg['ToUserName'] : 接受者（自己）id
# msg['Type'] : 信息类型
# msg['FromUserName'] : 发送者id
# msg['Content'] : 发送的信息
# {'Text': '蛤蛤蛤',  '': '@4a54b18c874f8d8158f5f03dda524f7e4348603ece9e0ec460cf',
# 'Type': 'Text', 'FromUserName': '@6859d300155a8e70b570af3c5',  'Content': '蛤蛤蛤'}
