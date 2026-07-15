from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_get_version():
    response = client.get("/version")

    assert response.status_code == 200

    assert response.json() == {
        "api_version": "0.59.0",
        "platform_checkpoint": "v3 (in progress)",
        "supported_scope": "v3",
        "scope_v2_compatible": True,
        "scope_v3_api_status": "certified",
    }

def test_version_reports_certified_scope_v3_api():
    response = client.get("/version")

    assert response.status_code == 200

    data = response.json()

    assert data["supported_scope"] == "v3"

    assert (
        data["scope_v3_api_status"]
        == "certified"
    )

    assert (
        data["scope_v2_compatible"]
        is True
    )