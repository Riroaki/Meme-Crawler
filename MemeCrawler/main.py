import sys
from scrapy.cmdline import execute

crawlers = ['jiki', 'bilibili']

if __name__ == '__main__':
    args = sys.argv
    assert len(args) == 2
    assert args[1] in crawlers
    # First run Jikipedia to fetch all data entries,
    # and save their names into JIKI_INDEX file.
    # Secondly run Bilibili and all other spiders.
    execute(['scrapy', 'crawl', args[1], '-L', 'INFO'])
