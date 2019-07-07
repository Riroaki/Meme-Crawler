import os
import pickle
from .settings import DATA_DIR


class MemecrawlerPipeline(object):
    @classmethod
    def process_item(cls, item, _):
        name = item['name']
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        filename = os.path.join(DATA_DIR, name)
        with open(filename, 'wb') as f:
            pickle.dump(dict(item), f)
        return item
