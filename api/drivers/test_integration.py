import json

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from .factories import DriverFactory


class DriverListTestCase(APITestCase):

    def test_get_list_ok(self):
        """200"""

        for i in range(3):
            DriverFactory.create()

        response = self.client.get(reverse("api:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 3)

    def test_get_list_search_model_ok(self):
        """200"""

        DriverFactory.create(model="Alpair 6M")
        DriverFactory.create(model="Pluvia Eleven")

        response = self.client.get(
            reverse("api:driver-list") + "?search=pluv")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["count"], 1)

#            "in_production",
#            "manufacturer",
#            "max_power",
#            "model",
#            "nominal_diameter",
#            "nominal_impedance",
#            "resonant_frequency",
#            "rms_power",
#            "sensitivity",
