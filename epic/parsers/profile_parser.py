from epic.models.external_auth import ExternalAuth
from epic.models.epic_profile import EpicProfile

from typing import (
    Union,
    List
)


def parse_profile_lookup_response(
    src: Union[dict, list]
) -> Union[EpicProfile, None]:
    # Sometimes the response is a list of profiles,
    # other times its a single profile.
    # To handle that we check the type
    if isinstance(src, list):
        if len(src) == 0:
            return

        profile = src[0]
    elif isinstance(src, dict):
        if "id" not in src:
            return

        profile = src

    epic_profile = __parse_epic_account_info(profile)
    return epic_profile

#region Private functions
def __parse_epic_account_info(profile: dict) -> Union[EpicProfile, None]:
    account_id = None
    if "id" in profile:
        account_id = profile["id"]

    display_name = None
    if "displayName" in profile:
        display_name = profile["displayName"]

    external_auths = __parse_external_auths(profile)

    epic_profile = EpicProfile(display_name, account_id, external_auths)
    return epic_profile

def __parse_external_auths(profile: dict) -> Union[List[ExternalAuth], None]:
    if "externalAuths" not in profile:
        return

    external_auths = profile["externalAuths"]
    if len(external_auths) == 0:
        return

    external_auth_objs = []
    for key in external_auths.keys():
        account_id = external_auths[key].get("accountId")
        auth_type = external_auths[key].get("type")
        display_name = external_auths[key].get("externalDisplayName")
        external_auth = ExternalAuth(display_name, account_id, auth_type)
        external_auth_objs.append(external_auth)

    return external_auth_objs
#endregion
