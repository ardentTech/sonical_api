import os

from django.core.management.base import BaseCommand

from dealers.factories import DealerFactory, DealerScraperFactory


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        dealers = []
        for dealer in [("Parts Express", "https://www.parts-express.com")]:
            dealers.append(DealerFactory.create(name=dealer[0], website=dealer[1]))
        print("Created {0} Dealer(s)".format(len(dealers)))

        dealer_scrapers = []
        for dealer in dealers:
            file_path = os.path.join(
                "dealers", "scrapers", dealer.name.lower().replace(" ", "_") + ".py")
            dealer_scrapers.append(DealerScraperFactory.create(
                dealer=dealer, file_path=file_path))
        print("Created {0} DealerScraper(s)".format(len(dealer_scrapers)))
