import os
import json
from .settings import DATA_DIR
from .logger import logger


class MemecrawlerPipeline(object):
    @classmethod
    def process_item(cls, item, _):
        name = item['name']
        index = item['index']
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        filename = os.path.join(DATA_DIR, '{}_{}.txt'.format(index, name))
        with open(filename, 'w') as f:
            json.dump(dict(item), f, ensure_ascii=False,
                      separators=(',', ': '), indent=4)
        logger.info('Entry {} has been fetched.'.format(item['name']))
        return item
