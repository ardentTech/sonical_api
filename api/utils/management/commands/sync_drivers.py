from django.core.management.base import BaseCommand

from drivers.scrapers import PartsExpress


class Command(BaseCommand):

    help_text = ""

    def handle(self, *args, **kwargs):
        PartsExpress().run()
