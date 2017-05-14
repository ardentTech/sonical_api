from django.core.urlresolvers import reverse

from .factories import DriverFactory, DriverGroupFactory
from manufacturing.factories import ManufacturerFactory
from users.factories import UserFactory
from utils.testing import BaseAPITestCase


class DriverDetailTestCase(BaseAPITestCase):

    def test_get_object_not_found(self):
        response = self.client.get(reverse("api:driver-detail", kwargs={"pk": 0}))
        self.assert_not_found(response)

    def test_get_object_ok(self):
        pk = DriverFactory.create().pk
        response = self.client.get(reverse("api:driver-detail", kwargs={"pk": pk}))
        self.assert_get_ok(response)


class DriverListTestCase(BaseAPITestCase):

    def test_get_ok(self):
        for i in range(3):
            DriverFactory.create()

        response = self.client.get(reverse("api:driver-list"))
        self.assert_get_ok(response, count=3)


class DriverListFilterTestCase(BaseAPITestCase):

    def test_get_dc_resistance_ok(self):
        DriverFactory.create(dc_resistance=2.00)
        DriverFactory.create(dc_resistance=8.00)

        response = self.client.get(
            reverse("api:driver-list") + "?dc_resistance=2.00")
        self.assert_get_ok(response, count=1)

    def test_get_electromagnetic_q_ok(self):
        DriverFactory.create(electromagnetic_q=2.00)
        DriverFactory.create(electromagnetic_q=8.00)

        response = self.client.get(
            reverse("api:driver-list") + "?electromagnetic_q=2.00")
        self.assert_get_ok(response, count=1)

    def test_get_in_production_ok(self):
        DriverFactory.create(in_production=True)
        DriverFactory.create(in_production=False)

        response = self.client.get(
            reverse("api:driver-list") + "?in_production=true")
        self.assert_get_ok(response, count=1)

    def test_get_manufacturer_ok(self):
        dayton_audio = ManufacturerFactory.create(name="Dayton Audio")
        markaudio = ManufacturerFactory.create(name="MarkAudio")
        DriverFactory.create(manufacturer=dayton_audio)
        DriverFactory.create(manufacturer=markaudio)

        response = self.client.get(
            reverse("api:driver-list") + "?manufacturer={0}".format(markaudio.id))
        self.assert_get_ok(response, count=1)

    def test_get_max_power_ok(self):
        DriverFactory.create(max_power=60)
        DriverFactory.create(max_power=50)

        response = self.client.get(
            reverse("api:driver-list") + "?max_power=60")
        self.assert_get_ok(response, count=1)

    def test_get_mechanical_q_ok(self):
        DriverFactory.create(mechanical_q=2.00)
        DriverFactory.create(mechanical_q=8.00)

        response = self.client.get(
            reverse("api:driver-list") + "?mechanical_q=2.00")
        self.assert_get_ok(response, count=1)

    def test_get_model_case_sensitive_ok(self):
        DriverFactory.create(model="Pluvia")
        DriverFactory.create(model="Testing")

        response = self.client.get(
            reverse("api:driver-list") + "?model__contains=Testing")
        self.assert_get_ok(response, count=1)

    def test_get_model_not_case_sensitive_ok(self):
        DriverFactory.create(model="Pluvia")
        DriverFactory.create(model="Testing")

        response = self.client.get(
            reverse("api:driver-list") + "?model__icontains=testing")
        self.assert_get_ok(response, count=1)

    def test_get_nominal_diameter_ok(self):
        DriverFactory.create(nominal_diameter=4)
        DriverFactory.create(nominal_diameter=5)

        response = self.client.get(
            reverse("api:driver-list") + "?nominal_diameter=5")
        self.assert_get_ok(response, count=1)

    def test_get_nominal_impedance_ok(self):
        DriverFactory.create(nominal_impedance=4)
        DriverFactory.create(nominal_impedance=8)

        response = self.client.get(
            reverse("api:driver-list") + "?nominal_impedance=4")
        self.assert_get_ok(response, count=1)

    def test_get_resonant_frequency_ok(self):
        DriverFactory.create(resonant_frequency=120)
        DriverFactory.create(resonant_frequency=80)

        response = self.client.get(
            reverse("api:driver-list") + "?resonant_frequency=80")
        self.assert_get_ok(response, count=1)

    def test_get_rms_power_ok(self):
        DriverFactory.create(rms_power=60)
        DriverFactory.create(rms_power=100)

        response = self.client.get(
            reverse("api:driver-list") + "?rms_power=100")
        self.assert_get_ok(response, count=1)

    def test_get_sensitivity_ok(self):
        DriverFactory.create(sensitivity=90.1)
        DriverFactory.create(sensitivity=88)

        response = self.client.get(
            reverse("api:driver-list") + "?sensitivity=90.1")
        self.assert_get_ok(response, count=1)

    def test_get_voice_coil_inductance_ok(self):
        DriverFactory.create(voice_coil_inductance=0.60)
        DriverFactory.create(voice_coil_inductance=0.90)

        response = self.client.get(
            reverse("api:driver-list") + "?voice_coil_inductance=0.60")
        self.assert_get_ok(response, count=1)


class DriverGroupListTestCase(BaseAPITestCase):

    def test_get_ok(self):
        DriverGroupFactory.create(drivers=(DriverFactory.create(),))
        DriverGroupFactory.create(drivers=(DriverFactory.create(),))

        response = self.client.get(reverse("api:drivergroup-list"))
        self.assert_get_ok(response, count=2)

    def test_post_invalid(self):
        response = self.client.post(reverse("api:drivergroup-list"), data={}, format="json")
        self.assert_bad_request(response)

    def test_post_ok(self):
        payload = DriverGroupFactory.attributes()
        payload["drivers"] = [DriverFactory.create().id]
        payload["author"] = UserFactory.create().id
        response = self.client.post(reverse("api:drivergroup-list"), data=payload, format="json")
        self.assert_post_ok(response)


class DriverGroupListSearchTestCase(BaseAPITestCase):

    def test_get_name_ok(self):
        name = "custom"
        DriverGroupFactory.create(
            drivers=(DriverFactory.create(),),
            name=name)
        DriverGroupFactory.create(
            drivers=(DriverFactory.create(),))

        response = self.client.get(
            reverse("api:drivergroup-list") + "?search={0}".format(name))
        self.assert_get_ok(response, count=1)
