from decimal import Decimal
import re
from time import sleep

from bulk_update.helper import bulk_update
from lxml import html
import requests

from dealers.models import DealerScraperReport
from drivers.models import Driver, DriverProductListing
from manufacturing.models import Manufacturer, Material
from utils.mixins.mode import ModeMixin


# @todo what if PE is down?


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
        self.db_record = scraper_record
        self.dealer = self.db_record.dealer
        self.base_url = self.dealer.website

        self.driver_product_listings = {
            l.path: l for l in DriverProductListing.objects.filter(dealer=self.dealer)}


class RecordProcessor(object):

    # @todo should the app have a big file of these constants?
    CREATE = "create"
    DRIVERS = "drivers"
    LISTINGS = "listings"
    MANUFACTURERS = "manufacturers"
    MATERIALS = "materials"
    UPDATE = "update"
    RECORD_METHODS = [CREATE, UPDATE]
    RECORD_TYPES = [DRIVERS, LISTINGS, MANUFACTURERS, MATERIALS]

    def __init__(self, dealer):
        self.dealer = dealer
        self.errors = []
        self.manufacturers = {m.name: m for m in Manufacturer.objects.all()}
        self.materials = {m.name: m for m in Material.objects.all()}
        # @todo should container be a nested class that inherits from dict?
        self.processed = self._get_container()
        self.unprocessed = self._get_container()

    def process(self):
        self._process_drivers()
        self._process_listings()
        return {
            "drivers_created": len(self._drivers_created()),
            "driver_product_listings_created": len(self._listings_created()),
            "driver_product_listings_updated": len(self._listings_updated()),
            "manufacturers_created": len(self._manufacturers_created()),
            "materials_created": len(self._materials_created()),
            "errors": len(self.errors)}

    def queue_driver(self, record):
        self._queue_record(self.DRIVERS, record, False)

    def queue_listing(self, record, update=False):
        self._queue_record(self.LISTINGS, record, update)

    # @todo should these be getters/setters?
    def _drivers_created(self):
        return self.processed[self.DRIVERS][self.CREATE]

    def _drivers_to_create(self):
        return self.unprocessed[self.DRIVERS][self.CREATE]

    def _format_driver(self, attrs):
        attrs["manufacturer"] = self._get_or_create(
            Manufacturer, attrs["manufacturer"])
        for item in [
                "basket_frame", "cone", "magnet",
                "surround", "voice_coil_former", "voice_coil_wire"]:
            if item in attrs:
                attrs[item] = self._get_or_create(
                    Material, attrs[item])
        return Driver(**attrs)

    def _get_container(self):
        container = {}
        for _type in self.RECORD_TYPES:
            container[_type] = {method: [] for method in self.RECORD_METHODS}
        return container

    def _get_or_create(self, cls, name):
        key = cls.__name__.lower() + "s"
        records = getattr(self, key)
        try:
            return records[name]
        except:
            new_obj = cls.objects.create(name=name)
            records[name] = new_obj
            self.processed[key][self.CREATE].append(new_obj)
            return records[name]

    def _listings_created(self):
        return self.processed[self.LISTINGS][self.CREATE]

    def _listings_updated(self):
        return self.processed[self.LISTINGS][self.UPDATE]

    def _listings_to_create(self):
        return self.unprocessed[self.LISTINGS][self.CREATE]

    def _listings_to_update(self):
        return self.unprocessed[self.LISTINGS][self.UPDATE]

    def _manufacturers_created(self):
        return self.processed[self.MANUFACTURERS][self.CREATE]

    def _materials_created(self):
        return self.processed[self.MATERIALS][self.CREATE]

    def _process_drivers(self):
        try:
            # @todo update manufacturer and materials here
            _drivers = list(map(
                self._format_driver, self._drivers_to_create()))
            self.processed[self.DRIVERS][self.CREATE] = Driver.objects.bulk_create(
                _drivers)
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


# @todo try/except in each _scrape method
class PartsExpressScraper(DealerScraper):

    SEED = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"

    def __init__(self, scraper_record):
        super(PartsExpressScraper, self).__init__(scraper_record)
        self.limit = None if self.pro_mode() else 1
        self.record_processor = RecordProcessor(self.dealer)

    def run(self):
        for category_path in self._scrape_category_paths(self.SEED, self.limit):
            # @todo handle next_path
            listings, next_path = self._scrape_listings(category_path, self.limit)
            for listing in listings:
                existing_listing = self.driver_product_listings.get(
                    listing["path"], None)
                if existing_listing is not None:  # update listing
                    existing_listing.price = listing["price"]
                    self.record_processor.queue_listing(existing_listing, True)
                else:  # create driver and listing
                    self.record_processor.queue_driver(
                        self._scrape_driver(listing["path"]))
                    self.record_processor.queue_listing(listing)

        self._create_report(self.record_processor.process())

    def _create_report(self, result):
        result["scraper"] = self.db_record
        DealerScraperReport.objects.create(**result)

    def _scrape_category_paths(self, path, limit):
        patterns = {"DRIVER_CATEGORY": '//a[@id="lbCategoryName"]/@href'}
        categories = self.get_html(
            self.build_url(path)).xpath(patterns["DRIVER_CATEGORY"])

        return [c for c in categories if not re.search(r"replace|recone", c)][:limit]

    def _scrape_driver(self, path):
        patterns = [
            # @todo make this structure more readable (@see listings below)
            ('//div[@id="MiddleColumn1"]', [
                ("model", 'h1[@class="ProductTitle"]/span/text()', "")
            ]),
            ('//div[@class="ProducDetailsNote"]', [
                # (key, table row column one text, formatter)
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
                ("voice_coil_wire", "Voice Coil Wire Material", None),
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

        # @todo need a cleaner way to do this type of thing
        data["model"] = data["model"].lstrip("{0}".format(data["manufacturer"]))

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
