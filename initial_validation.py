# _*_ coding: utf-8 _*_

from flask import Flask, request
from config import wechat_config
from wechat_sdk import WechatBasic as Basic, WechatConf as Conf

app = Flask(__name__)
conf = Conf(wechat_config)
wechat = Basic(conf=conf)


# 用于服务器配置初始验证
@app.route('/', methods=['GET'])
def validation():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    if wechat.check_signature(signature, timestamp, nonce):
        print '验证成功'
        return echostr
    else:
        print '服务器配置错误'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
