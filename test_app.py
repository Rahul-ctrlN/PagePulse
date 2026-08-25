import pytest
from app import app

client = app.test_client()


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200


def test_invalid_url():
    response = client.post(
        "/analyze",
        json={"url": "invalid-url"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid URL"


def test_empty_url():
    response = client.post(
        "/analyze",
        json={"url": ""}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid URL"