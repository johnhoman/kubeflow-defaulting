from fastapi.testclient import TestClient
from pytest import fixture

from src import depends, admission_review


@fixture(scope="function")
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
                        }
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


def test_v1_pod(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    assert pod.metadata.name == "test-pod"
    assert pod.metadata.namespace == "testspace-1234"


def test_v1_pod_spec(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    pod_spec = depends.v1_pod_spec(pod)
    assert pod.spec.to_dict() == pod_spec.to_dict()
