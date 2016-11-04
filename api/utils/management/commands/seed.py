from django.core.management.base import BaseCommand

from manufacturing.factories import ManufacturerFactory, MaterialFactory
from manufacturing.seed_data import MANUFACTURERS, MATERIALS


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.manufacturers = {}
        self.materials = {}
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        self._create_manufacturers()
        self._create_materials()
        print("ALL DONE!")

    def _create_manufacturers(self):
        for m in MANUFACTURERS:
            self.manufacturers[m[0]] = ManufacturerFactory.create(
                name=m[0], website=m[1])

        print("created {0} manufacturers".format(len(MANUFACTURERS)))

    def _create_materials(self):
        for m in MATERIALS:
            self.materials[m[0]] = MaterialFactory.create(name=m[0])

        print("created {0} materials".format(len(MATERIALS)))
