from src import admission_review
from src.patch_util import decode_patch


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


def test_spark_pod_has_ip_address(client, pod_admission_review):
    obj = client.post(
        "/spark/mutate-driver-core-v1-pod", json=pod_admission_review.dict()
    ).json()
    ob = decode_patch(admission_review.AdmissionReview(**obj))
    env = {env["name"]: env for env in ob["spec"]["containers"][0]["env"]}
    assert env["POD_IP_ADDRESS"]["valueFrom"]["fieldRef"]["fieldPath"] == "status.podIP"

