from decimal import Decimal
import re
from time import sleep

from bulk_update.helper import bulk_update
from lxml import html
import requests

from dealers.models import DealerScraperReport
from drivers.models import Driver, DriverProductListing
from manufacturing.models import Manufacturer
from utils.mixins.mode import ModeMixin


# @todo update records
# @todo get driver.model from price section at top
# @todo try/except in each _scrape method
# @todo detect if no records are in database, and enter in a different
# insert-only type mode


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
        self.dealer = scraper_record.dealer
        self.base_url = self.dealer.website
        self.manufacturers = {m.name: m for m in Manufacturer.objects.all()}
        self.driver_product_listings = {
            l.path: l for l in DriverProductListing.objects.filter(dealer=self.dealer)}
        self.db_record = scraper_record


class RecordProcessor(object):

    CREATE = "create"
    DRIVERS = "drivers"
    LISTINGS = "listings"
    UPDATE = "update"
    RECORD_METHODS = [CREATE, UPDATE]
    RECORD_TYPES = [DRIVERS, LISTINGS]

    def __init__(self, dealer):
        self.dealer = dealer
        self.errors = []
        # @todo should container be a nested class?
        self.processed = self._get_container()
        self.unprocessed = self._get_container()

    def process(self):
        self._process_drivers()
        self._process_listings()
        return {
            "drivers_created": len(self._drivers_created()),
            "driver_product_listings_created": len(self._listings_created()),
            "driver_product_listings_updated": len(self._listings_updated()),
            "errors": len(self.errors)}

    def queue_driver(self, record):
        self._queue_record(self.DRIVERS, record, False)

    def queue_listing(self, record, update=False):
        self._queue_record(self.LISTINGS, record, update)

    def _get_container(self):
        container = {}
        for _type in self.RECORD_TYPES:
            container[_type] = {method: [] for method in self.RECORD_METHODS}
        return container

    # @todo should these be getters/setters?
    def _drivers_created(self):
        return self.processed[self.DRIVERS][self.CREATE]

    def _drivers_to_create(self):
        return self.unprocessed[self.DRIVERS][self.CREATE]

    def _listings_created(self):
        return self.processed[self.LISTINGS][self.CREATE]

    def _listings_updated(self):
        return self.processed[self.LISTINGS][self.UPDATE]

    def _listings_to_create(self):
        return self.unprocessed[self.LISTINGS][self.CREATE]

    def _listings_to_update(self):
        return self.unprocessed[self.LISTINGS][self.UPDATE]

    def _process_drivers(self):
        try:
            self.processed[self.DRIVERS][self.CREATE] = Driver.objects.bulk_create(
                self._drivers_to_create())
        except Exception as e:
            self.errors.append("_process_drivers(): " + repr(e))

    def _process_listings(self):
        self._process_listings_create()
        self._process_listings_update()

    def _process_listings_create(self):
        try:
            _listings = []
            for idx, item in enumerate(self._listings_to_create()):
                item["dealer"] = self.dealer
                item["driver"] = self._drivers_created()[idx]
                item["price"] = Decimal(item["price"].__str__().lstrip("$"))
                _listings.append(DriverProductListing(**item))

            if _listings:
                self.processed[self.LISTINGS][self.CREATE] = DriverProductListing.objects.bulk_create(
                    _listings)
        except Exception as e:
            self.errors.append("_process_listings_create(): " + repr(e))

    def _process_listings_update(self):
        try:
            if self._listings_to_update():
                self.processed[self.LISTINGS][self.UPDATE] = bulk_update(
                    self._listings_to_update, update_fields=["price"])
        except Exception as e:
            self.errors.append("_process_listings_update(): " + repr(e))

    def _queue_record(self, _type, record, update):
        method = self.UPDATE if update else self.CREATE
        self.unprocessed[_type][method].append(record)


class PartsExpressScraper(DealerScraper):

    SEED = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def __init__(self, scraper_record):
        super(PartsExpressScraper, self).__init__(scraper_record)
        self.record_processor = RecordProcessor(self.dealer)

    def run(self):
        limit = self._get_limit()

        for category_path in self._scrape_category_paths(self.SEED, limit):
            # @todo handle next_path
            listings, next_path = self._scrape_listings(category_path, limit)
            for listing in listings:
                existing_listing = self.driver_product_listings.get(
                    listing["path"], None)
                if existing_listing is not None:
                    existing_listing.price = listing["price"]
                    self.record_processor.queue_listing(existing_listing, True)
                else:
                    self.record_processor.queue_driver(
                        Driver(**self._scrape_driver(listing["path"])))
                    self.record_processor.queue_listing(listing)

        self._create_report(self.record_processor.process())

    def _get_limit(self):
        return None if self.pro_mode() else 1

    def _create_report(self, result):
        result["scraper"] = self.db_record
        report = DealerScraperReport.objects.create(**result)
        print("{0}".format(report.__dict__))

    def _scrape_category_paths(self, path, limit):
        patterns = {"DRIVER_CATEGORY": '//a[@id="lbCategoryName"]/@href'}
        categories = self.get_html(
            self.build_url(path)).xpath(patterns["DRIVER_CATEGORY"])

        return [c for c in categories if not re.search(r"replace|recone", c)][:limit]

    def _scrape_driver(self, path):
        patterns = [
            # @todo make this structure more readable (@see listings below)
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
                    val = root.xpath(".//" + pattern.format(items[1]))[0]
                    if items[2]:
                        val = getattr(self, "_to_" + items[2])(val)
                    data[items[0]] = val
                except:
                    pass

        return data

    def _scrape_listings(self, path, limit):
        patterns = {
            "next_page": '//a[@id="ctl00_ctl00_MainContent_uxEBCategory_uxEBProductList_uxBottomPagingLinks_aNextNav"]',
            "listing": {
                "root": '//a[@id="GridViewProdLink"]',
                "path": './/@href',
                "price": './/div[@class="CatPriceSection"]/div/div/span[2]/text()',
            }
        }
        tree = self.get_html(self.build_url(path))
        listings = tree.xpath(patterns["listing"]["root"])
        data = []

        for listing in listings:
            data.append({
                "path": listing.xpath(patterns["listing"]["path"])[0],
                "price": listing.xpath(patterns["listing"]["price"])[0]
            })

        next_page = None
        if limit is None:
            try:
                next_page = tree.xpath(patterns["next_page"])[0]
            except IndexError:
                pass

        return (data, next_page)

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
