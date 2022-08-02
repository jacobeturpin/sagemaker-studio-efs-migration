"""User mapping"""

from dataclasses import dataclass


@dataclass
class UserMap:

    user_name: str

    source_efs_fs_uid: str = None
    target_efs_fs_uid: str = None

    sso_user_identifier: str = None
    sso_user_value: str = None
