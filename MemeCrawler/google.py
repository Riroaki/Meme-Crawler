import os
import pickle
import random
from settings import GOOGLE_IMAGE_DIR, GOOGLE_IMAGE_INDEX_FILE, JIKI_INDEX_FILE
from logger import logger


class GoogleSpider(object):
    name = 'google'

    def __init__(self):
        saved = {}
        if os.path.exists(GOOGLE_IMAGE_INDEX_FILE):
            with open(GOOGLE_IMAGE_INDEX_FILE, 'rb') as f:
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
        # Max limit of videos for one keyword
        self.limit = 20

    def run(self) -> None:
        cmd_raw = ('googleimagesdownload'
                   ' -o "{path}" -l {limit}'.format(path=GOOGLE_IMAGE_DIR,
                                                    limit=self.limit))
        try:
            for keyword in self.todo_list:
                cmd = ' '.join([cmd_raw, '-k', keyword])
                os.system(cmd)
                self.saved_dict[keyword] = 'ok'
        except KeyboardInterrupt:
            self.close('Abort due to keyboard interrupt.')
        self.close('Finished.')

    def close(self, reason):
        logger.info(reason)
        with open(GOOGLE_IMAGE_INDEX_FILE, 'wb') as f:
            pickle.dump(self.saved_dict, f)
        exit()


def main():
    g = GoogleSpider()
    g.run()


if __name__ == '__main__':
    main()
