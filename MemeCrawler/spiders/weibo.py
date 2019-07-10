import os
import re
import pickle
import scrapy
import random
from urllib.parse import quote
from ..settings import WEIBO_INDEX_FILE, JIKI_INDEX_FILE
from ..logger import logger
from ..items import WeiboItem, WeiboSingleItem


class WeiboSpider(scrapy.Spider):
    name = 'weibo'

    # Saved data
    saved_dict = {}
    todo_list = []

    # Url format of weibo search
    enytry_url = 'https://s.weibo.com/weibo?q={key}&Refer=index'

    # Patterns
    pat_dict = {
        'mid': 'mid=(.*?)&',
        'user': 'user_name">(.*?)<',
        'avator': 'user_pic"><img src="(.*?)"',
        'time': 'click:wb_time">([\s\S]*?)<',
        'like': '<em>([0-9]*)<',
        'repost': 'click:repost.*?>.*?([0-9]*)<',
        'comment': 'click:comment.*?>.*?([0-9]*)<',
        'source': 'rel="nofollow">(.*?)<'
    }

    # Default values
    default_dict = {
        'mid': '',
        'user': '',
        'avator': '',
        'time': '0000-00-00',
        'like': '0',
        'repost': '0',
        'comment': '0',
        'source': '微博 weibo.com'
    }

    # Handle bad http status
    handle_httpstatus_list = [404, 500]

    def start_requests(self) -> scrapy.Request:
        # Init saved index and next index sequence
        self.init_index()
        # Iterates all key words
        for keyword in self.todo_list:
            yield scrapy.Request(self.enytry_url.format(key=quote(keyword)),
                                 callback=self.parse, meta={'key': keyword})
        logger.info('All weibo data has been collected.')

    def parse(self, response: scrapy.http.response) -> scrapy.Item:
        keyword = response.meta['key']
        status = response.status
        # Check if ip has been banned
        # Check if is valid status
        if status == 200:
            text = response.text
            item = WeiboItem()
            item['name'] = keyword
            item['weibo_list'] = self.get_weibo_list(text)
            yield item
            self.saved_dict[keyword] = 'ok'
        elif status == 404:
            self.saved_dict[keyword] = 'error'
        else:  # status == 500
            self.crawler.engine.close_spider(self, 'Connection failed.')

    def init_index(self) -> None:
        saved = {}
        if os.path.exists(WEIBO_INDEX_FILE):
            with open(WEIBO_INDEX_FILE, 'rb') as f:
                saved = pickle.load(f)
        self.saved_dict = saved
        all_dict = {}
        if os.path.exists(JIKI_INDEX_FILE):
            with open(JIKI_INDEX_FILE, 'rb') as f:
                all_dict = pickle.load(f)
        # Generate to-do list
        todo = []
        for k in all_dict.values():
            if k != 'error' and k not in saved:
                todo.append(k)
        # Randomly start to aviod stuck
        random.shuffle(todo)
        self.todo_list = todo

    def get_weibo_list(self, raw: str) -> list:
        # Extract weibo information
        start = '<!--card-wrap-->'
        end = '<!--/card-wrap-->'
        item_list = []
        while start in raw:
            raw = raw[raw.find(start) + len(start):]
            piece = raw[:raw.find(end)]
            raw = raw[raw.find(end) + len(end):]
            item = WeiboSingleItem()
            for attr, pat in self.pat_dict.items():
                try:
                    item[attr] = re.search(pat, piece).group(1)
                except AttributeError:
                    item[attr] = self.default_dict[attr]
            item['content'] = self.get_weibo_content(piece)
            item_list.append(item)
        return item_list

    @staticmethod
    def get_weibo_content(piece: str) -> str:
        # Extract contents of weibo
        pat = '<!--微博内容-->([\s\S]*?)<!--\/微博内容'
        try:
            content = re.search(pat, piece).group(1).strip()
            content = re.sub('<.*?>', '', content)
        except AttributeError:
            content = ''
        return content

    def close(self, spider, reason):
        logger.info(reason)
        with open(WEIBO_INDEX_FILE, 'wb') as f:
            pickle.dump(self.saved_dict, f)
