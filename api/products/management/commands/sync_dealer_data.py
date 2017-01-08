from django.core.management.base import BaseCommand

# from dealers.models import DealerScraper
from utils.mixins.mode import ModeMixin


class Command(ModeMixin, BaseCommand):

    help = "Synchronizes local and remote dealer data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        pass
