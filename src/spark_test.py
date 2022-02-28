import json
import base64 as b64

from jsonpatch import JsonPatch

from src import admission_review


def test_spark_pod_has_block_manager_port_defined(client, pod_admission_review):
    obj = client.post(
        "/spark/mutate-driver-core-v1-pod", json=pod_admission_review.dict()
    ).json()
    res = admission_review.AdmissionReview(**obj)
    patch = JsonPatch.from_string(b64.b64decode(res.response.patch).decode())
    pod = patch.apply(pod_admission_review.request.object)
    ports = {port["name"]: port for port in pod["spec"]["containers"][0]["ports"]}
    assert "blockmanager" in ports
    assert ports["blockmanager"]["containerPort"] == 7777
