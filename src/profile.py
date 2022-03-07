from fastapi import APIRouter, Depends
from fastapi.logger import logger

from src import depends
from src.settings import Settings
from src.admission_review import AdmissionReview
from src.kubernetes_extension import V1Profile


router = APIRouter(tags=["profile"])


@router.post("/mutate-kubeflow-org-v1-profile-iam-plugin")
def iam_plugin(
    admission_review: AdmissionReview,
    profile: V1Profile = Depends(depends.v1_profile),
    settings: Settings = Depends(depends.settings, use_cache=True),
):

    if not settings.profile_iam_role:
        logger.warning(
            "profile iam role not configured in settings but iam plugin default endpoint is receiving traffic"
        )
        return admission_review.allowed()

    return admission_review.patch(profile)
