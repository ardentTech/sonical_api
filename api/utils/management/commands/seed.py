from django.core.management.base import BaseCommand

from dealers.factories import DealerFactory, DealerScraperFactory
from users.factories import UserFactory


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        UserFactory.create(
            email="jonathan@ardent.tech", is_staff=True, is_superuser=True)

        dealers = []
        for dealer in [("Parts Express", "https://www.parts-express.com")]:
            dealers.append(DealerFactory.create(name=dealer[0], website=dealer[1]))
        self.stdout.write("Created {0} Dealer(s)".format(len(dealers)))

        dealer_scrapers = []
        for dealer in dealers:
            dealer_scrapers.append(DealerScraperFactory.create(
                class_name="PartsExpressScraper", dealer=dealer))
        self.stdout.write("Created {0} DealerScraper(s)".format(len(dealer_scrapers)))
