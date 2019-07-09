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
    """Definition of a meme and related videos."""
    name = scrapy.Field()
    video_list = scrapy.Field()
