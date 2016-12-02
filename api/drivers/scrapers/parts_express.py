from decimal import Decimal
import re

from lxml import html
import requests

from drivers.factories import DriverFactory
from drivers.models import Driver
from manufacturing.models import Manufacturer


# @todo create a report each time this is run?


# this is happy path and based upon all fields being present and an expected
# order in the DOM. problematic. would work better if matching against the row
# title, and then grabbing the following <span> tag's value...
DC_RESISTANCE = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[2]/span[2]/text()'
DRIVER_CATEGORIES_PATH = '/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13'
DRIVER_CATEGORY_XPATH = '//a[@id="lbCategoryName"]/@href'
DRIVER_DETAIL_XPATH = '//a[@id="GridViewProdLink"]/@href'
ELECTROMAGNETIC_Q = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[7]/span[2]/text()'
HOST = "www.parts-express.com"
MANUFACTURER = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[1]/span[2]/text()'
MAX_POWER = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[4]/span[2]/text()'
MECHANICAL_Q = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[5]/span[2]/text()'
MODEL = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[6]/ul/li[2]/span[2]/text()'
NEXT_PAGE_XPATH = '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]/@href'
NOMINAL_DIAMETER = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[1]/span[2]/text()'
NOMINAL_IMPEDANCE = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[5]/span[2]/text()'
PROTOCOL = "https://"
RESONANT_FREQUENCY = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[1]/span[2]/text()'
RMS_POWER = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[2]/span[2]/text()'
SENSITIVITY = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[1]/ul/li[8]/span[2]/text()'
VOICE_COIL_INDUCTANCE = '//*[@id="ctl00_ctl00_MainContent_uxProduct_pnlProductDetails"]/div[2]/div[3]/div[2]/ul/li[4]/span[2]/text()'

# @todo add ability to only scrape one category at a time?


class PartsExpress(object):

    def __init__(self):
        self.data_store = {}
        self.manufacturers = {m.name: m for m in Manufacturer.objects.all()}

    # @todo handle each category on a different thread
    def run(self):
        categories = self._get_categories()
        for category in categories:
            data_store = self.data_store.setdefault(category[0], [])
            self._get_drivers(category[1], data_store)
            self._create_drivers(data_store)

    def _build_url(self, path):
        return PROTOCOL + HOST + path

    def _create_driver(self, attrs):
        name = attrs["manufacturer"]
        try:
            attrs["manufacturer"] = self.manufacturers[name]
        except:
            self.manufacturers[name] = Manufacturer.objects.create(name=name)
            attrs["manufacturer"] = self.manufacturers[name]

        print("Creating {0}".format(attrs))
        DriverFactory.create(**attrs)
#        print("Created {0} {1}".format(attrs["manufacturer"], attrs["model"]))

    def _create_drivers(self, store):
        for path in store:
            url = self._build_url(path)
            driver = Driver.objects.filter(data_source=url)
            if not driver:
                self._create_driver(self._get_driver_attrs(url))

    def _get_categories(self):
        page = requests.get(self._build_url(DRIVER_CATEGORIES_PATH))
        tree = html.fromstring(page.content)
        paths = tree.xpath(DRIVER_CATEGORY_XPATH)
        return [
            (p.split("/")[2], p) for p in paths if not re.search(r'replace|recone', p)]

    def _get_driver_attrs(self, url):
        attrs = {}

        page = requests.get(url)
        tree = html.fromstring(page.content)

        # @todo this is so error prone bc PE doesn't use IDs...
        # need to use basic regex searches for units, etc. to at least try
        # to get sanitary data
        # @todo need to remove units, white space, etc.
        # (model field name, xpath pattern, regex patter) ?
        attrs["dc_resistance"] = self._sanitize_resistance(
            tree.xpath(DC_RESISTANCE)[0])
        attrs["electromagnetic_q"] = tree.xpath(ELECTROMAGNETIC_Q)[0]
        attrs["manufacturer"] = tree.xpath(MANUFACTURER)[0]
        attrs["max_power"] = self._sanitize_power(tree.xpath(MAX_POWER)[0])
        attrs["mechanical_q"] = tree.xpath(MECHANICAL_Q)[0]
        attrs["model"] = tree.xpath(MODEL)[0]
        attrs["nominal_diameter"] = self._sanitize_nominal_diameter(
            tree.xpath(NOMINAL_DIAMETER)[0])
        attrs["nominal_impedance"] = self._sanitize_resistance(
            tree.xpath(NOMINAL_IMPEDANCE)[0])
        attrs["resonant_frequency"] = self._sanitize_resonant_frequency(
            tree.xpath(RESONANT_FREQUENCY)[0])
        attrs["rms_power"] = self._sanitize_power(tree.xpath(RMS_POWER)[0])
        attrs["sensitivity"] = self._sanitize_sensitivity(
            tree.xpath(SENSITIVITY)[0])
        attrs["voice_coil_inductance"] = self._sanitize_inductance(
            tree.xpath(VOICE_COIL_INDUCTANCE)[0])

        return attrs

    def _get_drivers(self, path, store):
        page = requests.get(self._build_url(path))
        tree = html.fromstring(page.content)

        for driver in tree.xpath(DRIVER_DETAIL_XPATH):
            store.append(driver)

        try:  # go to next drivers page if exists
            next_path = tree.xpath(NEXT_PAGE_XPATH)[0]
            self._get_drivers(next_path, store)
        except IndexError:  # no next_path was found
            return
        except Exception as e:
            print("Unexpected Exception: {0}".format(e))

    def _sanitize_sensitivity(self, val):
        return Decimal(val.split(" ")[0])

    def _sanitize_resistance(self, val):
        return Decimal(val.split(" ")[0])

    def _sanitize_inductance(self, val):
        return Decimal(val.split(" ")[0])

    def _sanitize_nominal_diameter(self, val):
        parts = val.rstrip('"').split("-")
        integer_part = Decimal(parts[0])
        fraction_part = Decimal(0)

        if len(parts) > 1:
            fractional_parts = parts[1].split("/")
            fraction_part = Decimal(fractional_parts[0]) / Decimal(fractional_parts[1])

        return integer_part + fraction_part

    def _sanitize_power(self, val):
        return int(val.split(" ")[0])

    def _sanitize_resonant_frequency(self, val):
        return Decimal(val.split(" ")[0])
