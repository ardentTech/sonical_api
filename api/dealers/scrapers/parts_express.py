from decimal import Decimal
import re
from time import sleep

from lxml import html
import requests

from utils.mixins.mode import ModeMixin


# @todo scrapers as singletons that reset data on each run


class ScraperData(object):

    def __init__(self):
        # @todo need a way to handle single dicts (for drivers)
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
    Responsible for managing data, coordinating path scrapers and creating a
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
        _data = {}
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
                    _data[key] = val
                except Exception:
                    pass

        # special processing
        _data["model"] = _data["model"].lstrip(_data["manufacturer"])

        self.data.add("items", _data)
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
                "price": listing.xpath(self.PATTERNS["listing"]["price"])[0].lstrip("$")
            })
        try:
            self.data.set("next_page", tree.xpath(self.PATTERNS["next_page"])[0])
        except IndexError:
            self.data.set("next_page", None)
        return self


class PartsExpressScraper(ModeMixin, DealerScraper):

    SEED = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def scrape_categories(self):
        limit = None if self.pro_mode() else 1
        return CategoryScraper(self.base_url).run(self.SEED).data.get()["items"][:limit]

    def scrape_driver_listings(self):
        data = []
        for c in self.scrape_categories():
            self._scrape_driver_listings(data, c["path"])
        return data

    def scrape_driver(self, path):
        return DriverScraper(self.base_url).run(path).data.get()["items"][0]

    def _scrape_driver_listings(self, data, path):
        res = DriverListingScraper(self.base_url).run(path).data.get()
        data += res["items"]
        if self.pro_mode() and res["next_page"] is not None:
            self._scrape_driver_listings(data, res["next_page"])
