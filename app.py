# _*_ coding: utf-8 _*_

from flask import request
from config import app, db, wechat, menu, site_filter
from models import User
from downloader import blog_video, blog_photo, post_video
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
        return wechat.response_text(menu['NEW'] + menu['INDEX'], escape=False)

    # 处理文本消息并返回
    if isinstance(wechat.message, TextMessage):
        content = wechat.message.content

        # 处理主菜单回复文本
        if user.status == 'home' and content == '1':
            user.status = 'post'
            db.session.add(user)
            return wechat.response_text(menu['MAIN1'], escape=False)

        if user.status == 'home' and content == '2':
            user.status = 'video'
            db.session.add(user)
            return wechat.response_text(menu['MAIN2'], escape=False)

        if user.status == 'home' and content == '3':
            user.status = 'photo'
            db.session.add(user)
            return wechat.response_text(menu['MAIN2'], escape=False)

        if user.status == 'home' and content == '4':
            pass

        if user.status == 'home' and content not in ['1', '2', '3', '4']:
            return wechat.response_text(u'请按照下面的菜单回复消息哦' + menu['INDEX'], escape=False)

        # 处理子菜单 '1'
        if user.status == 'post':
            user.status = 'home'
            db.session.add(user)
            tmp = blog_photo(content)
            if tmp:
                return wechat.response_text(menu['SUB2'].format(content) + tmp, escape=False)
            else:
                return wechat.response_text(menu['ERROR_NOT_FOUND'], escape=False)

        # 处理子菜单 '2'
        if user.status == 'video':
            if site_filter(content):
                user.status = 'home'
                db.session.add(user)
                tmp = blog_video(content)
                if tmp:
                    return wechat.response_text(menu['SUB2'].format(content) + tmp, escape=False)
                else:
                    return wechat.response_text(menu['ERROR_NOT_FOUND'], escape=False)
            else:
                return wechat.response_text(menu['ERROR_NAME'], escape=False)

        # 处理子菜单 '3'
        if user.status == 'photo':
            if site_filter(content):
                user.status = 'home'
                db.session.add(user)
                tmp = blog_photo(content)
                if tmp:
                    return wechat.response_news(tmp)
                else:
                    return wechat.response_text(menu['ERROR_NOT_FOUND'], escape=False)
            else:
                return wechat.response_text(menu['ERROR_NAME'], escape=False)


    # 处理语音消息并返回
    if isinstance(wechat.message, VoiceMessage):
        # media_id = wechat.message.media_id  # 对应于 XML 中的 MediaId
        # format = wechat.message.format  # 对应于 XML 中的 Format
        recognition = wechat.message.recognition  # 对应于 XML 中的 Recognition
        response_message = wechat.response_text(u'您刚刚发的语音说的是 "{0}" 吗？\n{1}' \
                                                .format(recognition, menu['INDEX']), escape=False)
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
                                                                        menu['INDEX']
                                                                        ), escape=False)
        return response_message


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
