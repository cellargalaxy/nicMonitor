# -*- coding: utf-8 -*-
import hashlib
import urllib.request

import time

xiaodouUrl='http://api.douqq.com/'
key='RWVDUkZsZEFoOVN0L2Z5Tj1SSkY9bzRuaEJJQUFBPT0'
nicUrl='http://192.168.123.1:8080/nic/wx/jsonHost?token='

def xiaodou(msg):
    data = urllib.request.urlopen(url=xiaodouUrl+'?key='+key+'&msg='+urllib.parse.quote(msg)).read()
    return data.decode('utf-8')

def jsonHost():
    md5 = hashlib.md5()
    md5.update(time.strftime("%Y-%m-%d %H", time.localtime()).encode('utf-8'))
    token=md5.hexdigest()
    data = urllib.request.urlopen(url=nicUrl +token).read()
    return data.decode('utf-8')

if __name__ == '__main__':
    print(jsonHost())