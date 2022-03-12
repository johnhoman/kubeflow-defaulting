import uuid

import pytest
from kubernetes.config import load_kube_config
from kubernetes.client import CoreV1Api
from kubernetes.client import (
    V1Container,
    V1Namespace,
    V1ObjectMeta,
    V1Pod,
    V1PodSpec,
)


class Client(object):

    def __init__(self, namespace):
        self._namespace = namespace

    def create_pod(self, pod):
        resp = CoreV1Api().create_namespaced_pod(self._namespace, pod)
        return resp


@pytest.fixture(scope="session")
def minikube():
    load_kube_config(context="minikube")


@pytest.fixture()
def client(minikube):
    namespace = "testspace-" + str(uuid.uuid4())[:8]
    CoreV1Api().create_namespace(V1Namespace(
        metadata=V1ObjectMeta(name=namespace)
    ))
    yield Client(namespace)
    CoreV1Api().delete_namespace(namespace)


def test_spark_driver(client):

    body = V1Pod(
        metadata=V1ObjectMeta(
            generate_name="spark-driver",
            labels={"spark-driver": "client-mode"}
        ),
        spec=V1PodSpec(
            containers=[V1Container(
                name="driver",
                image="python:3.8",
                command=["python"],
                args=["-m", "http.server", "8888"]
            )]
        ),
    )

    res = client.create_pod(body)
    mapping = {}
    for port in res.spec.containers[0].ports:
        mapping[port.name] = port

    assert mapping["driver"].container_port == 2222
    assert mapping["blockmanager"].container_port == 7777
