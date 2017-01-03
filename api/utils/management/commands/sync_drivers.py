from django.core.management.base import BaseCommand

from drivers.models import Driver
from drivers.scrapers import PartsExpressScraper
from manufacturing.models import Manufacturer
from utils.mixins.mode import ModeMixin


# @todo associate a manufacturer to a driver
# @todo how to efficiently create/update driver records?
# @todo create/update product listing
# @todo i think i need to pass the existing product listings to the appropriate
#   scraper. the scraper (parts express) can then determine whether or not it
#   should fetch driver details or merely scrape the price


class Command(ModeMixin, BaseCommand):

    help = "Synchs local driver records with their remotes"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.manufacturers = {m.name: m for m in Manufacturer.objects.all()}

    def handle(self, *args, **kwargs):
        self._scrape_parts_express()

    def _scrape_parts_express(self):
        results = PartsExpressScraper().run()
        # @todo create scraping report here

        if self.pro_mode():
            Driver.objects.bulk_create(
                [self._expand_attrs(driver) for driver in results["successes"]])
        else:
            print("Successes: {0}".format(len(results["successes"])))
            print("Failures: {0}".format(len(results["failures"])))

    def _expand_attrs(self, driver):
        # @todo separated associated product listing price
        key = "manufacturer"
        name = driver[key]
        try:
            driver[key] = self.manufacturers[name]
        except:
            self.manufacturers[name] = Manufacturer.objects.create(name=name)
            driver[key] = self.manufacturers[name]
        return driver
