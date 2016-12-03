from django.core.management.base import BaseCommand

from drivers.scrapers import PartsExpressScraper
from manufacturing.models import Manufacturer


class Command(BaseCommand):

    help_text = ""

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.manufacturers = {m.name: m for m in Manufacturer.objects.all()}

    def handle(self, *args, **kwargs):
        drivers = PartsExpressScraper().run()
        for d in drivers:
            print("{0}".format(d))
