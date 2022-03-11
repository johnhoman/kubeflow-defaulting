import json

from src.kubernetes_extension import ApiClient, V1Profile


class R:
    def __init__(self, d):
        self.data = json.dumps(d)


def test_can_deserialize_profile():
    p = {
        "apiVersion": "kubeflow.org/v1",
        "kind": "Profile",
        "metadata": {
            "name": "profile-name",
        },
        "spec": {
            "owner": {
                "kind": "User",
                "name": "homan.jack@gmail.com",
            },
            "resourceQuotaSpec": {
                "hard": {
                    "cpu": "2",
                    "memory": "2Gi",
                    "requests.nvidia.com/gpu": "1",
                    "persistentvolumeclaims": "1",
                    "requests.storage": "5Gi",
                }
            },
        },
    }

    out = ApiClient().deserialize(R(p), V1Profile)
    assert out.metadata.name == "profile-name"
    assert out.kind == "Profile"
    assert out.api_version == "kubeflow.org/v1"
    assert out.spec.owner.kind == "User"
    assert out.spec.owner.name == "homan.jack@gmail.com"
    assert out.spec.resource_quota_spec.hard == {
        "cpu": "2",
        "memory": "2Gi",
        "requests.nvidia.com/gpu": "1",
        "persistentvolumeclaims": "1",
        "requests.storage": "5Gi",
    }
