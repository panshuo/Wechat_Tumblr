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
# @app.route('/', methods=['GET', 'POST'])
# def validation():
#     signature = request.args.get('signature')
#     timestamp = request.args.get('timestamp')
#     nonce = request.args.get('nonce')
#     echostr = request.args.get('echostr')
#     if wechat.check_signature(signature, timestamp, nonce):
#         print '验证成功'
#         return echostr
#     else:
#         print '服务器配置错误'


# 接受微信公众号服务器转发过来的信息并处理返回
@app.route('/', methods=['GET','POST'])
def home():
    wechat.parse_data(request.data)
    id = wechat.message.id  # 对应于 XML 中的 MsgId
    target = wechat.message.target  # 对应于 XML 中的 ToUserName
    source = wechat.message.source  # 对应于 XML 中的 FromUserName
    time = wechat.message.time  # 对应于 XML 中的 CreateTime
    type = wechat.message.type  # 对应于 XML 中的 MsgType
    raw = wechat.message.raw  # 原始 XML 文本，方便进行其他分析
    content = wechat.message.content
    response_message = wechat.response_text('是的，我爱特神', escape=False)
    print type
    access_token = wechat.get_access_token()
    return response_message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)