from fastapi import APIRouter, Depends
from fastapi.logger import logger

from src import depends
from src.settings import Settings
from src.admission_review import AdmissionReview
from src.kubernetes_extension import V1Profile


router = APIRouter(tags=["profile"])


AWS_IAM_FOR_SERVICE_ACCOUNT_KIND = "AwsIamForServiceAccount"


@router.post(
    "/mutate-kubeflow-org-v1-profile-iam-plugin",
    response_model=AdmissionReview,
)
def iam_plugin(
    admission_review: AdmissionReview,
    profile: V1Profile = Depends(depends.v1_profile, use_cache=False),
    settings: Settings = Depends(depends.settings, use_cache=True),
):

    if not settings.profile_iam_role:
        logger.warning(
            "profile iam role not configured in settings but "
            "iam plugin default endpoint is receiving traffic"
        )
        return admission_review.allowed()

    if not profile.spec.plugins:
        profile.spec.plugins = []

    for k, plugin in enumerate(profile.spec.plugins):
        # defaulting webhooks should not change existing
        # configuration
        if plugin.kind == AWS_IAM_FOR_SERVICE_ACCOUNT_KIND:
            # only update if it's not already defined
            return admission_review.allowed()

    plugin = {
        "kind": AWS_IAM_FOR_SERVICE_ACCOUNT_KIND,
        "spec": {
            "awsIamRole": settings.profile_iam_role,
        },
    }
    profile.spec.plugins.append(plugin)

    return admission_review.patch(profile)
