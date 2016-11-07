import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from drivers.factories import DriverFactory
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
        drivers = []
        path = os.path.join(settings.BASE_DIR, "drivers", "seed", "drivers.json")

        with open(path) as data:
            drivers = json.load(data)

        generator = (driver["fields"] for driver in drivers)
        for d in generator:
            DriverFactory.create(
                model=d["model"],
                manufacturer=self.manufacturers[d["manufacturer"]],
                nominal_diameter=d["nominal_diameter"],
                in_production=d["in_production"],
                max_power=d["max_power"],
                nominal_impedance=d["nominal_impedance"],
                resonant_frequency=d["resonant_frequency"],
                rms_power=d["rms_power"],
                sensitivity=d["sensitivity"],
            )

        print("created {0} drivers".format(len(drivers)))

    def _create_manufacturers(self):
        for m in MANUFACTURERS:
            manufacturer = ManufacturerFactory.create(name=m[0], website=m[1])
            self.manufacturers[manufacturer.id] = manufacturer

        print("created {0} manufacturers".format(len(MANUFACTURERS)))

    def _create_materials(self):
        for m in MATERIALS:
            self.materials[m[0]] = MaterialFactory.create(name=m[0])

        print("created {0} materials".format(len(MATERIALS)))
