import json
import sys
import unittest
from io import BytesIO
from pathlib import Path


EXAMPLE_ROOT = Path(__file__).resolve().parents[1] / "examples" / "tiny-task-api"
sys.path.insert(0, str(EXAMPLE_ROOT))

from tasks import api as task_api  # noqa: E402
from tasks.service import TaskService  # noqa: E402


class TinyTaskApiTest(unittest.TestCase):
    def setUp(self):
        self.previous_service = task_api.service
        task_api.service = TaskService()

    def tearDown(self):
        task_api.service = self.previous_service

    def request(self, method, path, body=b""):
        response = {}
        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "CONTENT_LENGTH": str(len(body)),
            "wsgi.input": BytesIO(body),
        }

        def start_response(status, headers):
            response["status"] = status
            response["headers"] = dict(headers)

        chunks = task_api.application(environ, start_response)
        response_body = b"".join(chunks)
        response["body"] = json.loads(response_body)
        return response

    def test_get_tasks_returns_empty_list(self):
        response = self.request("GET", "/tasks")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["body"], [])

    def test_post_creates_task_and_trims_title(self):
        response = self.request("POST", "/tasks", b'{"title":"  Read the sample  "}')
        self.assertEqual(response["status"], "201 Created")
        self.assertEqual(response["body"], {"id": 1, "title": "Read the sample"})
        self.assertEqual(self.request("GET", "/tasks")["body"], [response["body"]])

    def test_invalid_json_returns_bad_request(self):
        response = self.request("POST", "/tasks", b'{"title":')
        self.assertEqual(response["status"], "400 Bad Request")
        self.assertEqual(response["body"]["error"], "invalid JSON")

    def test_non_object_json_returns_bad_request(self):
        response = self.request("POST", "/tasks", b"[]")
        self.assertEqual(response["status"], "400 Bad Request")
        self.assertEqual(response["body"]["error"], "expected an object")

    def test_missing_title_returns_bad_request(self):
        response = self.request("POST", "/tasks", b"{}")
        self.assertEqual(response["status"], "400 Bad Request")
        self.assertEqual(response["body"]["error"], "title must be a non-empty string")

    def test_blank_title_returns_bad_request(self):
        response = self.request("POST", "/tasks", b'{"title":"    "}')
        self.assertEqual(response["status"], "400 Bad Request")
        self.assertEqual(response["body"]["error"], "title must be a non-empty string")

    def test_unknown_path_returns_not_found(self):
        response = self.request("GET", "/missing")
        self.assertEqual(response["status"], "404 Not Found")

    def test_unsupported_method_returns_method_not_allowed(self):
        response = self.request("DELETE", "/tasks")
        self.assertEqual(response["status"], "405 Method Not Allowed")


if __name__ == "__main__":
    unittest.main()
