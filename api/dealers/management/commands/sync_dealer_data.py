# from decimal import Decimal

from django.core.management.base import BaseCommand

from dealers.models import DealerScraper
from drivers.models import Driver, DriverProductListing
from manufacturing.models import Manufacturer, Material


class Command(BaseCommand):

    help = "Synchronizes local and remote dealer data"

    def __init__(self, *args, **kwargs):
        self.driver_product_listings = self._setup_driver_product_listings()
        self.manufacturers = self._setup_manufacturers()
        self.materials = self._setup_materials()
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        to_create = []
        for scraper in DealerScraper.objects.filter(is_active=True):
            for listing in scraper.setup().scrape_driver_listings():
                key = scraper.dealer.website + listing["path"]
                if key not in self.driver_product_listings:
                    driver = scraper.setup().scrape_driver(listing["path"])
                    self._set_manufacturer(driver)
                    self._set_materials(driver)
                    to_create.append({
                        "dealer": scraper.dealer, "driver": driver, "listing": listing})
        self._create_records(to_create)

    def _create_records(self, records):
        # create driver product listings
        Driver.objects.bulk_create([Driver(**r["driver"]) for r in records])

    def _get_manufacturer(self, name):
        if name and name not in self.manufacturers:
            m = Manufacturer.objects.create(name=name)
            self.manufacturers[name] = m
        return self.manufacturers[name]

    def _get_material(self, name):
        if name and name not in self.materials:
            m = Material.objects.create(name=name)
            self.materials[name] = m
        return self.materials[name]

    def _set_manufacturer(self, driver):
        driver["manufacturer"] = self._get_manufacturer(driver["manufacturer"])

    def _set_materials(self, driver):
        for m in ["basket_frame", "cone", "magnet", "surround", "voice_coil_former", "voice_coil_wire"]:
            if m in driver:
                driver[m] = self._get_material(driver[m])

    def _setup_driver_product_listings(self):
        return {dpl.url(): dpl for dpl in DriverProductListing.objects.all()}

    def _setup_manufacturers(self):
        return {m.name: m for m in Manufacturer.objects.all()}

    def _setup_materials(self):
        return {m.name: m for m in Material.objects.all()}
