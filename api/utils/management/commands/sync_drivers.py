from collections import deque

from django.core.management.base import BaseCommand

from lxml import html
import requests


class Command(BaseCommand):

    host = "www.parts-express.com"
    protocol = "https://"

    def __init__(self, *args, **kwargs):
        self.data_store = {}
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        self._crawl_parts_express()
        print("done!")

    def _build_url(self, path):
        return self.protocol + self.host + path

    def _crawl_category(self, category):
        data_store = self.data_store.setdefault(category[0], [])
        self._scrape_paginated_drivers(self._build_url(category[1]), data_store)

    def _scrape_paginated_drivers(self, url, data_store):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        drivers = tree.xpath('//a[@id="GridViewProdLink"]/@href')
        deque(map(data_store.append, drivers))

        try:
            next_path = tree.xpath('//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href')[0]
            self._scrape_paginated_drivers(self._build_url(next_path), data_store)
        except IndexError:
            return
        except Exception as e:
            print("Unexpected Exception: {0}".format(e))  # @todo log this

    def _crawl_parts_express(self):
        categories = self._get_categories()
        deque(map(self._crawl_category, categories))

    def _get_categories(self):
# @todo don't hardcode path
        return [("woofers", "/cat/woofers/15")]
