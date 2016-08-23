# _*_ coding: utf-8 _*_

from flask import request
from models import User
from config import app, db, wechat
from downloader import blog_video, post_video
from wechat_sdk.messages import TextMessage, VoiceMessage, LocationMessage
# from wechat_sdk.messages import ImageMessage, LinkMessage, VideoMessage, ShortVideoMessage

MAIN_MENU = u'\n回复1 下载单个视频(未开放)\n回复2 下载整个博客视频\n回复3 下载整个博客图片(未开放)\n回复4 使用帮助'


# 接受微信公众号服务器转发过来的信息并处理返回
@app.route('/', methods=['GET', 'POST'])
def home():
    wechat.parse_data(request.data)
    source = wechat.message.source  # 对应于 XML 中的 FromUserName

    # id = wechat.message.id  # 对应于 XML 中的 MsgId
    # target = wechat.message.target  # 对应于 XML 中的 ToUserName
    # time = wechat.message.time  # 对应于 XML 中的 CreateTime
    # type = wechat.message.type  # 对应于 XML 中的 MsgType
    # raw = wechat.message.raw  # 原始 XML 文本，方便进行其他分析
    # access_token = wechat.get_access_token()

    user = User.query.filter_by(username=source).first()
    if not user:
        # message = Message(type=type, raw=raw)
        user = User(username=source)
        db.session.add(user)
        return wechat.response_text(u'这好象是您第一次给本公众号发送消息，下面是菜单\n' + MAIN_MENU, escape=False)

    # 处理文本消息并返回
    if isinstance(wechat.message, TextMessage):
        content = wechat.message.content
        if user.status == 'home' and content == '2':
            # 处理文本消息并返回
                    user.status = 'blog'
                    db.session.add(user)
                    return wechat.response_text(u'请回复您需要下载的blog的名字，不要用人家下载那些羞羞的东西哦', escape=False)
                # elif content == '3':
                #     pass
                # elif content == '4':
                #     pass
        if user.status == 'home' and content != '2':
            return wechat.response_text(u'抱歉，功能暂未开通\n' + MAIN_MENU, escape=False)
        if user.status == 'blog':
            user.status = 'home'
            db.session.add(user)
            tmp = blog_video(content)
            return wechat.response_text(u'下面是您回复的博客：\n“{}” 最新发布的十条视频的下载地址，直接打开可能会被微信阻止，您可以复制到safari和其它浏览器打开,也可复制到手机迅雷或者其它下载工具下载。\n'.format(content) + tmp, escape=False)

    # 处理语音消息并返回
    if isinstance(wechat.message, VoiceMessage):
        # media_id = wechat.message.media_id  # 对应于 XML 中的 MediaId
        # format = wechat.message.format  # 对应于 XML 中的 Format
        recognition = wechat.message.recognition  # 对应于 XML 中的 Recognition
        response_message = wechat.response_text(u'您刚刚发的语音说的是 "{0}" 吗？\n{1}' \
                                                .format(recognition, MAIN_MENU), escape=False)
        return response_message

    # 处理定位消息并返回
    if isinstance(wechat.message, LocationMessage):
        location = wechat.message.location  # Tuple(X, Y)，对应于 XML 中的 (Location_X, Location_Y)
        # scale = wechat.message.scale  # 对应于 XML 中的 Scale
        label = wechat.message.label  # 对应于 XML 中的 Label
        response_message = wechat.response_text(u'您的位置好像在:\n{0}\n纬度 {1}\n经度 {2}\n{3}' \
                                                .format(label, location[0], location[1], MAIN_MENU), escape=False)
        return response_message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
