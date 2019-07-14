import os
import re
import json
import pickle
import numpy as np
import logging
from MemeCrawler.settings import BILIBILI_DIR, JIKI_DIR, WEIBO_DIR, \
    GOOGLE_IMAGE_DIR

MERGE_DIR = 'data/merged'
MERGE_INEDX_FILE = 'index/merged_index'
logging.basicConfig(level=logging.INFO)


def txt_filter(fname: str) -> bool:
    is_txt = fname.endswith('.txt')
    return is_txt


def dir_filter(fname: str) -> bool:
    full_name = os.path.join(GOOGLE_IMAGE_DIR, fname)
    is_dir = os.path.isdir(full_name)
    return is_dir


def img_filter(fname: str) -> bool:
    img_ext = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
    ext = fname[fname.rfind('.'):].lower()
    is_img = ext in img_ext
    return is_img


jiki_list = set(filter(txt_filter, os.listdir(JIKI_DIR)))
bilibili_list = set(filter(txt_filter, os.listdir(BILIBILI_DIR)))
weibo_list = set(filter(txt_filter, os.listdir(WEIBO_DIR)))
google_list = set(filter(dir_filter, os.listdir(GOOGLE_IMAGE_DIR)))


def can_merge(entry: str) -> bool:
    in_bilibili = entry + '.txt' in bilibili_list
    in_weibo = entry + '.txt' in weibo_list
    in_google = entry in google_list
    all_in = in_bilibili and in_weibo and in_google
    return all_in


def ensure_data(data: dict) -> dict:
    def process_value(raw) -> int:
        if isinstance(raw, int):
            return raw
        if isinstance(raw, str):
            k = 1000 if 'k' in raw else 1
            raw = raw.replace('k', '')
            raw = int(float(raw) * k)
            return raw
        return 0

    def process_weibo(weibo_raw_list: list) -> list:
        for weibo in weibo_raw_list:
            avator = 'https:' + weibo['avator']
            content = weibo['content']
            time = weibo['time']
            # Parse content
            content = re.sub('<.*?>', '\n', content)
            content = re.sub('\s+', '\n', content)
            head1 = '展开全文\nc\n'
            tail1 = '\n收起全文'
            head2 = '\nc\n投诉\n'
            tail2 = '\n&nbsp;来自\n'
            if head1 in content:
                content = content[content.find(head1) + len(head1):]
                content = content[: content.rfind(tail1)]
            else:
                content = content[content.find(head2) + len(head2):]
                content = content[: content.rfind(tail2)]
            img_list = re.findall('<img src="(.*?)"', content)
            weibo['imgList'] = ['https:' + img for img in img_list]
            time = re.sub('\s+', '', time)
            weibo['content'] = content
            weibo['avator'] = avator
            weibo['time'] = time
        return weibo_raw_list

    res = {'id': data['index'], 'name': data['name'], 'time': data['time'],
           'image': data['image_url'], 'view': process_value(data['view']),
           'like': process_value(data['like']),
           'dislike': process_value(data['dislike']),
           'tagList': data['tag_list'], 'content': data['content'],
           'imageList': data['image_list'], 'videoList': data['video_list'],
           'weiboList': process_weibo(data['weibo_list'])}
    return res


def main():
    merged_entry = set()
    if os.path.exists(MERGE_INEDX_FILE):
        with open(MERGE_INEDX_FILE, 'rb') as f:
            merged_entry = pickle.load(f)
    id_to_file = {}
    entry_to_ids = {}
    for fname in jiki_list:
        index = int(fname[:fname.find('_')])
        entry = fname[fname.find('_') + 1: fname.rfind('.txt')]
        id_to_file[index] = os.path.join(JIKI_DIR, fname)
        if not can_merge(entry) or entry in merged_entry:
            continue
        if entry not in entry_to_ids:
            entry_to_ids[entry] = [index]
        else:
            entry_to_ids[entry].append(index)
    to_merge = {}
    for entry, id_list in entry_to_ids.items():
        # Choose the file whose size is largest
        size_list = [os.path.getsize(id_to_file[index]) for index in
                     id_list]
        remain = id_list[int(np.argmax(size_list))]
        to_merge[entry] = remain
    logging.info('{} entries to merge.'.format(len(to_merge)))
    # Merge all kinds of data
    if not os.path.exists(MERGE_DIR):
        os.mkdir(MERGE_DIR)
    for entry, index in to_merge.items():
        try:
            jiki_file = id_to_file[index]
            bilibili_file = os.path.join(BILIBILI_DIR, entry + '.txt')
            weibo_file = os.path.join(WEIBO_DIR, entry + '.txt')
            google_dir = os.path.join(GOOGLE_IMAGE_DIR, entry)
            with open(jiki_file, 'r') as f:
                data = json.load(f)
            with open(bilibili_file, 'r') as f:
                video_data = json.load(f)
                data['video_list'] = video_data['video_list']
            with open(weibo_file, 'r') as f:
                weibo_data = json.load(f)
                data['weibo_list'] = weibo_data['weibo_list']
            image_list = list(filter(img_filter, os.listdir(google_dir)))
            image_list = [os.path.join(entry, image) for image in image_list]
            data['image_list'] = image_list
            # Reformat data
            data = ensure_data(data)
            with open(os.path.join(MERGE_DIR,
                                   '{}_{}.txt'.format(index, entry)), 'w') as f:
                json.dump(data, f, ensure_ascii=False,
                          separators=(',', ':'), indent=4)
            merged_entry.add(entry)
        except Exception as e:
            logging.warning(e)
    logging.info('{} entries have been merged.'.format(len(to_merge)))
    with open(MERGE_INEDX_FILE, 'wb') as f:
        pickle.dump(merged_entry, f)


if __name__ == '__main__':
    main()
