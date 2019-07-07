import scrapy


class DefinitionItem(scrapy.Item):
    """Definition of entry."""
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
