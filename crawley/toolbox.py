from crawlers import BaseCrawler

default_crawler = BaseCrawler()

def request(url, data=None):

    return default_crawler.request(url, data=data)