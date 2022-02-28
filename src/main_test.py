from src.main import HealthCheck


def test_healthcheck(client):
    res = HealthCheck(**client.get("/healthz").json())
    assert res.ok
