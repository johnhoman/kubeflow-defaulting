import json
import typing

from fastapi import Depends
from kubernetes.client import V1Pod, V1PodSpec, V1Container
from kubernetes.client import ApiClient

from src.admission_review import AdmissionReview


def _ser(cls):
    def to_dict(self):
        return ApiClient().sanitize_for_serialization(self)

    cls.to_dict = to_dict
    return cls


class _Req(object):
    def __init__(self, data):
        self.data = json.dumps(data)


def _deserialize(obj, type_):
    return ApiClient().deserialize(_Req(obj), type_)


def v1_pod(admission_review: AdmissionReview) -> V1Pod:
    """
    Get the pod object from the AdmissionReview and return
    the model representation of the object

    Returns
    -------
    kubernetes.client.V1Pod
    """
    return _deserialize(admission_review.request.object, _ser(V1Pod))


def v1_pod_spec(pod: V1Pod = Depends(v1_pod)) -> V1PodSpec:
    """
    Get the pod spec from the pod object in the AdmissionReview and return
    the model representation of the object

    Returns
    -------
    kubernetes.client.V1PodSpec
    """
    return pod.spec


def v1_container(
    *,
    position: int = None,
    name: str = None,
) -> typing.Callable[[AdmissionReview], V1Container]:
    def container(spec: V1PodSpec = Depends(v1_pod_spec)) -> V1Container:
        if position:
            return spec.containers[position]
        elif name:
            for container in spec.containers:
                if container.name == name:
                    return container
            return spec.containers[0]
        else:
            return spec.containers[0]

    return container
