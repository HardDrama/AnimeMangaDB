from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_frontend_origin_is_allowed():
    response = client.options(
        "/anime",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["access-control-allow-origin"]
        == "http://localhost:5173"
    )