import json

from tasks.service import TaskService

service = TaskService()


def _respond(start_response, status, body):
    payload = json.dumps(body).encode("utf-8")
    start_response(
        status,
        [("Content-Type", "application/json"), ("Content-Length", str(len(payload)))],
    )
    return [payload]


def application(environ, start_response):
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]

    if path != "/tasks":
        return _respond(start_response, "404 Not Found", {"error": "not found"})

    if method == "GET":
        return _respond(start_response, "200 OK", service.list_tasks())
    if method != "POST":
        return _respond(start_response, "405 Method Not Allowed", {"error": "method not allowed"})

    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw_body = environ["wsgi.input"].read(length)
    try:
        body = json.loads(raw_body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _respond(start_response, "400 Bad Request", {"error": "invalid JSON"})
    if not isinstance(body, dict):
        return _respond(start_response, "400 Bad Request", {"error": "expected an object"})

    try:
        task = service.create(body.get("title"))
    except ValueError as error:
        return _respond(start_response, "400 Bad Request", {"error": str(error)})
    return _respond(start_response, "201 Created", task)
