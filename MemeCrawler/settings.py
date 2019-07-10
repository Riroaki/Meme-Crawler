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
DOWNLOAD_DELAY = 3
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
    'Accept': 'application/json, text/plain, */*',
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
    # Google-bot headers
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    ('Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P)'
     ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96'
     ' Mobile Safari/537.36 (compatible; Googlebot/2.1;'
     ' +http://www.google.com/bot.html)'),
    'Googlebot/2.1 (+http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Googlebot/2.1; http://www.google.com/bot.html)',
    # Baidu-bot headers
    ('Mozilla/5.0 (compatible; Baiduspider/2.0;'
     '+http://www.baidu.com/search/spider.html）'),
    ('Mozilla/5.0 (compatible;Baiduspider-render/2.0;'
     ' +http://www.baidu.com/search/spider.html)')
]

# Driver path
DRIVER_PATH = 'driver/chromedriver'

# Download control
DOWNLOAD_TIMEOUT = 10
RETRY_ENABLED = False
RETRY_TIMES = 1

# Selenium parameters
POLL_FREQUENCY = 2
RANDOM_SLEEP_LONG = 5
RANDOM_SLEEP_SHORT = 2

# Save directory
JIKI_DIR = 'data/jikipedia'
BILIBILI_DIR = 'data/bilibili'
WEIBO_DIR = 'data/weibo'

# Saved entry index files
JIKI_INDEX_FILE = 'index/jiki_index'
BILIBILI_INDEX_FILE = 'index/bilibili_index'
WEIBO_INDEX_FILE = 'index/weibo_index'
