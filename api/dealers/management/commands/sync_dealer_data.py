from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Synchronizes local and remote dealer data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        pass
