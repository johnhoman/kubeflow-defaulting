import base64
import typing
from typing import List, Optional

import jsonpatch
import pydantic
from pydantic import Field


class BaseModel(pydantic.BaseModel):
    """
    Forces models to serialize with alias names and exclude all unset
    values
    """

    class Config:
        allow_population_by_field_name = True

    def dict(self, *args, **kwargs):
        kwargs.update(by_alias=True, exclude_unset=True)
        return super().dict(**kwargs)


class GroupVersionKind(BaseModel):
    group: str
    version: str
    kind: str


class GroupVersionResource(BaseModel):
    group: str
    version: str
    resource: str


class UserInfo(BaseModel):
    username: typing.Optional[str]
    uid: typing.Optional[str]
    groups: List[str]


class AdmissionRequest(BaseModel):
    uid: str
    kind: GroupVersionKind
    resource: GroupVersionResource
    namespace: Optional[str]
    operation: str
    user_info: UserInfo = Field(..., alias="userInfo")
    object: dict
    old_object: dict = Field(None, alias="oldObject")


class AdmissionResponse(BaseModel):
    uid: str
    allowed: bool
    status: dict = None
    patch: str = None
    patch_type: str = Field(None, alias="patchType")
    warnings: typing.List[str] = None


class AdmissionReview(BaseModel):
    kind: str
    api_version: str = Field(..., alias="apiVersion")
    request: AdmissionRequest
    response: AdmissionResponse = None

    def patch(self, obj) -> "AdmissionReview":
        """
        Creates a patch response from a mutated object
        :param obj:
        :return:
        """

        while hasattr(obj, "transform"):
            obj = obj.transform(obj)

        if hasattr(obj, "to_dict"):
            obj = obj.to_dict()

        self_copy = self.copy(deep=True)
        p = jsonpatch.JsonPatch.from_diff(self.request.object, obj)
        self_copy.response = AdmissionResponse(
            allowed=True,
            uid=self.request.uid,
            patch=base64.b64encode(str(p).encode()).decode(),
            patch_type="JSONPatch",
        )
        return self_copy

    def denied(self, reason: str = None) -> "AdmissionReview":
        self_copy = self.copy(deep=True)
        self_copy.response = AdmissionResponse(
            allowed=False,
            uid=self_copy.request.uid,
        )
        if reason:
            self_copy.response.status = {"message": reason, "code": 403}
        return self_copy

    def allowed(self) -> "AdmissionReview":
        self_copy = self.copy(deep=True)
        self_copy.response = AdmissionResponse(
            allowed=True,
            uid=self_copy.request.uid,
        )
        return self_copy
