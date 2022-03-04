from fastapi import APIRouter, Depends
from kubernetes.client import (
    V1ContainerPort,
    V1EnvVar,
    V1EnvVarSource,
    V1ObjectFieldSelector,
    V1Pod,
    V1PodSpec,
)

from src import depends
from src.admission_review import AdmissionReview


router = APIRouter(tags=["spark"])


@router.post("/mutate-driver-core-v1-pod")
def spark_driver_defaults(
    admission_review: AdmissionReview,
    pod: V1Pod = Depends(depends.v1_pod),
    spec: V1PodSpec = Depends(depends.v1_pod_spec),
):
    """
    Configure pod to run as spark driver in client mode

    The driver runs on port 2222, the block manager runs on
    port 7777
    """

    container = spec.containers[0]
    if container.ports is None:
        container.ports = []

    ports = set(port.name for port in container.ports)
    if "driver" not in ports:
        port = V1ContainerPort(
            container_port=2222,
            name="driver",
            protocol="TCP",
        )
        container.ports.append(port)

    if "blockmanager" not in ports:
        port = V1ContainerPort(
            container_port=7777,
            name="blockmanager",
            protocol="TCP",
        )
        container.ports.append(port)

    if container.env is None:
        container.env = []

    envs = set(env.name for env in container.env)
    if "POD_NAMESPACE" not in envs:
        var = V1EnvVar(
            name="POD_NAMESPACE",
            value_from=V1EnvVarSource(
                field_ref=V1ObjectFieldSelector(
                    field_path="metadata.namespace",
                )
            ),
        )
        container.env.append(var)

    if "POD_NAME" not in envs:
        var = V1EnvVar(
            name="POD_NAME",
            value_from=V1EnvVarSource(
                field_ref=V1ObjectFieldSelector(
                    field_path="metadata.name",
                )
            ),
        )
        container.env.append(var)

    if "POD_IP_ADDRESS" not in envs:
        var = V1EnvVar(
            name="POD_IP_ADDRESS",
            value_from=V1EnvVarSource(
                field_ref=V1ObjectFieldSelector(
                    field_path="status.podIP",
                )
            ),
        )
        container.env.append(var)

    pod.spec = spec
    return admission_review.patch(pod.to_dict())
