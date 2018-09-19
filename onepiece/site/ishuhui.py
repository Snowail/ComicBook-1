import re
import random
import json
import warnings

import requests

from . import Chapter


class ComicBook():

    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/65.0.3325.146 Safari/537.36')
    }
    TIMEOUT = 30

    def __init__(self):
        self.session = requests.session()
        self.name = '鼠绘漫画'

    def send_request(self, url, **kwargs):
        kwargs.setdefault('headers', self.HEADERS)
        kwargs.setdefault('timeout', self.TIMEOUT)
        return self.session.get(url, **kwargs)

    def get_html(self, url):
        response = self.send_request(url)
        return response.text

    def get_chapter_pics(self, _id):
        """根据章节的URL获取该章节的图片列表
        :param str _id: 章节的URL如 http://hanhuazu.cc/cartoon/post?id=10694，id为10694
        :yield pic_url:
        """
        url = 'http://hanhuazu.cc/cartoon/post?id={_id}'.format(_id=_id)
        html = self.get_html(url)
        cdn_str = re.search(r'<meta name=img-url content="(.*?)"', html).group(1).replace('&#34;', '"')
        cdn_info = json.loads(cdn_str)
        cdn_url = random.choice(cdn_info)

        ver_str = re.search(r'<meta name=ver content="(.*?)">', html).group(1).replace('&#34;', '"')
        ver_info = json.loads(ver_str)
        ver = random.choice(list(ver_info.values()))

        url = 'http://hhzapi.ishuhui.com/cartoon/post/ver/{ver}/id/{_id}.json'.format(ver=ver, _id=_id)
        response = self.send_request(url)
        data = response.json()
        img_data = json.loads(data['data']['content_img'])
        for url in img_data.values():
            pic_url = 'http:{}{}'.format(cdn_url, url.replace('upload/', ''))
            yield pic_url

    def get_all_chapter(self, comicid=None, name=None):
        """根据漫画id获取所有的章节列表: http://ac.qq.com/Comic/ComicInfo/id/505430
        :param str/int comicid: 漫画id 如 505430
        :return (comic_title, all_chapter): 漫画标题和所有章节信息
        """
        if not comicid:
            comicid = self.search(name)
        url = 'http://www.ishuhui.com/cartoon/book/{}'.format(comicid)
        html = self.get_html(url)
        r = re.search(r'<meta name=ver content="(.*?)">', html)
        ver = json.loads(r.group(1).replace('&#34;', '"'))

        url = 'http://api.ishuhui.com/cartoon/book_ish/ver/{ver}/id/{comicid}.json'\
            .format(ver=random.choice(list(ver.values())), comicid=comicid)
        response = self.send_request(url)
        data = response.json()
        comic_title = data['data']['book']['name']
        all_chapter = {}
        for key, value in data['data']['cartoon']['0']['posts'].items():
            r1 = re.search(r'^c-(\d+)', key)
            r2 = re.search(r'^n-(\d+)$', key)
            chapter_number = None
            if r1:
                chapter_number = int(r1.group(1))
            elif r2:
                chapter_number = int(r2.group(1))
            all_chapter[chapter_number] = value
        return comic_title, all_chapter

    def get_task_chapter(self, comicid=None, name=None, chapter_number_list=None, is_download_all=None):
        """根据参数来确定下载哪些章节
        :param str/int comicid: 漫画id
        :param str name: 漫画名
        :param list chapter_number_list: 需要下载的章节列表，如 chapter_number_list = [1, 2, 3]
        :param is_download_all: 若设置成True，则下载该漫画的所有章节
        :yield chapter: Chapter instance
        """
        comic_title, all_chapter = self.get_all_chapter(comicid, name)
        max_chapter_number = max(all_chapter.keys())
        if is_download_all:
            chapter_number_list = list(all_chapter.keys())
        for idx in chapter_number_list:
            chapter_number = idx if idx >= 0 else max_chapter_number + idx + 1
            value = all_chapter.get(chapter_number)

            if value is None:
                warnings.warn('找不到第{}集资源'.format(chapter_number))
                continue

            if all([src['source'] not in [1, 5] for src in value]):
                warnings.warn('暂不支持的资源类型：{} 第{}集'.format(comic_title, chapter_number))

            for src in value:
                if src['source'] in [1, 5]:
                    chapter_title = src['title']
                    chapter = Chapter(chapter_number=chapter_number,
                                      chapter_title=chapter_title,
                                      comic_title=comic_title,
                                      chapter_pics=self.get_chapter_pics(src['id']),
                                      site_name=self.name
                                      )
                    yield chapter
                    break

    def search(self, name):
        pass
