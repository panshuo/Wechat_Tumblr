# _*_ coding: utf-8 _*_

from flask import request
from config import app, db, wechat, menu, site_filter
from models import User
from downloader import blog_video, post_video
from wechat_sdk.messages import TextMessage, VoiceMessage, LocationMessage
# from wechat_sdk.messages import ImageMessage, LinkMessage, VideoMessage, ShortVideoMessage


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
        return wechat.response_text(u'这好象是您第一次给本公众号发送消息，下面是菜单\n' + menu['MAIN_MENU'], escape=False)

    # 处理文本消息并返回
    if isinstance(wechat.message, TextMessage):
        content = wechat.message.content
        if user.status == 'home' and content == '2':
            # 处理文本消息并返回
            user.status = 'blog'
            db.session.add(user)
            return wechat.response_text(menu['MAIN2'], escape=False)
            # elif content == '3':
            #     pass
            # elif content == '4':
            #     pass
        if user.status == 'home' and content != '2':
            return wechat.response_text(u'请按照下面的菜单回复消息哦\n' + menu['MAIN_MENU'], escape=False)
        if user.status == 'blog':
            if site_filter(content):
                user.status = 'home'
                db.session.add(user)
                tmp = blog_video(content)
                if tmp:
                    return wechat.response_text(menu['SUB2'].format(content) + tmp, escape=False)
                else:
                    return wechat.response_text(menu['ERROR_NOT_FIND'], escape=False)
            else:
                return wechat.response_text(menu['ERROR_NAME'], escape=False)
    # 处理语音消息并返回
    if isinstance(wechat.message, VoiceMessage):
        # media_id = wechat.message.media_id  # 对应于 XML 中的 MediaId
        # format = wechat.message.format  # 对应于 XML 中的 Format
        recognition = wechat.message.recognition  # 对应于 XML 中的 Recognition
        response_message = wechat.response_text(u'您刚刚发的语音说的是 "{0}" 吗？\n{1}' \
                                                .format(recognition, menu['MAIN_MENU']), escape=False)
        return response_message

    # 处理定位消息并返回
    if isinstance(wechat.message, LocationMessage):
        location = wechat.message.location  # Tuple(X, Y)，对应于 XML 中的 (Location_X, Location_Y)
        # scale = wechat.message.scale  # 对应于 XML 中的 Scale
        label = wechat.message.label  # 对应于 XML 中的 Label
        user.location = label
        db.session.add(user)
        response_message = wechat.response_text(menu['LOCATION'].format(label,
                                                                        location[0],
                                                                        location[1],
                                                                        menu['MAIN_MENU']
                                                                        ), escape=False)
        return response_message


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
