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
