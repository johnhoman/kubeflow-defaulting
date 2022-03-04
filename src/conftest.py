from fastapi.testclient import TestClient
import pytest

from src import main, admission_review


@pytest.fixture(scope="function")
def app():
    app_ = main.app
    app_.dependency_overrides = {}
    return app_


@pytest.fixture(scope="function")
def client(app):
    return TestClient(app)


@pytest.fixture(scope="function")
def pod_admission_review():
    ar = {
        "kind": "AdmissionReview",
        "apiVersion": "admission.k8s.io/v1beta1",
        "request": {
            "uid": "0df28fbd-5f5f-11e8-bc74-36e6bb280816",
            "kind": {"group": "", "version": "v1", "kind": "Pod"},
            "resource": {"group": "", "version": "v1", "resource": "pods"},
            "namespace": "dummy",
            "operation": "CREATE",
            "userInfo": {
                "username": "system:serviceaccount:kube-system:replicaset-controller",
                "uid": "a7e0ab33-5f29-11e8-8a3c-36e6bb280816",
                "groups": [
                    "system:serviceaccounts",
                    "system:serviceaccounts:kube-system",
                    "system:authenticated",
                ],
            },
            "object": {
                "metadata": {
                    "name": "test-pod",
                    "namespace": "testspace-1234",
                },
                "spec": {
                    "volumes": [],
                    "containers": [
                        {
                            "name": "main",
                            "image": "python:3.8",
                        },
                        {
                            "name": "proxy",
                            "image": "nginx:latest",
                        },
                    ],
                    "restartPolicy": "Always",
                    "serviceAccountName": "default",
                    "serviceAccount": "default",
                },
                "status": {},
            },
            "oldObject": None,
        },
    }
    return admission_review.AdmissionReview(**ar)
