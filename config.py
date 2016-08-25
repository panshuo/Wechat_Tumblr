# _*_ coding: utf-8 _*_

from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from wechat_sdk import WechatBasic as Basic, WechatConf as Conf

menu = {'NEW': u'这好象是您第一次给本公众号发送消息，下面是菜单\n',
        'INDEX': u'\n回复1 下载单个视频(未开放)\n回复2 下载整个博客视频\n回复3 下载整个博客图片(未开放)\n回复4 使用帮助',
        'MAIN1': u'请回复您需要下载的Post的名字\n例如： http://taylorswift.tumblr.com/post/142356007592/the-best-people-in-life-are-free-newromantics\n只需要回复中间的这串数字 "142356007592" (不含引号) 就可以了',
        'MAIN2': u'请回复您需要下载的Blog的名字\n例如： http://taylorswift.tumblr.com\n只需要回复最前面的 "taylorswift" (不含引号) 就可以了',
        'MAIN3': '',
        'MAIN4': '',
        'SUB2': u'下面是您回复的博客： “{}” 最新发布的十条视频的下载地址，直接打开可能会被微信阻止 您可以复制到safari和其它浏览器打开 也可复制到手机迅雷或者其它下载工具下载。',
        'SUB3': u'下面是您回复的博客： “{}” 最新发布的十张图片的下载地址，直接打开可能会被微信阻止 您可以复制到safari和其它浏览器打开 也可复制到手机迅雷或者其它下载工具下载。',
        'LOCATION': u'您的位置好像在:\n{0}\n纬度 {1}\n经度 {2}\n{3}',
        'ERROR_NAME': u'您回复的blog的名字好像不对\n应该只包含大小写字母数字和横杠',
        'ERROR_NOT_FOUND': u'您回复的blog没有找到'
        }

wechat_config = {'token': 'tetetetest',
                 'appid': 'wx1766a3244906ed6e',
                 'appsecret': '92c5bd5f5c759f53e0798c9bfc140c73',
                 'encrypt_mode': 'normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
                 # 如果传入 encoding_aes_key 值则必须保证同时传入 token, appid
                 'encoding_aes_key': 'uf2xUCwvr3lIsi2VPok9GO6cd9jb1lwwP2XSpW4vtPZ'
                 }


def site_filter(seq):
    charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-'
    for c in seq:
         if c in charset:
                return True
    return False


class Config:
    def __init__(self):
        pass
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data-dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '$%^NB4%^#_+UHha'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# 实例化 Flask, SQLAlchemy, Wechat-SDK 基础对象并传入配置
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
conf = Conf(wechat_config)
wechat = Basic(conf=conf)
