import json

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from .factories import DriverFactory
from manufacturing.factories import ManufacturerFactory


class DriverListTestCase(APITestCase):

    def test_get_list_ok(self):
        for i in range(3):
            DriverFactory.create()

        response = self.client.get(reverse("api:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 3)


class DriverListSearchTestCase(APITestCase):

    def test_get_list_search_model_ok(self):
        DriverFactory.create(model="Alpair 6M")
        DriverFactory.create(model="Pluvia Eleven")

        response = self.client.get(
            reverse("api:driver-list") + "?search=pluv")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)


class DriverListFilterTestCase(APITestCase):

    def test_get_list_filter_in_production_ok(self):
        DriverFactory.create(in_production=True)
        DriverFactory.create(in_production=False)

        # @todo find a way to use lowercase 'true' in query param
        response = self.client.get(
            reverse("api:driver-list") + "?in_production=True")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)

    def test_get_list_filter_manufacturer_ok(self):
        dayton_audio = ManufacturerFactory.create(name="Dayton Audio")
        markaudio = ManufacturerFactory.create(name="MarkAudio")
        DriverFactory.create(manufacturer=dayton_audio)
        DriverFactory.create(manufacturer=markaudio)

        response = self.client.get(
            reverse("api:driver-list") + "?manufacturer=MarkAudio")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)

    def test_get_list_filter_max_power_ok(self):
        DriverFactory.create(max_power=60)
        DriverFactory.create(max_power=50)

        response = self.client.get(
            reverse("api:driver-list") + "?max_power=60")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)

    def test_get_list_filter_model_ok(self):
        DriverFactory.create(model="Pluvia")
        DriverFactory.create(model="Testing")

        # @todo this is exact and case-sensitive. loosen those restrictions.
        response = self.client.get(
            reverse("api:driver-list") + "?model=Testing")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)

    def test_get_list_filter_nominal_diameter_ok(self):
        DriverFactory.create(nominal_diameter=4)
        DriverFactory.create(nominal_diameter=5)

        response = self.client.get(
            reverse("api:driver-list") + "?nominal_diameter=5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)

    def test_get_list_filter_nominal_impedance_ok(self):
        DriverFactory.create(nominal_impedance=4)
        DriverFactory.create(nominal_impedance=8)

        response = self.client.get(
            reverse("api:driver-list") + "?nominal_impedance=4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)

    def test_get_list_filter_resonant_frequency_ok(self):
        DriverFactory.create(resonant_frequency=120)
        DriverFactory.create(resonant_frequency=80)

        response = self.client.get(
            reverse("api:driver-list") + "?resonant_frequency=80")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)

    def test_get_list_filter_rms_power_ok(self):
        DriverFactory.create(rms_power=60)
        DriverFactory.create(rms_power=100)

        response = self.client.get(
            reverse("api:driver-list") + "?rms_power=100")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)

    def test_get_list_filter_sensitivity_ok(self):
        DriverFactory.create(sensitivity=90.1)
        DriverFactory.create(sensitivity=88)

        response = self.client.get(
            reverse("api:driver-list") + "?sensitivity=90.1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)
