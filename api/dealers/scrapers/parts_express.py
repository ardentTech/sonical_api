from decimal import Decimal
import re
from time import sleep

from lxml import html
import requests


# @todo DriverScraper


class ScraperData(object):

    def __init__(self):
        self._data = {"items": []}

    def add(self, key, data):
        self._data[key].append(data)

    def concat(self, key, data):
        try:
            self._data[key] += data
        except KeyError:
            self._data[key] = data

    def get(self, key=None):
        return self._data if key is None else self._data[key]

    def set(self, key, val):
        self._data[key] = val


class Scraper(object):

    SCRAPER_ID = "Sonical Scraper 1.0 (jonathan@ardent.tech)"

    def __init__(self, base_url):
        self.base_url = base_url
        self.data = ScraperData()

    def get_html(self, path):
        sleep(1)  # avoid barraging server
        page = requests.get(
            self.base_url + path, headers={"user-agent": self.SCRAPER_ID})
        return html.fromstring(page.content)

    def run(self):
        raise Exception("Scrapers must implement a `run` method.")


class DealerScraper(Scraper):
    """
    Responsible managing data, coordinating path scrapers and creating a
    DealerScraperReport.
    """

    def __init__(self, db_record):
        self.db_record = db_record
        self.dealer = self.db_record.dealer
        super(DealerScraper, self).__init__(self.dealer.website)


class PathScraper(Scraper):
    """
    Responsible for scraping a path and returning a dict.
    """

    pass


class CategoryScraper(PathScraper):

    PATTERNS = {"path": '//a[@id="lbCategoryName"]/@href'}

    def run(self, path):
        categories = self.get_html(path).xpath(self.PATTERNS["path"])
        self.data.set(
            "items",
            [{"path": c} for c in categories if not re.search(r"replace|recone", c)])
        return self


class DriverScraper(PathScraper):

    PATTERNS = [
        {
            "id": "overview",
            "scope": '//div[@id="MiddleColumn1"]',
            "base_pattern": '{0}',
            "items": [
                # (django key, PE pattern, post_scrape)
                ("model", 'h1[@class="ProductTitle"]/span/text()', "")]},
        {
            "id": "details",
            "scope": '//div[@class="ProducDetailsNote"]',
            "base_pattern": 'span[text()="{0}"]/following-sibling::span[1]/text()',
            "items": [
                # (django key, PE pattern, post_scrape)
                ("basket_frame", "Basket / Frame Material", None),
                ("bl_product", "BL Product (BL)", "_to_decimal"),
                ("compliance_equivalent_volume", "Compliance Equivalent Volume (Vas)", "_to_decimal"),
                ("cone", "Cone Material", None),
                ("cone_surface_area", "Surface Area of Cone (Sd)", "_to_decimal"),
                ("dc_resistance", "DC Resistance (Re)", "_to_decimal"),
                ("diaphragm_mass_including_airload", "Diaphragm Mass Inc. Airload (Mms)", "_to_diaphragm"),
                ("electromagnetic_q", "Electromagnetic Q (Qes)", "_to_decimal"),
                ("frequency_response", "Frequency Response", "_to_frequency_response"),
                ("magnet", "Magnet Material", None),
                ("manufacturer", "Brand", None),
                ("max_power", "Power Handling (max)", "_to_int"),
                ("max_linear_excursion", "Maximum Linear Excursion (Xmax)", "_to_decimal"),
                ("mechanical_compliance_of_suspension", "Mechanical Compliance of Suspension (Cms)", "_to_decimal"),
                ("mechanical_q", "Mechanical Q (Qms)", "_to_decimal"),
                ("nominal_diameter", "Nominal Diameter", "_to_diameter"),
                ("nominal_impedance", "Impedance", "_to_decimal"),
                ("resonant_frequency", "Resonant Frequency (Fs)", "_to_decimal"),
                ("rms_power", "Power Handling (RMS)", "_to_int"),
                ("sensitivity", "Sensitivity", "_to_decimal"),
                ("surround", "Surround Material", None),
                ("voice_coil_diameter", "Voice Coil Diameter", "_to_diameter"),
                ("voice_coil_former", "Voice Coil Former", None),
                ("voice_coil_inductance", "Voice Coil Inductance (Le)", "_to_decimal"),
                ("voice_coil_wire", "Voice Coil Wire Material", None)]}]

    def run(self, path):
        tree = self.get_html(path)

        for section in self.PATTERNS:
            scope = tree.xpath(section["scope"])[0]
            for item in section["items"]:
                key = item[0]
                pattern = ".//" + section["base_pattern"].format(item[1])
                post_scrape = item[2]
                try:
                    val = scope.xpath(pattern)[0]
                    if post_scrape:
                        val = getattr(self, post_scrape)(val)
                    self.data.set(key, val)
                except Exception:
                    pass

        # @todo this sucks but will have to do for now
        self.data.set(
            "model", self.data.get("model").lstrip(self.data.get("manufacturer")))
        return self

    def _to_decimal(self, val):
        return Decimal(val.split(" ")[0])

    def _to_diameter(self, val):
        _val = val.rstrip("\"")
        if "-" in _val:
            parts = _val.split("-")
            whole_number = parts[0]
            fraction = parts[1].split("/")
            decimal_digits = fraction[0] / fraction[1]
            _val = whole_number + "." + decimal_digits
        return Decimal(_val)

    def _to_diaphragm(self, val):
        return Decimal(val.rstrip("g"))

    def _to_int(self, val):
        return int(val.split(" ")[0])

    def _to_frequency_response(self, val):
        parts = val.replace(",", "").split(" ")
        return (Decimal(parts[0]), Decimal(parts[2]))


class DriverListingScraper(PathScraper):

    PATTERNS = {
        "next_page": '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href',
        "listing": {
            "scope": '//a[@id="GridViewProdLink"]',
            "path": './/@href',
            "price": './/div[@class="CatPriceSection"]/div/div/span[2]/text()'}}

    def run(self, path):
        tree = self.get_html(path)
        for listing in tree.xpath(self.PATTERNS["listing"]["scope"]):
            self.data.add("items", {
                "path": listing.xpath(self.PATTERNS["listing"]["path"])[0],
                "price": listing.xpath(self.PATTERNS["listing"]["price"])[0]
            })
        try:
            self.data.set("next_page", tree.xpath(self.PATTERNS["next_page"])[0])
        except IndexError:
            self.data.set("next_page", None)
        return self


class PartsExpressScraper(DealerScraper):

    SEED = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def run(self):
        self._scrape_categories(self.SEED)
        for category in self.data.get("categories"):
            self._scrape_driver_listings(category["path"])
        for driver_listing in self.data.get("driver_listings"):
            self._scrape_driver(driver_listing["path"])

    def _scrape_categories(self, path):
        self.data.set("categories", CategoryScraper(
            self.base_url).run(path).data.get()["items"])

    def _scrape_driver(self, path):
        res = DriverScraper(self.base_url).run(path).data.get()
        print("{0}".format(res))

    def _scrape_driver_listings(self, path):
        res = DriverListingScraper(self.base_url).run(path).data.get()
        self.data.concat("driver_listings", res["items"])
        # handle pagination
        if res["next_page"] is not None:
            self._scrape_driver_listings(res["next_page"])
