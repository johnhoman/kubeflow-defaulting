import kubernetes
from kubernetes.client import Configuration
from kubernetes.client import V1Pod


class _ExtensionBase(object):
    """
    Base type for defining additional openapi types that
    implement a kubernetes.client.models object
    """

    to_dict = V1Pod.to_dict
    to_str = V1Pod.to_str

    def __repr__(self):
        return self.to_str()

    def __eq__(self, other):
        if not isinstance(type(self), other):
            return False
        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        if not isinstance(type(self), other):
            return True
        return self.to_dict() != other.to_dict()


class V1ProfileCondition(_ExtensionBase):
    openapi_types = {
        "type_": "str",
        "status": "str",
        "message": "str",
    }

    attribute_map = {
        "type_": "type",
        "status": "status",
        "message": "message",
    }

    def __init__(
        self,
        type_=None,
        status=None,
        message=None,
        local_vars_configuration=None,
    ):

        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self.type_ = type_
        self.status = status
        self.message = message


class V1ProfileStatus(_ExtensionBase):
    openapi_types = {"conditions": "list[V1ProfileCondition]"}
    attribute_map = {"conditions": "conditions"}

    def __init__(
        self,
        conditions=None,
        local_vars_configuration=None,
    ):

        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self.conditions = conditions


class V1ProfilePlugin(_ExtensionBase):
    openapi_types = {
        "kind": "str",
        "spec": "dict(str, str)",
    }
    attribute_map = {
        "kind": "kind",
        "spec": "spec",
    }

    def __init__(
        self,
        kind=None,
        spec=None,
        local_vars_configuration=None,
    ):

        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self.kind = kind
        self.spec = spec


class V1ProfileSpec(_ExtensionBase):
    openapi_types = {
        "owner": "V1Subject",
        "resource_quota_spec": "V1ResourceQuotaSpec",
        "plugins": "list[V1ProfilePlugin]",
    }
    attribute_map = {
        "owner": "owner",
        "resource_quota_spec": "resourceQuotaSpec",
        "plugins": "plugins",
    }

    def __init__(
        self,
        owner=None,
        resource_quota_spec=None,
        plugins=None,
        local_vars_configuration=None,
    ):
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self.owner = owner
        self.resource_quota_spec = resource_quota_spec
        self.plugins = plugins


class V1Profile(_ExtensionBase):
    openapi_types = {
        "api_version": "str",
        "kind": "str",
        "metadata": "V1ObjectMeta",
        "spec": "V1ProfileSpec",
        "status": "V1ProfileStatus",
    }
    attribute_map = {
        "api_version": "apiVersion",
        "kind": "kind",
        "metadata": "metadata",
        "spec": "spec",
        "status": "status",
    }

    def __init__(
        self,
        api_version=None,
        kind=None,
        metadata=None,
        spec=None,
        status=None,
        local_vars_configuration=None,
    ):
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self.api_version = api_version
        self.kind = kind
        self.metadata = metadata
        self.spec = spec
        self.status = status


class ApiClient(kubernetes.client.ApiClient):
    """
    deserialize additional api models
    """

    # additional_types is so deserialize finds the
    # below types. kubernetes is hardcoded to
    # getattr(kubernetes.client.models, klass) so
    # there's no other way to inject these AFAICT
    additional_types = {
        "V1Profile": V1Profile,
        "V1ProfileSpec": V1ProfileSpec,
        "V1ProfilePlugin": V1ProfilePlugin,
        "V1ProfileStatus": V1ProfileStatus,
        "V1ProfileCondition": V1ProfileCondition,
    }

    def __deserialize(self, data, klass):
        if isinstance(klass, str) and klass in self.additional_types:
            klass = self.additional_types[klass]

        return super().__deserialize(data, klass)
