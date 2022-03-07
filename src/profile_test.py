from src import depends, admission_review
from src.patch_util import decode_patch
from src.settings import Settings
from src.profile import AWS_IAM_FOR_SERVICE_ACCOUNT_KIND


def test_iam_profile_not_defined_should_not_change_profile(
    client, profile_admission_review
):
    body = client.post(
        "/profile/mutate-kubeflow-org-v1-profile-iam-plugin",
        json=profile_admission_review.dict(),
    ).json()

    assert body["response"]["allowed"]


def test_profile_iam_plugin_defaults(app, client, profile_admission_review):
    def override():
        return Settings(
            profile_iam_role="arn:aws:iam::0123456789012:role/default-editor"
        )

    app.dependency_overrides[depends.settings] = override
    body = client.post(
        "/profile/mutate-kubeflow-org-v1-profile-iam-plugin",
        json=profile_admission_review.dict(),
    ).json()

    res = admission_review.AdmissionReview(**body)
    patch = decode_patch(res)
    assert len(patch["spec"]["plugins"]) == 1
    assert patch["spec"]["plugins"] == [
        {
            "kind": AWS_IAM_FOR_SERVICE_ACCOUNT_KIND,
            "spec": {"awsIamRole": "arn:aws:iam::0123456789012:role/default-editor"},
        }
    ]


def test_profile_iam_plugin_does_not_overwrite(app, client, profile_admission_review):
    def override():
        return Settings(
            profile_iam_role="arn:aws:iam::0123456789012:role/default-editor"
        )

    profile_admission_review.request.object["spec"]["plugins"] = [
        {
            "kind": AWS_IAM_FOR_SERVICE_ACCOUNT_KIND,
            "spec": {
                "awsIamRole": "arn:aws:iam:0123456789012:role/default-viewer",
            },
        }
    ]
    app.dependency_overrides[depends.settings] = override
    body = client.post(
        "/profile/mutate-kubeflow-org-v1-profile-iam-plugin",
        json=profile_admission_review.dict(),
    ).json()

    res = admission_review.AdmissionReview(**body)
    assert res.response.patch is None
