# -*- coding: utf-8 -*-
import urllib.request

url='http://api.douqq.com/'
key='RWVDUkZsZEFoOVN0L2Z5Tj1SSkY9bzRuaEJJQUFBPT0'

def xiaodou(msg):
    data = urllib.request.urlopen(url=url+'?key='+key+'&msg='+urllib.parse.quote(msg)).read()
    return data.decode('utf-8')
