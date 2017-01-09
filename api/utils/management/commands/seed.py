from django.core.management.base import BaseCommand

from dealers.factories import DealerFactory, DealerScraperFactory


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        dealers = [("Parts Express", "https://www.parts-express.com")]
        for dealer in dealers:
            d = DealerFactory.create(name=dealer[0], website=dealer[1])
            DealerScraperFactory.create(dealer=d)
        print("Created {0} Dealer(s)".format(len(dealers)))
        print("Created {0} DealerScraper(s)".format(len(dealers)))
