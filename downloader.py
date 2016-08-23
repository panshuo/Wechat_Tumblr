# _*_ coding: utf-8 _*_

from flask import render_template_string
import requests
import xmltodict
import re

# Numbers of photos/videos per page
MEDIA_NUM = 10


def blog_video(site):
    result = []
    base_url = "http://{0}.tumblr.com/api/read?type=video&num={1}&start=0"
    while True:
        media_url = base_url.format(site, MEDIA_NUM)
        response = requests.get(media_url, proxies={"http": "http://10.0.0.4:13000", "https": "https://10.0.0.4:13000"})
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


def post_video():
    pass
