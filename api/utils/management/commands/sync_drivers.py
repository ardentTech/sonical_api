from django.core.management.base import BaseCommand

from drivers.models import Driver, DriverProductListing
from drivers.scrapers import PartsExpressScraper
from manufacturing.models import Manufacturer
from products.models import Dealer
from utils.mixins.mode import ModeMixin


# @todo how to efficiently create/update driver records?
# @todo create/update product listing
# @todo i think i need to pass the existing product listings to the appropriate
#   scraper. the scraper (parts express) can then determine whether or not it
#   should fetch driver details or merely scrape the price


class Command(ModeMixin, BaseCommand):

    help = "Synchronizes local and remote driver data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.manufacturers = {m.name: m for m in Manufacturer.objects.all()}

    def handle(self, *args, **kwargs):
        scrapers = [PartsExpressScraper()]
        for scraper in scrapers:
            self._process_result(scraper.run())

    def _get_manufacturer(self, name):
        try:
            return self.manufacturers[name]
        except:
            self.manufacturers[name] = Manufacturer.objects.create(name=name)
            return self.manufacturers[name]

    def _process_result(self, result):
        dealer, created = Dealer.objects.get_or_create(name="Parts Express")

        if self.dev_mode():  # @todo change dev to pro
            to_create = []
            listing_attrs = []
            for data in result["successes"]:
                data["manufacturer"] = self._get_manufacturer(data["manufacturer"])
                listing_attrs.append({
                    "path": data.pop("path", None),
                    "price": data.pop("price", None)})
                to_create.append(Driver(**data))

            created = Driver.objects.bulk_create(to_create)

            del to_create[:]
            for idx, driver in enumerate(created):
                attrs = listing_attrs[idx]
                attrs["dealer"] = dealer
                attrs["driver"] = driver
                to_create.append(DriverProductListing(**attrs))

            DriverProductListing.objects.bulk_create(to_create)
