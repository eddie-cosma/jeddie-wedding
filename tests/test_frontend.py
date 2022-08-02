import pytest

from . import app, client, runner


def test_homepage_connection(client):
    response = client.get("/")
    assert response.status_code == 200
