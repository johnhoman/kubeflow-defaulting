from src import depends


def test_v1_pod(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    assert pod.metadata.name == "test-pod"
    assert pod.metadata.namespace == "testspace-1234"


def test_v1_pod_spec(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    pod_spec = depends.v1_pod_spec(pod)
    assert pod.spec.to_dict() == pod_spec.to_dict()


def test_v1_container_default(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    pod_spec = depends.v1_pod_spec(pod)
    container = depends.v1_container()(pod_spec)
    assert pod.spec.containers[0].to_dict() == container.to_dict()


def test_v1_container_position_0(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    pod_spec = depends.v1_pod_spec(pod)
    container = depends.v1_container(position=0)(pod_spec)
    assert pod.spec.containers[0].to_dict() == container.to_dict()


def test_v1_container_by_name(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    pod_spec = depends.v1_pod_spec(pod)
    container = depends.v1_container(name="main")(pod_spec)
    assert pod.spec.containers[0].to_dict() == container.to_dict()


def test_v1_container_by_name_can_revert_to_pod(pod_admission_review):
    pod = depends.v1_pod(pod_admission_review)
    pod_spec = depends.v1_pod_spec(pod)
    container = depends.v1_container(name="main")(pod_spec)
    assert pod_admission_review.patch(container) == pod_admission_review.patch(pod)


def test_v1_profile_can_deserialize(profile_admission_review):
    profile = depends.v1_profile(profile_admission_review)
    assert profile.spec.owner.kind == "User"
