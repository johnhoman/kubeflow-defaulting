def test_iam_profile_not_defined_should_not_change_profile(
    client, profile_admission_review
):

    body = client.post(
        "/profile/mutate-kubeflow-org-v1-profile-iam-plugin",
        json=profile_admission_review.dict(),
    ).json()

    assert body["response"]["allowed"]
