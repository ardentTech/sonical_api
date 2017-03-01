from django.core.management.base import BaseCommand

from dealers.models import DealerScraper


class Command(BaseCommand):

    help = "Synchronizes local and remote dealer data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        scrapers = DealerScraper.objects.filter(is_active=True)
        for scraper in scrapers:
            res = scraper.run()
            print("{0}".format(res.keys()))
