from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    """
    the provided iam role will be used as the default
    iam role for profiles. If left empty, profile will
    not change the iam plugin values.
    """

    profile_iam_role: str = Field(None, env="KF_DEFAULTING_PROFILE_IAM_ROLE_ARN")
