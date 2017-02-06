import re
from time import sleep

from lxml import html
import requests


# @todo DriverScraper


class ScraperData(object):

    def __init__(self):
        self._data = {"items": []}

    def concat(self, key, data):
        self._data[key] += data

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

    PATTERNS = {
        "path": '//a[@id="lbCategoryName"]/@href'
    }

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
                # (django key, PE matcher, post_scrape)
                ("model", 'h1[@class="ProductTitle"]/span/text()', "")]
        },
        {
            "id": "details",
            "scope": '//div[@class="ProducDetailsNote"]',
            "base_pattern": 'span[text()="{0}"]/following-sibling::span[1]/text()',
            "items": [
                # (django key, PE matcher, post_scrape)
                ("basket_frame", "Basket / Frame Material", None),
                ("bl_product", "BL Product (BL)", "decimal"),
                ("compliance_equivalent_volume", "Compliance Equivalent Volume (Vas)", "decimal"),
                ("cone", "Cone Material", None),
                ("cone_surface_area", "Surface Area of Cone (Sd)", "decimal"),
                ("dc_resistance", "DC Resistance (Re)", "decimal"),
                ("diaphragm_mass_including_airload", "Diaphragm Mass Inc. Airload (Mms)", "diaphragm"),
                ("electromagnetic_q", "Electromagnetic Q (Qes)", "decimal"),
                ("frequency_response", "Frequency Response", "frequency_response"),
                ("magnet", "Magnet Material", None),
                ("manufacturer", "Brand", None),
                ("max_power", "Power Handling (max)", "int"),
                ("max_linear_excursion", "Maximum Linear Excursion (Xmax)", "decimal"),
                ("mechanical_compliance_of_suspension", "Mechanical Compliance of Suspension (Cms)", "decimal"),
                ("mechanical_q", "Mechanical Q (Qms)", "decimal"),
                ("nominal_diameter", "Nominal Diameter", "diameter"),
                ("nominal_impedance", "Impedance", "decimal"),
                ("resonant_frequency", "Resonant Frequency (Fs)", "decimal"),
                ("rms_power", "Power Handling (RMS)", "int"),
                ("sensitivity", "Sensitivity", "decimal"),
                ("surround", "Surround Material", None),
                ("voice_coil_diameter", "Voice Coil Diameter", "diameter"),
                ("voice_coil_former", "Voice Coil Former", None),
                ("voice_coil_inductance", "Voice Coil Inductance (Le)", "decimal"),
                ("voice_coil_wire", "Voice Coil Wire Material", None)]
        }
    ]

    def run(self, path):
        tree = self.get_html(path)

        for section in self.PATTERNS:
            scope = tree.xpath(section["scope"])[0]
            for items in section["items"]:
                try:
                    val = scope.xpath(".//" + section["pattern"].format(items[1]))[0]
                    if items[2]:
#                        val = getattr(self, "_to_" + items[2])(val)
                        print("run post_scrape")
                    self.data.set(items[0], val)
                except:
                    pass
#    data["model"] = data["model"].lstrip("{0}".format(data["manufacturer"]))


class DriverListingScraper(PathScraper):

    PATTERNS = {
        "next_page": '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href',
        "listing": {
            "scope": '//a[@id="GridViewProdLink"]',
            "path": './/@href',
            "price": './/div[@class="CatPriceSection"]/div/div/span[2]/text()',
        }
    }

    def run(self, path):
        tree = self.get_html(path)
        for listing in tree.xpath(self.PATTERNS["listing"]["scope"]):
            self.data.concat("items", {
                "path": listing.xpath(self.PATTERNS["listing"]["path"])[0],
                "price": listing.xpath(self.PATTERNS["listing"]["price"])[0]
            })
        try:
            self.data.set("next_page", tree.xpath(self.PATTERNS["next_page"])[0])
        except IndexError:
            pass
        return self


class PartsExpressScraper(DealerScraper):

    SEED = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def run(self):
        self._scrape_categories(self.SEED)
        print("{0}".format(self.data.get()))

    def _scrape_categories(self, path):
        self.data.set("items", CategoryScraper(
            self.base_url).run(path).data.get()["items"])

#    def _get_driver_listings(self, path):
#        res = DriverListingScraper(self.base_url).run(path).get_data()
#        next_page = res.pop("next_page", None)
#        self.DATA["driver_listings"] + [{} for path, price in res.items()]
#        try:
#            self.data.set(
#                "driver_listings", self.get_data("driver_listings") + res)
#        except KeyError:
#            self.data.set("driver_listings", res)
#
#        # handle pagination
#        if next_page is not None:
#            self._get_driver_listings(next_page)
