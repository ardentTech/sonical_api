from decimal import Decimal
import re
from time import sleep

from lxml import html
import requests

from drivers.models import DriverProductListing
from utils.mixins.mode import ModeMixin


# @todo fetch price from list page and NOT detail
# @todo DealerScraperResult
# @todo if there is already a DriverProductListing for a given path, simply
# update the price and DO NOT scrape the detail.


class Scraper(ModeMixin):

    SCRAPER_ID = "Sonical Scraper 1.0 (jonathan@ardent.tech)"

    def build_url(self, path):
        return self.base_url + path

    def get_html(self, url):
        sleep(1)
        page = requests.get(url, headers={"user-agent": self.SCRAPER_ID})
        return html.fromstring(page.content)


class DealerScraper(Scraper):

    def __init__(self, dealer):
        self.base_url = dealer.website
        # @todo make a dict of {url: price}
        self.product_listings = self._get_product_listings(dealer)

    def _get_product_listings(self, dealer):
        return DriverProductListing.objects.filter(dealer=dealer)


class PartsExpressScraper(DealerScraper):

    SEED = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def run(self):
        limit = self._get_limit()
        category_paths = self._get_category_paths(self.SEED, limit)
        driver_paths = []

        for c in category_paths:
            self._get_driver_paths(c, driver_paths, limit)

        drivers = [self._get_driver(path) for path in driver_paths[:limit]]

        print("Categories: {0}".format(len(category_paths)))
        print("Driver Paths: {0}".format(len(driver_paths)))
        print("Drivers: {0}".format(drivers))

    def _get_category_paths(self, path, limit):
        targets = {"DRIVER_CATEGORY": '//a[@id="lbCategoryName"]/@href'}
        categories = self.get_html(
            self.build_url(path)).xpath(targets["DRIVER_CATEGORY"])

        return [c for c in categories if not re.search(r"replace|recone", c)][:limit]

    def _get_driver(self, path):
        targets = [
            ('//div[@id="MiddleColumn1"]', [
                # (key, xpath pattern, formatter)
                ("price", 'div[@class="PriceContBox"]/div[1]/div[1]/span[1]/span[2]/text()', "decimal"),
            ]),
            ('//div[@class="ProducDetailsNote"]', [
                # (key, table row column one text, formatter)
                ("dc_resistance", "DC Resistance (Re)", "decimal"),
                ("electromagnetic_q", "Electromagnetic Q (Qes)", "decimal"),
                ("manufacturer", "Brand", None),
                ("max_power", "Power Handling (max)", "int"),
                ("mechanical_q", "Mechanical Q (Qms)", "decimal"),
                ("model", "Model", None),
                ("nominal_diameter", "Nominal Diameter", "decimal"),
                ("nominal_impedance", "Impedance", "decimal"),
                ("resonant_frequency", "Resonant Frequency (Fs)", "decimal"),
                ("rms_power", "Power Handling (RMS)", "int"),
                ("sensitivity", "Sensitivity", "decimal"),
                ("voice_coil_inductance", "Voice Coil Inductance (Le)", "decimal"),
            ])
        ]

        data = {"path": path}
        tree = self.get_html(self.build_url(path))

        for idx, section in enumerate(targets):
            root = tree.xpath(section[0])[0]
            pattern = '{0}'
            if idx == 1:
                pattern = 'span[text()="{0}"]/following-sibling::span[1]/text()'

            for items in section[1]:
                try:
                    val = root.xpath("//" + pattern.format(items[1]))[0]
                    if items[2]:
                        val = getattr(self, "_to_" + items[2])(val)
                    data[items[0]] = val
                except:
                    pass

        return data

    def _get_driver_paths(self, path, store, limit):
        targets = {
            "DRIVER_DETAIL": '//a[@id="GridViewProdLink"]/@href',
            "NEXT_PAGE": '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href',
        }
        tree = self.get_html(self.build_url(path))

        for driver in tree.xpath(targets["DRIVER_DETAIL"]):
            store.append(driver)

        if limit is None:
            try:
                return self._get_drivers(tree.xpath(targets["NEXT_PAGE"])[0])
            except IndexError:
                return
            except:
                raise

    def _get_limit(self):
        return None if self.pro_mode() else 2

    def _to_decimal(self, val):
        return Decimal(val.split(" ")[0])

    def _to_int(self, val):
        return int(val.split(" ")[0])
