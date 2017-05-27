import logging
import time

from django.core.management.base import BaseCommand

from dealers.models import DealerScraper, DealerScraperReport
from drivers.models import Driver, DriverProductListing
from manufacturing.models import Manufacturer, Material


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "Synchronizes local and remote dealer data"

    def __init__(self, *args, **kwargs):
        self.driver_product_listings = self._setup_driver_product_listings()
        self.manufacturers = self._setup_manufacturers()
        self.materials = self._setup_materials()
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        try:
            for scraper in DealerScraper.objects.filter(is_active=True):
                start_time = time.time()
                to_create = []
                to_update = []
                self.report = DealerScraperReport(scraper=scraper)
                for listing in scraper.setup().scrape_driver_listings():
                    key = scraper.dealer.website + listing["path"]
                    if key not in self.driver_product_listings:
                        to_create.append({
                            "driver": scraper.setup().scrape_driver(listing["path"]),
                            "listing": listing})
                    else:
                        listing["url"] = key
                        to_update.append(listing)
                self._create_records(to_create, scraper.dealer)
                self._update_listings(to_update)
                self.report.execution_time = round(time.time() - start_time)
                self.report.save()
        except Exception as e:
            logger.exception(repr(e))

    def _create_records(self, records, dealer):
        new_drivers = Driver.objects.bulk_create(
            [self._format_driver(r["driver"]) for r in records])
        self.report.drivers_created = len(new_drivers)
        listings = [self._format_driver_product_listing(
            r["listing"], new_drivers[id], dealer) for id, r in enumerate(records)]
        new_listings = DriverProductListing.objects.bulk_create(listings)
        self.report.driver_product_listings_created = len(new_listings)

    def _format_driver(self, driver):
        self._set_manufacturer(driver)
        self._set_materials(driver)
        return Driver(**driver)

    def _format_driver_product_listing(self, listing, driver, dealer):
        listing["driver"] = driver
        listing["dealer"] = dealer
        return DriverProductListing(**listing)

    def _get_manufacturer(self, name):
        if name and name not in self.manufacturers:
            m = Manufacturer.objects.create(name=name)
            self.manufacturers[name] = m
            self.report.manufacturers_created += 1
        return self.manufacturers[name]

    def _get_material(self, name):
        if name and name not in self.materials:
            m = Material.objects.create(name=name)
            self.materials[name] = m
            self.report.materials_created += 1
        return self.materials[name]

    def _set_manufacturer(self, driver):
        driver["manufacturer"] = self._get_manufacturer(driver["manufacturer"])

    def _set_materials(self, driver):
        for m in ["basket_frame", "cone", "magnet", "surround", "voice_coil_former", "voice_coil_wire"]:
            if m in driver:
                driver[m] = self._get_material(driver[m])

    def _setup_driver_product_listings(self):
        return {dpl.url: dpl for dpl in DriverProductListing.objects.all()}

    def _setup_manufacturers(self):
        return {m.name: m for m in Manufacturer.objects.all()}

    def _setup_materials(self):
        return {m.name: m for m in Material.objects.all()}

    def _update_listings(self, listings):
        for listing in listings:
            dpl = self.driver_product_listings[listing["url"]]
            if dpl.price != listing["price"]:
                dpl.price = listing["price"]
                dpl.save()  # @todo use a bulk_update eventually
                self.report.driver_product_listings_updated += 1
