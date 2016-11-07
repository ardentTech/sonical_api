import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from drivers.factories import DriverFactory
from manufacturing.factories import ManufacturerFactory


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.manufacturers = {}
        self.materials = {}
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        self._create_manufacturers()
        self._create_drivers()
        print("ALL DONE!")

    def _create_drivers(self):
        file_path = os.path.join(settings.BASE_DIR, "drivers", "seed", "drivers.json")
        drivers = self._read_json_data(file_path)
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
        file_path = os.path.join(
            settings.BASE_DIR, "manufacturing", "seed", "manufacturers.json")
        manufacturers = self._read_json_data(file_path)
        generator = (manufacturer["fields"] for manufacturer in manufacturers)

        for m in generator:
            manufacturer = ManufacturerFactory.create(
                name=m["name"], website=m["website"])
            self.manufacturers[manufacturer.id] = manufacturer

        print("created {0} manufacturers".format(len(manufacturers)))

    def _read_json_data(self, file_path):
        data = []
        with open(file_path) as file_data:
            data = json.load(file_data)
        return data
