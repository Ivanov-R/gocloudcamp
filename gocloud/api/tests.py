import requests
from django.test import TestCase
from rest_framework import status


class ApiTests(TestCase):
    def test_post_get_delete_config(self):
        request = {
            "service": "managed-k8s_v3",
            "data": [{"key5": "value7"}, {"key6": "value8"}],
        }
        response = requests.post("http://127.0.0.1:8080/config", json=request)
        response = requests.get(
            "http://127.0.0.1:8080/config?service=managed-k8s_v3"
        )
        expected_response = {"key6": "value8", "key5": "value7"}
        self.assertEqual(response.json(), expected_response)
        response = requests.delete(
            "http://127.0.0.1:8080/config?service=managed-k8s_v3"
        )
        expected_response = {
            "message": "You need to specify version in request!"
        }
        self.assertEqual(response.json(), expected_response)
        response = requests.delete(
            "http://127.0.0.1:8080/config?service=managed-k8s_v3&version=1"
        )
        expected_response = {
            "message": "Not allowed to delete actual config used in service!"
        }
        self.assertEqual(response.json(), expected_response)

    def test_get_config_status_code(self):
        request = {
            "service": "managed-k8s",
            "data": [{"key1": "value1"}, {"key2": "value2"}],
        }
        response = requests.post("http://127.0.0.1:8080/config", json=request)
        responses = {
            "http://127.0.0.1:8080/config?service=managed-k8s":
                status.HTTP_200_OK,
            "http://127.0.0.1:8080/config?service=managed-k8s&version=1":
                status.HTTP_200_OK,
            "http://127.0.0.1:8080/config?version=1":
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            "http://127.0.0.1:8080/config?service=noname":
                status.HTTP_404_NOT_FOUND,
            "http://127.0.0.1:8080/config?service=managed-k8s&version=2":
                status.HTTP_404_NOT_FOUND,
            "http://127.0.0.1:8080/noname_address":
                status.HTTP_404_NOT_FOUND,
        }
        for url, expected_status in responses.items():
            response = requests.get(url)
            with self.subTest(url=url):
                self.assertEqual(response.status_code, expected_status)

    def test_repeat_requests(self):
        request = {
            "service": "managed-k8s_v3",
            "data": [{"key5": "value7"}, {"key6": "value8"}],
        }
        response = requests.post("http://127.0.0.1:8080/config", json=request)
        response = requests.post("http://127.0.0.1:8080/config", json=request)
        expected_response = {
            "message": (
                "Such config already exists! Use method Put to"
                " add new version of config for this service"
            )
        }
        self.assertEqual(response.json(), expected_response)
