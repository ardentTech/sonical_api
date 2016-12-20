import json

from rest_framework.test import APITestCase


class BaseAPITestCase(APITestCase):

    def dump_response(self, response):
        print("{0}".format(self.get_content(response)))

    def get_content(self, response):
        return json.loads(response.content.decode("utf-8"))
