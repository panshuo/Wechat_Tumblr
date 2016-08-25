# _*_ coding: utf-8 _*_

from flask import render_template_string, url_for
import requests
import xmltodict
import re, os

# Numbers of photos/videos per page
MEDIA_NUM = 10


def blog_video(site):
    result = []
    base_url = "http://{0}.tumblr.com/api/read?type=video&num={1}&start=0"
    while True:
        media_url = base_url.format(site, MEDIA_NUM)
        response = requests.get(media_url, proxies={"http": "http://10.0.0.4:13000", "https": "https://10.0.0.4:13000"})
        if response.status_code == 200:
            data = xmltodict.parse(response.content)
            try:
                posts = data["tumblr"]["posts"]["post"]
                for post in posts:
                    url = handle_medium_url('video', post)
                    result.append(url)
                return render_template_string(u'{% for video in result %}\n{{ video }}\n{% endfor %}', result=result)
            except KeyError:
                break
        else:
            return None


def blog_photo(site):
    current_folder = os.getcwd()
    target_folder = os.path.join(current_folder, 'photos/' + site)
    result = []
    base_url = "http://{0}.tumblr.com/api/read?type=photo&num=5&start=0"
    while True:
        media_url = base_url.format(site)
        response = requests.get(media_url, proxies={"http": "http://10.0.0.4:13000", "https": "https://10.0.0.4:13000"})
        if response.status_code == 200:
            data = xmltodict.parse(response.content)
            try:
                posts = data["tumblr"]["posts"]["post"]
                for post in posts:
                    url = handle_medium_url("photo", post, site, target_folder)
                    result.append(url)
                return result
            except KeyError:
                break
        else:
            return None


def post_video():
    pass


def handle_medium_url(medium_type, post, site, target_folder=None):
    try:
        if medium_type == "photo":
            item = {}
            if not os.path.isdir(target_folder):
                os.mkdir(target_folder)
            r = requests.get(post["photo-url"][0]["#text"],
                             stream=True,
                             proxies={"http": "http://10.0.0.4:13000",
                                      "https": "https://10.0.0.4:13000"
                                      }
                             )
            local_filename = post["@id"] + "." + post["photo-url"][0]["#text"].split('.')[-1]
            absolute_path = "photos/" + site + "/" + local_filename
            with open(target_folder + "/" + local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                f.close()
            item['title'] = post["photo-caption"]
            item['picurl'] = "http://tetewechat.ngrok.cc/" + absolute_path
            item['description'] = post["@date"]
            item['url'] = post["@url"]
            return item

        if medium_type == "video":
            video_player = post["video-player"][1]["#text"]
            pattern = re.compile(r'[\S\s]*src="(\S*)" ')
            match = pattern.match(video_player)
            if match is not None:
                try:
                    return match.group(1)
                except IndexError:
                    return None
    except:
        raise TypeError("Unable to find the right url for downloading. "
                        "Please open a new issue on "
                        "https://github.com/dixudx/tumblr-crawler/"
                        "issues/new attached with below information:\n\n"
                        "%s" % post)
