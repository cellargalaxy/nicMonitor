# 交换机监控及微信机器人警报
在学校有对交换机是否存活监控，如果交换机挂了就警报的需求。以前我写过，但是我的python是三天入门，七天精通那种，所以写出来就只能达到需求就好。前两天有大佬（是itchat的作者？）在B站直播itchat接入微信和聊天机器人，所以手痒把交换机监控及接入微信机器人警报再写了一遍，记录一下。
.零、环境
系统环境：ubuntu16
Python环境：python3.5.2
Ide：pycharm
.一、交换机监控
交换机监控ping一下看通不通就好，这个我用java写过，java实现ping我当时是用Runtime.getRuntime().exec(commandText)来执行，即与系统有关，速度又慢，多线程一起ping消耗资源又多，并不是十分好。所以我就找到一个python原生实现ping功能的（[python3-ping](https://github.com/emamirazavi/python3-ping "Markdown")），我只需要得到延时，如果不通延时就为-1，所以我改了一下。
其余的交换机类，校区类的省略
.二、微信机器人
微信机器人是使用itchat（[ItChat](https://github.com/littlecodersh/ItChat "Markdown")），以前Python即水，对微信机器人有没有好好看过他的接口，基本上就是一个文件过，既没有类也没有什么结构。简单生搬硬凑能用就用。这次在B站看了大佬直播写代码，提起心肝第一次认认真真写个python的东西，这里要记录一下的是itchat的食用方法。
在itchat文件夹下面有一个core.py文件，里面有一个Core(object)类，这个类就是itchat的机器人类，这个类的对象可以调用他下面很多有用的api，其中我筛选了比较常用的方法：

Itchat通过回调的方法调用我们写好的方法，在这个方法里会传入一个叫msg的参数。这个参数直播时候没解释，在文档里我也没能找到他的结构，就只好打印一下，选了一下比较常用的：

有一点不懂，我print过msg的类型，是个类，为什么能够想字典一样通过[‘’]来引用，并且作者说是字典。
除此之外还接入了小豆机器人（[小豆机器人](http://xiao.douqq.com/ "Markdown")http://xiao.douqq.com/）用来娱乐一下。请求的信息需要用urllib.parse.quote()处理一下，不然中文会报错。
    def xiaodou(msg):
        data = urllib.request.urlopen(url=url+'?key='+key+'&msg='+urllib.parse.quote(msg)).read()
        return data.decode('utf-8')
最后我需要到Windows里部署，结果就gg了：
    SyntaxError: (unicode error) 'utf-8' codec can't decode byte 0xcd in position 0: invalid continuation byte
后来发现把'# -*- coding: utf-8 -*-'改为'# -*- coding: GBK -*-'就好了
