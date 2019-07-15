import os
import re
import json
import pickle
import logging
import datetime
import tqdm
import jieba
from wordcloud import WordCloud
from settings import BILIBILI_DIR, JIKI_DIR, WEIBO_DIR, GOOGLE_IMAGE_DIR

MERGE_DIR = 'data/merged'
# Optional: generate word cloud pictures
CLOUD_DIR = 'data/wordcloud'
MERGE_INEDX_FILE = 'index/merged_index'
FONT_PATH = 'fonts/HanyiSentyCrayon-2.ttf'
STOP_WORDS_FILE = 'stopwords/stopwords.txt'
logging.basicConfig(level=logging.INFO)
jieba.setLogLevel(logging.INFO)


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


def ensure_data(data: dict) -> dict:
    # Reformat data
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
                content = content[:content.rfind(tail1)]
            else:
                content = content[content.find(head2) + len(head2):]
                content = content[:content.rfind(tail2)]
            img_list = re.findall('<img src="(.*?)"', content)
            weibo['imgList'] = ['https:' + img for img in img_list]
            if time == '0000-00-00':
                time = datetime.datetime.now().strftime('%Y-%m-%d')
            else:
                time = re.sub('\s+', '', time)
            weibo['content'] = content
            weibo['avator'] = avator
            weibo['time'] = time
        return weibo_raw_list

    res = {
        'id': data['index'],
        'name': data['name'],
        'time': data['time'],
        'image': data['image_url'],
        'view': process_value(data['view']),
        'like': process_value(data['like']),
        'dislike': process_value(data['dislike']),
        'tagList': data['tag_list'],
        'content': data['content'],
        'imageList': data['image_list'],
        'videoList': data['video_list'],
        'weiboList': process_weibo(data['weibo_list'])
    }
    return res


# Load file list
jiki_list = set(filter(txt_filter, os.listdir(JIKI_DIR)))
bilibili_list = set(filter(txt_filter, os.listdir(BILIBILI_DIR)))
weibo_list = set(filter(txt_filter, os.listdir(WEIBO_DIR)))
google_list = set(filter(dir_filter, os.listdir(GOOGLE_IMAGE_DIR)))
# Load stop words dictionary
stopwords_set = set(
    [line.strip() for line in open(STOP_WORDS_FILE, 'r').readlines()])


def can_merge(entry: str) -> bool:
    in_bilibili = entry + '.txt' in bilibili_list
    in_weibo = entry + '.txt' in weibo_list
    in_google = entry in google_list
    all_in = in_bilibili and in_weibo and in_google
    return all_in


def extract_text(data: dict) -> str:
    # Combine certain attributes from entry data
    name = data['name'] * 5
    tags = ' '.join(data['tagList']) * 10
    content = data['content'] * 5
    video_content = ' '.join(
        [video['description'] for video in data['videoList']])
    weibo_content = ' '.join([weibo['content'] for weibo in data['weiboList']])
    raw = ' '.join([name, tags, content, video_content, weibo_content])
    # Cut sentences and remove stop words
    words = list(filter(lambda w: w not in stopwords_set, jieba.cut(raw)))
    text = ' '.join(words)
    return text


def main():
    merged_entry = set()
    if os.path.exists(MERGE_INEDX_FILE):
        with open(MERGE_INEDX_FILE, 'rb') as f:
            merged_entry = pickle.load(f)
    id_to_file = {}
    entry_to_ids = {}
    for fname in jiki_list:
        index = int(fname[:fname.find('_')])
        entry = fname[fname.find('_') + 1:fname.rfind('.txt')]
        id_to_file[index] = os.path.join(JIKI_DIR, fname)
        if not can_merge(entry) or entry in merged_entry:
            continue
        if entry not in entry_to_ids:
            entry_to_ids[entry] = [index]
        else:
            entry_to_ids[entry].append(index)
    to_merge = {}
    # Merge all items with same name
    for entry, id_list in entry_to_ids.items():
        full = {}
        for index in id_list:
            try:
                with open(
                        os.path.join(JIKI_DIR,
                                     '{}_{}.txt'.format(index, entry)),
                        'r') as f:
                    data = json.load(f)
                    if len(full) < len(data):
                        full.update(data)
                    else:
                        full['tag_list'].extend(data['tag_list'])
                        full['content'] += '\n\n' + data['content']
            except Exception as e:
                logging.warning('{}:{}'.format(entry, e))
                merged_entry.add(entry)
        # Skip invalid format
        if len(full) == 0:
            continue
        full['tag_list'] = list(set(full['tag_list']))
        to_merge[entry] = full
    logging.info('{} entries to merge.'.format(len(to_merge)))
    # Merge all kinds of data
    if not os.path.exists(MERGE_DIR):
        os.mkdir(MERGE_DIR)
    if not os.path.exists(CLOUD_DIR):
        os.mkdir(CLOUD_DIR)
    # Visualize progress using a progress bar
    progress_bar = tqdm.tqdm(total=len(to_merge))
    # Cloud object
    cloud = WordCloud(
        font_path=FONT_PATH,
        background_color='white',
        max_words=20,
        max_font_size=250,
        width=1000,
        height=500,
        collocations=False)
    # Merge data from all sources
    for entry, data in to_merge.items():
        try:
            bilibili_file = os.path.join(BILIBILI_DIR, entry + '.txt')
            weibo_file = os.path.join(WEIBO_DIR, entry + '.txt')
            google_dir = os.path.join(GOOGLE_IMAGE_DIR, entry)
            with open(bilibili_file, 'r') as f:
                video_data = json.load(f)
                data['video_list'] = video_data['video_list']
            with open(weibo_file, 'r') as f:
                weibo_data = json.load(f)
                data['weibo_list'] = weibo_data['weibo_list']
            image_list = list(filter(img_filter, os.listdir(google_dir)))
            image_list = [
                os.path.join(GOOGLE_IMAGE_DIR, entry, image)
                for image in image_list
            ]
            data['image_list'] = image_list
            # Reformat data
            data = ensure_data(data)
            # Draw word cloud
            text = extract_text(data)
            pic = cloud.generate(text)
            pic_name = os.path.join(CLOUD_DIR, '{}.png'.format(entry))
            pic.to_file(pic_name)
            data['wordCloud'] = pic_name
            # Save data
            with open(
                    os.path.join(MERGE_DIR, '{}_{}.txt'.format(
                        data['id'], entry)), 'w') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'),
                          indent=4)
            merged_entry.add(entry)
        except Exception as e:
            logging.warning('{}:{}'.format(entry, e))
            merged_entry.add(entry)
        progress_bar.update(1)
    progress_bar.close()
    logging.info('{} entries have been merged.'.format(len(to_merge)))
    with open(MERGE_INEDX_FILE, 'wb') as f:
        pickle.dump(merged_entry, f)


if __name__ == '__main__':
    main()
