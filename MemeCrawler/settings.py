# -*- coding: utf-8 -*-

# Scrapy settings for MemeCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'MemeCrawler'

SPIDER_MODULES = ['MemeCrawler.spiders']
NEWSPIDER_MODULE = 'MemeCrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'MemeCrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# Default using google-bot header
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': ('Mozilla/5.0 (compatible; Googlebot/2.1;'
                   ' +http://www.google.com/bot.html)'),
    'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
               'image/webp,image/apng,*/*;q=0.8,'
               'application/signed-exchange;v=b3'),
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Origin': 'https://google.com',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'MemeCrawler.middlewares.MetacrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'MemeCrawler.middlewares.RandomUserAgentMiddlware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'MemeCrawler.middlewares.SeleniumMiddleware': 543
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'MemeCrawler.pipelines.MemecrawlerPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# User-Agent to choose from
UA_LIST = [
    # Google-bot UAs
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    ('Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P)'
     ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96'
     ' Mobile Safari/537.36 (compatible; Googlebot/2.1;'
     ' +http://www.google.com/bot.html)'),
    'Googlebot/2.1 (+http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Googlebot/2.1; http://www.google.com/bot.html)',
    # Baidu-bot UAs
    ('Mozilla/5.0 (compatible; Baiduspider/2.0;'
     '+http://www.baidu.com/search/spider.html）'),
    ('Mozilla/5.0 (compatible;Baiduspider-render/2.0;'
     ' +http://www.baidu.com/search/spider.html)'),
    # Normal UAs
    ("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser;"
     " .NET CLR 1.1.4322; .NET CLR 2.0.50727)"),
    ("Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser;"
     " SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)"),
    ("Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35;"
     " Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"),
    ("Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64;"
     " Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729;"
     " .NET CLR 2.0.50727; Media Center PC 6.0)"),
    ("Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64;"
     " Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729;"
     " .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)"),
    ("Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2;"
     " .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2;"
     " .NET CLR 3.0.04506.30)"),
    ("Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15"
     " (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)"),
    ("Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+"
     " (KHTML, like Gecko, Safari/419.3) Arora/0.6"),
    ("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;"
     " rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"),
    ("Mozilla/5.0 (Windows; U; Windows NT 5.1;"
     " zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"),
]

# Driver path
DRIVER_PATH = 'driver/chromedriver'

# Download control
DOWNLOAD_DELAY = 10
DOWNLOAD_TIMEOUT = 25
RETRY_ENABLED = False
RETRY_TIMES = 1

# Selenium parameters
SHOW_WINDOW = False
POLL_FREQUENCY = 4
RANDOM_SLEEP_LONG = 5
RANDOM_SLEEP_SHORT = 2

# Save directory
JIKI_DIR = 'data/jikipedia'
BILIBILI_DIR = 'data/bilibili'
WEIBO_DIR = 'data/weibo'
GOOGLE_IMAGE_DIR = 'data/google_image'

# Saved entry index files
JIKI_INDEX_FILE = 'index/jiki_index'
BILIBILI_INDEX_FILE = 'index/bilibili_index'
WEIBO_INDEX_FILE = 'index/weibo_index'
