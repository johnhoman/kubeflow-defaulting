from src import depends, admission_review


def test_v1_pod(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    assert pod.metadata.name == "test-pod"
    assert pod.metadata.namespace == "testspace-1234"


def test_v1_pod_spec(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    pod_spec = depends.v1_pod_spec(pod)
    assert pod.spec.to_dict() == pod_spec.to_dict()


def test_v1_container(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    pod_spec = depends.v1_pod_spec(pod)
    container = depends.v1_container(position=0)(pod_spec)
    assert pod.spec.containers[0].to_dict() == container.to_dict()
