from django.core.management.base import BaseCommand

from drivers.factories import DriverFactory
from drivers.seed_data import DRIVERS
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
        self._create_drivers()
        print("ALL DONE!")

    def _create_drivers(self):
        for d in DRIVERS:
            DriverFactory.create(
                model=d[0],
                manufacturer=self.manufacturers[d[1]],
                nominal_diameter=d[2],
                in_production=d[3],
                max_power=d[4],
                nominal_impedance=d[5],
                resonant_frequency=d[6],
                rms_power=d[7],
                sensitivity=d[8],
            )

        print("created {0} drivers".format(len(DRIVERS)))

    def _create_manufacturers(self):
        for m in MANUFACTURERS:
            self.manufacturers[m[0]] = ManufacturerFactory.create(
                name=m[0], website=m[1])

        print("created {0} manufacturers".format(len(MANUFACTURERS)))

    def _create_materials(self):
        for m in MATERIALS:
            self.materials[m[0]] = MaterialFactory.create(name=m[0])

        print("created {0} materials".format(len(MATERIALS)))
