from django.core.management.base import BaseCommand

from drivers.models import Driver
from drivers.scrapers import PartsExpressScraper
from manufacturing.models import Manufacturer


# @todo need a mode here. should it be handled here and then passed to all
# scrapers?
# @todo if driver already exists (check `data_source` attr), do not create it on 22
# @todo driver["price"] belongs to the DriverProductListing and not the Driver


class Command(BaseCommand):

    help = "Synchs local driver records with their remotes"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.drivers = Driver.objects.values_list("data_source", flat=True)
        self.manufacturers = {m.name: m for m in Manufacturer.objects.all()}

    def handle(self, *args, **kwargs):
        drivers = PartsExpressScraper().run()
        print("{0}".format([self._expand_attrs(d) for d in drivers]))
#        Driver.objects.bulk_create([self._expand_attrs(d) for d in drivers])

    def _expand_attrs(self, driver):
        name = driver["manufacturer"]
        try:
            driver["manufacturer"] = self.manufacturers[name]
        except:
            self.manufacturers[name] = Manufacturer.objects.create(name=name)
            driver["manufacturer"] = self.manufacturers[name]
        return driver
