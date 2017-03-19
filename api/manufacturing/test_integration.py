from django.core.urlresolvers import reverse

from .factories import ManufacturerFactory, MaterialFactory
from utils.testing import BaseAPITestCase


class ManufacturerListTestCase(BaseAPITestCase):

    def test_get_ok(self):
        count = 3
        for i in range(count):
            ManufacturerFactory.create()

        response = self.client.get(reverse("api:manufacturer-list"))
        self.assert_get_ok(response, count=count)


class MaterialListTestCase(BaseAPITestCase):

    def test_get_ok(self):
        count = 3
        for i in range(count):
            MaterialFactory.create()

        response = self.client.get(reverse("api:material-list"))
        self.assert_get_ok(response, count=count)
