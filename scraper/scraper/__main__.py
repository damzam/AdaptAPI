import asyncio
import json
import logging
import warnings
import sys

import scrapy

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.mock_carrier import MockCarrierSpider
from .spiders.mock_indemnity import MockIndemnitySpider

logging.getLogger('asyncio').propagate = False
logging.getLogger('scrapy').propagate = False
warnings.filterwarnings("ignore", category=scrapy.exceptions.ScrapyDeprecationWarning)

BASE_URL = 'https://scraping-interview.onrender.com'


def load_input():
    try:
        loaded = []
        with open(sys.argv[1]) as fp:
            for item in json.load(fp):
                loaded.append(item)
        return loaded
    except OSError as err:
        print('OUCH:', err)
        return []


def run_concurrent_spiders(targets):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for target in targets:
        url = '/'.join([BASE_URL, target['carrier'].lower(), target['customerId']])
        # if target['carrier'] == 'MOCK_INDEMNITY':
        #    process.crawl(MockIndemnitySpider, domain=url)
        if target['carrier'] == 'PLACEHOLDER_CARRIER': 
            process.crawl(MockCarrierSpider, domain=url)
    process.start()


def main():
    run_concurrent_spiders(load_input())


if __name__ == '__main__':
    main()
