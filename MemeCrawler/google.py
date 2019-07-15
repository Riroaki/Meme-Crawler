import os
import pickle
import random
from settings import GOOGLE_IMAGE_DIR, JIKI_INDEX_FILE
from logger import logger


class GoogleSpider(object):
    name = 'google'

    def __init__(self):
        # Max limit of videos for one keyword
        self.limit = 5
        saved = set()
        if not os.path.exists(GOOGLE_IMAGE_DIR):
            os.mkdir(GOOGLE_IMAGE_DIR)
        for path in os.listdir(GOOGLE_IMAGE_DIR):
            if os.path.isdir(path):
                full_path = os.path.join(GOOGLE_IMAGE_DIR, path)
                if len(os.listdir(full_path)) < self.limit:
                    os.remove(full_path)
                else:
                    saved.add(path)
        all_dict = {}
        if os.path.exists(JIKI_INDEX_FILE):
            with open(JIKI_INDEX_FILE, 'rb') as f:
                all_dict = pickle.load(f)
        # Generate to-do list
        todo = []
        for k in all_dict.values():
            if k not in {'error', 'noname'} and k not in saved:
                todo.append(k)
        # Randomly start to aviod stuck
        random.shuffle(todo)
        self.todo_list = todo

    def run(self) -> None:
        cmd_raw = ('googleimagesdownload'
                   ' -o "{path}" -l {limit}'.format(path=GOOGLE_IMAGE_DIR,
                                                    limit=self.limit))
        try:
            for keyword in self.todo_list:
                cmd = ' '.join([cmd_raw, '-k', keyword])
                os.system(cmd)
        except KeyboardInterrupt:
            self.close('Abort due to keyboard interrupt.')
        self.close('Finished.')

    @staticmethod
    def close(reason):
        logger.info(reason)
        exit()


def main():
    g = GoogleSpider()
    g.run()


if __name__ == '__main__':
    main()
