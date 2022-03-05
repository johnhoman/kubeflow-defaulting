import json
import typing

from fastapi import Depends
from kubernetes.client import V1Pod, V1PodSpec, V1Container
from kubernetes.client import ApiClient

from src.admission_review import AdmissionReview


def _wrap(obj):
    def to_dict():
        return ApiClient().sanitize_for_serialization(obj)

    obj.to_dict = to_dict
    return obj


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
    pod = _deserialize(admission_review.request.object, V1Pod)
    return _wrap(pod)


def v1_pod_spec(pod: V1Pod = Depends(v1_pod)) -> V1PodSpec:
    """
    Get the pod spec from the pod object in the AdmissionReview and return
    the model representation of the object

    Returns
    -------
    kubernetes.client.V1PodSpec
    """

    def transform(p):
        def _transform(obj):
            p.spec = obj
            return p

        return _transform

    spec = pod.spec
    spec.transform = transform(pod)
    return _wrap(spec)


def v1_container(
    *,
    position: int = None,
    name: str = None,
) -> typing.Callable[[V1PodSpec], V1Container]:
    def container(spec: V1PodSpec = Depends(v1_pod_spec)) -> V1Container:
        pos = 0
        if position:
            pos = position
        elif name:
            for k, item in enumerate(spec.containers):
                if item.name == name:
                    pos = k

        rv = spec.containers[pos]

        def transform(s, rank):
            def _transform(obj):
                s.containers[rank] = obj
                return s

            return _transform

        rv.transform = transform(spec, pos)
        return _wrap(rv)

    return container
