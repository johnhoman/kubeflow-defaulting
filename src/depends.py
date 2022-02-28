import json

from fastapi import Depends
from kubernetes.client import V1Pod, V1PodSpec
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
    return _deserialize(admission_review.request.object, _ser(V1Pod))


def v1_pod_spec(pod: V1Pod = Depends(v1_pod)) -> V1PodSpec:
    return pod.spec
