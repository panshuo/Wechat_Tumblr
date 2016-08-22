# _*_ coding: utf-8 _*_

from flask import Flask, request
from wechat_sdk import WechatBasic as Basic, WechatConf as Conf

app = Flask(__name__)
conf = Conf(
    token='tetetetest',
    appid='wx1766a3244906ed6e',
    appsecret='92c5bd5f5c759f53e0798c9bfc140c73',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='uf2xUCwvr3lIsi2VPok9GO6cd9jb1lwwP2XSpW4vtPZ'  # 如果传入此值则必须保证同时传入 token, appid
)
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
