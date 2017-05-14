import json

from rest_framework.test import APITestCase


class BaseAPITestCase(APITestCase):

    def assert_bad_request(self, response):
        self.assertEqual(response.status_code, 400)

    def assert_get_ok(self, response, **kwargs):
        count = kwargs.get("count", 0)
        self.assertEqual(response.status_code, 200)
        if count > 0:
            self.assertEqual(self.get_content(response)["count"], count)

    def assert_not_found(self, response, **kwargs):
        self.assertEqual(response.status_code, 404)

    def assert_post_ok(self, response, **kwargs):
        self.assertEqual(response.status_code, 201)

    def dump_response(self, response):
        print("{0}".format(self.get_content(response)))

    def get_content(self, response):
        return json.loads(response.content.decode("utf-8"))
