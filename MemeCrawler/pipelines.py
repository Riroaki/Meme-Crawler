import os
import json
from .settings import JIKI_DIR, BILIBILI_DIR
from .logger import logger
from .items import JikiItem, BilibiliItem


class MemecrawlerPipeline(object):
    """Save data into local files."""

    @classmethod
    def process_item(cls, item, _):
        # Register items with corresponding process methods
        handlers = {JikiItem: cls.process_jiki,
                    BilibiliItem: cls.process_bilibili}
        item_type = type(item)
        # Process items
        if item_type in handlers:
            handlers[item_type](item)
        return item

    @staticmethod
    def process_jiki(item: JikiItem) -> None:
        name = item['name']
        index = item['index']
        if not os.path.exists(JIKI_DIR):
            os.mkdir(JIKI_DIR)
        filename = os.path.join(JIKI_DIR, '{}_{}.txt'.format(index, name))
        with open(filename, 'w') as f:
            json.dump(dict(item), f, ensure_ascii=False,
                      separators=(',', ': '), indent=4)
        logger.info('Jiki entry {} has been fetched.'.format(name))

    @staticmethod
    def process_bilibili(item: BilibiliItem) -> None:
        name = item['name']
        if not os.path.exists(BILIBILI_DIR):
            os.mkdir(BILIBILI_DIR)
        filename = os.path.join(BILIBILI_DIR, '{}.txt'.format(name))
        with open(filename, 'w') as f:
            json.dump(dict(item), f, ensure_ascii=False,
                      separators=(',', ':'), indent=4)
        logger.info('Bilibili videos about {} has been fetched.'.format(name))
