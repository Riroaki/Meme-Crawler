import scrapy


class JikiItem(scrapy.Item):
    """Definition of a meme in jikipedia."""
    name = scrapy.Field()
    index = scrapy.Field()
    content = scrapy.Field()
    view = scrapy.Field()
    like = scrapy.Field()
    dislike = scrapy.Field()
    time = scrapy.Field()
    image_url = scrapy.Field()
    comment_count = scrapy.Field()
    tag_list = scrapy.Field()


class BilibiliItem(scrapy.Item):
    """A meme's related videos."""
    name = scrapy.Field()
    video_list = scrapy.Field()


class WeiboItem(scrapy.Item):
    """A meme's related weibos."""
    name = scrapy.Field()
    weibo_list = scrapy.Field()


class WeiboSingleItem(scrapy.Item):
    """Information about a piece of weibo."""
    mid = scrapy.Field()
    user = scrapy.Field()
    avator = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    like = scrapy.Field()
    repost = scrapy.Field()
    comment = scrapy.Field()
    source = scrapy.Field()
