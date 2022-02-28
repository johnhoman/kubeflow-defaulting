from fastapi.testclient import TestClient
import pytest

from src import main


@pytest.fixture(scope="function")
def app():
    app_ = main.app
    app_.dependency_overrides = {}
    return app_


@pytest.fixture(scope="function")
def client(app):
    return TestClient(app)


def test_healthcheck(client):
    res = main.HealthCheck(**client.get("/healthz").json())
    assert res.ok
