# _*_ coding: utf-8 _*_

from flask import Flask, request, render_template_string
from wechat_sdk import WechatBasic as Basic, WechatConf as Conf
from wechat_sdk.messages import TextMessage, VoiceMessage, LocationMessage
# from tumblr import CrawlerScheduler
# from wechat_sdk.messages import ImageMessage, LinkMessage, VideoMessage, ShortVideoMessage
# from flask.ext.sqlalchemy import SQLAlchemy
import requests
import xmltodict
import re

app = Flask(__name__)
conf = Conf(
    token='tetetetest',
    appid='wx1766a3244906ed6e',
    appsecret='92c5bd5f5c759f53e0798c9bfc140c73',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='uf2xUCwvr3lIsi2VPok9GO6cd9jb1lwwP2XSpW4vtPZ'  # 如果传入此值则必须保证同时传入 token, appid
)
wechat = Basic(conf=conf)

MAIN_MENU = u'回复1 下载单个视频(未开放)\n回复2 下载整个博客视频\n回复3 下载整个博客图片(未开放)\n回复4 使用帮助'

# Numbers of photos/videos per page
MEDIA_NUM = 10


def blog_video(site):
    result = []
    base_url = "http://{0}.tumblr.com/api/read?type=video&num={1}&start=0"
    while True:
        media_url = base_url.format(site, MEDIA_NUM)
        response = requests.get(media_url, proxies={"http": "http://10.0.0.4:13000","https": "https://10.0.0.4:13000"})
        data = xmltodict.parse(response.content)
        try:
            posts = data["tumblr"]["posts"]["post"]
            for post in posts:
                video_url = handle_medium_url(post)
                print video_url
                result.append(video_url)
            # length = len(result)
            return render_template_string(u'{% for video in result %}\n{{ video }}\n{% endfor %}', result=result)
        except KeyError:
            break

def handle_medium_url(post):
    video_player = post["video-player"][1]["#text"]
    pattern = re.compile(r'[\S\s]*src="(\S*)" ')
    match = pattern.match(video_player)
    if match is not None:
        try:
            return match.group(1)
        except IndexError:
            return None


# 接受微信公众号服务器转发过来的信息并处理返回
@app.route('/', methods=['GET', 'POST'])
def home():
    wechat.parse_data(request.data)
    # id = wechat.message.id  # 对应于 XML 中的 MsgId
    # target = wechat.message.target  # 对应于 XML 中的 ToUserName
    # source = wechat.message.source  # 对应于 XML 中的 FromUserName
    # time = wechat.message.time  # 对应于 XML 中的 CreateTime
    # type = wechat.message.type  # 对应于 XML 中的 MsgType
    # raw = wechat.message.raw  # 原始 XML 文本，方便进行其他分析
    # access_token = wechat.get_access_token()

    # 处理文本消息并返回
    if isinstance(wechat.message, TextMessage):
        content = wechat.message.content
        if content == '1':
            pass
        elif content == '2':
            return wechat.response_text(u'请回复您需要下载的blog的名字，不要用人家下载那些羞羞的东西哦', escape=False)
        elif content == '3':
            pass
        elif content == '4':
            pass
        else:
            tmp = blog_video(content)
            return wechat.response_text(u'下面是您回复的博客：\n“{}” 最新发布的十条视频的下载地址，直接打开可能会被微信阻止，您可以复制到safari和其它浏览器打开,也可复制到手机迅雷或者其它下载工具下载。'.format(content) + tmp, escape=False)

    # 处理语音消息并返回
    if isinstance(wechat.message, VoiceMessage):
        # media_id = wechat.message.media_id  # 对应于 XML 中的 MediaId
        # format = wechat.message.format  # 对应于 XML 中的 Format
        recognition = wechat.message.recognition  # 对应于 XML 中的 Recognition
        response_message = wechat.response_text(u'您刚刚发的语音说的是 "{0}" 吗？\n\n{1}' \
                                                .format(recognition, MAIN_MENU), escape=False)
        return response_message

    # 处理定位消息并返回
    if isinstance(wechat.message, LocationMessage):
        location = wechat.message.location  # Tuple(X, Y)，对应于 XML 中的 (Location_X, Location_Y)
        # scale = wechat.message.scale  # 对应于 XML 中的 Scale
        label = wechat.message.label  # 对应于 XML 中的 Label
        response_message = wechat.response_text(u'您的位置好像在:\n{0}\n纬度 {1}\n经度 {2}\n\n{3}' \
                                                .format(label, location[0], location[1], MAIN_MENU), escape=False)
        return response_message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
