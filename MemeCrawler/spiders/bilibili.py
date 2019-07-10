import os
import re
import pickle
import scrapy
import random
from urllib.parse import quote
from ..settings import BILIBILI_INDEX_FILE, JIKI_INDEX_FILE
from ..logger import logger
from ..items import BilibiliItem


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'

    # Saved data
    saved_dict = {}
    todo_list = []

    # Url format of Bilibili search
    enytry_url = 'https://search.bilibili.com/all?keyword={key}'

    # Handle bad http status
    handle_httpstatus_list = [404, 500]

    def start_requests(self) -> scrapy.Request:
        # Init saved index and next index sequence
        self.init_index()
        # Iterates all key words
        for keyword in self.todo_list:
            yield scrapy.Request(self.enytry_url.format(key=quote(keyword)),
                                 callback=self.parse, meta={'key': keyword})

    def parse(self, response: scrapy.http.response) -> scrapy.Item:
        keyword = response.meta['key']
        status = response.status
        # Check if ip has been banned
        # Check if is valid status
        if status == 200:
            text = response.text
            item = BilibiliItem()
            item['name'] = keyword
            item['video_list'] = self.get_video_list(text)
            yield item
            self.saved_dict[keyword] = 'ok'
        elif status == 404:
            self.saved_dict[keyword] = 'error'
        else:  # status == 500
            self.crawler.engine.close_spider(self, 'Connection failed.')

    def init_index(self) -> None:
        saved = {}
        if os.path.exists(BILIBILI_INDEX_FILE):
            with open(BILIBILI_INDEX_FILE, 'rb') as f:
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

    @staticmethod
    def get_video_list(raw: str) -> list:
        # Extract video ids
        pat = 'a href="//www.bilibili.com/video/av(.*?)\?'
        video_list = []
        for video_id in re.findall(pat, raw):
            video_list.append(video_id)
        return video_list

    def close(self, spider, reason):
        logger.info(reason)
        with open(BILIBILI_INDEX_FILE, 'wb') as f:
            pickle.dump(self.saved_dict, f)
