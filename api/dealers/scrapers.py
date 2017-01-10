from decimal import Decimal
import re
from time import sleep

from lxml import html
import requests

from dealers.models import DealerScraperReport
from drivers.models import Driver
from manufacturing.models import Manufacturer
from utils.mixins.mode import ModeMixin


# @todo move all xpath patterns to another file
# @todo fetch price from list page and NOT detail
# @todo if there is already a DriverProductListing for a given path, simply
# update the price and DO NOT scrape the detail.
# try/except in each _scrape method


class Scraper(ModeMixin):

    SCRAPER_ID = "Sonical Scraper 1.0 (jonathan@ardent.tech)"

    def build_url(self, path):
        return self.base_url + path

    def get_html(self, url):
        sleep(1)
        page = requests.get(url, headers={"user-agent": self.SCRAPER_ID})
        return html.fromstring(page.content)


class DealerScraper(Scraper):

    def __init__(self, scraper_record):
        self.base_url = scraper_record.dealer.website
#        self.product_listings = self._get_product_listings(dealer)
#        print("{0}".format(len(self.product_listings)))
        self.manufacturers = {m.name: m for m in Manufacturer.objects.all()}
        self.report = DealerScraperReport(scraper=scraper_record)

#    def _get_product_listings(self, dealer):
#        product_listings = DriverProductListing.objects.filter(dealer=dealer)
#        return {pl.path: pl for pl in product_listings}


class PartsExpressScraper(DealerScraper):

    SEED = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def __init__(self, scraper_record):
        super(PartsExpressScraper, self).__init__(scraper_record)
        self.result = {
            "category_paths": [], "driver_paths": [], "drivers": [], "errors": []}

    def run(self):
        limit = self._get_limit()
        self._scrape_category_paths(self.SEED, limit)

        for category_path in self.result["category_paths"]:
            self._scrape_driver_paths(category_path, limit)

        for driver_path in self.result["driver_paths"]:
            self._scrape_driver(driver_path)

        self._process_result()

    def _get_limit(self):
        return None if self.pro_mode() else 1

    def _process_result(self):
        Driver.objects.bulk_create(self.result["drivers"])
        self._result_to_report()

    def _result_to_report(self):
        self.report.attempted = len(self.result["driver_paths"])
        self.report.processed = len(self.result["drivers"])
        self.report.save()

    def _scrape_category_paths(self, path, limit):
        patterns = {"DRIVER_CATEGORY": '//a[@id="lbCategoryName"]/@href'}
        categories = self.get_html(
            self.build_url(path)).xpath(patterns["DRIVER_CATEGORY"])

        self.result["category_paths"] = [
            c for c in categories if not re.search(r"replace|recone", c)][:limit]

    def _scrape_driver(self, path):
        patterns = [
            ('//div[@id="MiddleColumn1"]', []),
            ('//div[@class="ProducDetailsNote"]', [
                # (key, table row column one text, formatter)
                ("dc_resistance", "DC Resistance (Re)", "decimal"),
                ("electromagnetic_q", "Electromagnetic Q (Qes)", "decimal"),
                ("manufacturer", "Brand", "manufacturer"),
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

        data = {}
        tree = self.get_html(self.build_url(path))

        for idx, section in enumerate(patterns):
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

        self.result["drivers"].append(Driver(**data))

    def _scrape_driver_paths(self, path, limit):
        patterns = {
            "DRIVER_DETAIL": '//a[@id="GridViewProdLink"]/@href',
            "NEXT_PAGE": '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href',
        }
        tree = self.get_html(self.build_url(path))

        for driver in tree.xpath(patterns["DRIVER_DETAIL"]):
            self.result["driver_paths"].append(driver)

        if limit is None:
            try:
                return self._get_drivers(tree.xpath(patterns["NEXT_PAGE"])[0])
            except IndexError:
                return
            except:
                raise

    def _to_decimal(self, val):
        return Decimal(val.split(" ")[0])

    def _to_int(self, val):
        return int(val.split(" ")[0])

    def _to_manufacturer(self, val):
        try:
            return self.manufacturers[val]
        except:
            self.manufacturers[val] = Manufacturer.objects.create(name=val)
            return self.manufacturers[val]
