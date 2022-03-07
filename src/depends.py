import json
import typing

from fastapi import Depends
from kubernetes.client import V1Pod, V1PodSpec, V1Container

from src.kubernetes_extension import ApiClient, V1Profile
from src.admission_review import AdmissionReview


def _wrap(cls):
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
    pod = _deserialize(admission_review.request.object, _wrap(V1Pod))
    return pod


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
    return spec


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
        return rv

    return container


def v1_profile(admission_review: AdmissionReview):
    profile = _deserialize(admission_review.request.object, _wrap(V1Profile))
    return profile
