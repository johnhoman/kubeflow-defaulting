import json

from kubernetes.client import V1Pod
from kubernetes.client import ApiClient

from src.admission_review import AdmissionReview


class _Req(object):
    def __init__(self, data):
        self.data = json.dumps(data)


def _deserialize(obj, type_):
    return ApiClient().deserialize(_Req(obj), type_)


def _serialize(obj):
    return ApiClient().sanitize_for_serialization(obj)


def pod(admission_review: AdmissionReview) -> V1Pod:
    return _deserialize(admission_review.request.object, V1Pod)
