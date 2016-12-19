from decimal import Decimal
import re

from .scraper import Scraper


# @todo scrape driver price, rating and review #
# @todo need some sort of dev mode
# @todo multithreading
# @todo adjust XPATH patterns to match by text instead of just position indexes


URL = "https://www.parts-express.com"
XPATH_PATTERNS = {
    "DC_RESISTANCE": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[2]/span[2]/text()',
    "DRIVER_CATEGORY_XPATH": '//a[@id="lbCategoryName"]/@href',
    "DRIVER_DETAIL_XPATH": '//a[@id="GridViewProdLink"]/@href',
    "ELECTROMAGNETIC_Q": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[7]/span[2]/text()',
    "MANUFACTURER": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[1]/span[2]/text()',
    "MAX_POWER": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[4]/span[2]/text()',
    "MECHANICAL_Q": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[5]/span[2]/text()',
    "MODEL": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[2]/span[2]/text()',
    "NEXT_PAGE_XPATH": '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href',
    "NOMINAL_DIAMETER": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[1]/span[2]/text()',
    "NOMINAL_IMPEDANCE": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[5]/span[2]/text()',
    "RESONANT_FREQUENCY": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[1]/span[2]/text()',
    "REVIEW_COUNT": '//*[@id="TurnToTopSummary"]/div[1]/div/div[2]/a[1]/text()',
    "RMS_POWER": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[2]/span[2]/text()',
    "SENSITIVITY": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[8]/span[2]/text()',
    "VOICE_COIL_INDUCTANCE": '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[4]/span[2]/text()',
}


class DriverScraper(Scraper):

    def __init__(self):
        # @todo is there a way to determine these programmatically from the model
        # instead of writing all this out?
        _attrs = [
            ("dc_resistance", XPATH_PATTERNS["DC_RESISTANCE"], self._to_decimal),
            ("electromagnetic_q", XPATH_PATTERNS["ELECTROMAGNETIC_Q"], None),
            ("manufacturer", XPATH_PATTERNS["MANUFACTURER"], None),
            ("max_power", XPATH_PATTERNS["MAX_POWER"], self._to_int),
            ("mechanical_q", XPATH_PATTERNS["MECHANICAL_Q"], None),
            ("model", XPATH_PATTERNS["MODEL"], None),
            ("nominal_diameter", XPATH_PATTERNS["NOMINAL_DIAMETER"], None),
            ("nominal_impedance", XPATH_PATTERNS["NOMINAL_IMPEDANCE"], self._to_decimal),
            ("resonant_frequency", XPATH_PATTERNS["RESONANT_FREQUENCY"], self._to_decimal),
            ("rms_power", XPATH_PATTERNS["RMS_POWER"], self._to_int),
            ("sensitivity", XPATH_PATTERNS["SENSITIVITY"], self._to_decimal),
            ("voice_coil_inductance", XPATH_PATTERNS["VOICE_COIL_INDUCTANCE"], self._to_decimal)]
        self.driver_attrs = [
            {"key": attr[0], "pattern": attr[1], "sanitizer": attr[2]} for attr in _attrs]

    def run(self, path):
        data = {"data_source": URL + path}
        tree = self._get_tree(data["data_source"])

        for attr in self.driver_attrs:
            val = tree.xpath(attr["pattern"])[0]
            if attr["sanitizer"] is not None:
                val = attr["sanitizer"](val)
            data[attr["key"]] = val

        return data

    def _to_decimal(self, val):
        return Decimal(val.split(" ")[0])

    def _to_int(self, val):
        return int(val.split(" ")[0])


class DriverListScraper(Scraper):

    def __init__(self):
        self.data = []

    def run(self, path):
        tree = self._get_tree(URL + path)

        for driver in tree.xpath(XPATH_PATTERNS["DRIVER_DETAIL_XPATH"]):
            self.data.append(driver)

        # crawl pagination
        try:
            return self.run(tree.xpath(XPATH_PATTERNS["NEXT_PAGE_XPATH"])[0])
        except IndexError:
            return self.data

        return self.data


class CategoryListScraper(Scraper):

    def run(self, path):
        categories = self._get_tree(URL + path).xpath(XPATH_PATTERNS["DRIVER_CATEGORY_XPATH"])
        return [c for c in categories if not re.search(r'replace|recone', c)]


class PartsExpressScraper(Scraper):

    INITIAL_CATEGORY_PATH = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def __init__(self):
        self.category_list_scraper = CategoryListScraper()
        self.driver_list_scraper = DriverListScraper()
        self.driver_scraper = DriverScraper()

    def run(self):
        drivers = []

        for cp in self.category_list_scraper.run(self.INITIAL_CATEGORY_PATH):
            driver_paths = self.driver_list_scraper.run(cp)
            for dp in driver_paths:
                drivers.append(self.scrapers["driver"].run(dp))

        return drivers
