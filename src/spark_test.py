import base64 as b64

from jsonpatch import JsonPatch

from src import admission_review


def decode_patch(review: admission_review.AdmissionReview) -> dict:
    """
    decode the patch from the admission response
    and return the patched object
    """

    patch = JsonPatch.from_string(b64.b64decode(review.response.patch).decode())
    obj = patch.apply(review.request.object)
    return obj


def test_spark_pod_has_block_manager_port_defined(client, pod_admission_review):
    """
    the webhook exposes port 7777 on the target pod
    """
    obj = client.post(
        "/spark/mutate-driver-core-v1-pod", json=pod_admission_review.dict()
    ).json()
    res = admission_review.AdmissionReview(**obj)
    pod = decode_patch(res)
    ports = {port["name"]: port for port in pod["spec"]["containers"][0]["ports"]}
    assert "blockmanager" in ports
    assert ports["blockmanager"]["containerPort"] == 7777


def test_spark_default_is_idempotent(client, pod_admission_review):
    """
    repeated calls to the webhook produces the same result
    """
    obj = client.post(
        "/spark/mutate-driver-core-v1-pod", json=pod_admission_review.dict()
    ).json()
    res = admission_review.AdmissionReview(**obj)
    before = decode_patch(res)
    obj = client.post(
        "/spark/mutate-driver-core-v1-pod",
        json=admission_review.AdmissionReview(**obj).dict(),
    ).json()
    res = admission_review.AdmissionReview(**obj)
    after = decode_patch(res)
    assert before == after
