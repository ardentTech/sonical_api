from django.core.management.base import BaseCommand

from dealers.factories import DealerFactory


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        DealerFactory.create(
            name="Parts Express", website="https://www.parts-express.com")
        print("ALL DONE!")
