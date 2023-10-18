# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import requests

from epic.models.epic_profile import EpicProfile
from epic.models.cosmetic import Cosmetic

from epic.parsers import (
    profile_parser,
    cosmetic_parser
)

from epic.session import Session
from constants import (
    PUBLIC_ACCOUNT_URL,
    EXTERNAL_AUTH_URL,
    MCP_URL
)

from typing import (
    List,
    Union
)


def get_epic_profile_by_username(
    username: str,
    proxy: str,
    session: Session
) -> Union[EpicProfile, None]:
    url = f"{PUBLIC_ACCOUNT_URL}/displayName/{username}"
    return __get_epic_profile_by_path(url, proxy, session)

def get_epic_profile_by_external_username(
    username: str,
    platform: str,
    proxy: str,
    session: Session
) -> Union[EpicProfile, None]:
    url = f"{EXTERNAL_AUTH_URL}/{platform}/displayName/{username}"
    return __get_epic_profile_by_path(url, proxy, session)

def get_cosmetics_list(
    account_id: str,
    proxy: str,
    session: Session
) -> Union[List[Cosmetic], None]:
    headers = {
        "Authorization": session.access_authorization_header,
        "Content-Type": "application/json"
    }

    proxies = {
        "https": proxy,
        "http": proxy
    }

    url = f"{MCP_URL}/{account_id}/public/QueryPublicProfile?profileId=campaign"
    with requests.post(url, headers=headers, json={}, proxies=proxies) as resp:
        if resp.status_code != 200:
            raise Exception(f"get_cosmetics_list received status code : {resp.status_code}")

        src = resp.json()

        cosmetics = cosmetic_parser.parse_all_cosmetics(src)
        return cosmetics

#region Private functions
def __get_epic_profile_by_path(
    url: str,
    proxy: str,
    session: Session
) -> Union[EpicProfile, None]:
    headers = {
        "Authorization": session.access_authorization_header
    }

    proxies = {
        "https": proxy
    }

    with requests.get(url, headers=headers, proxies=proxies) as resp:
        if resp.status_code != 200:
            raise Exception(f"__get_epic_profile_by_path received status code : {resp.status_code}")

        src = resp.json()

        epic_profile = profile_parser.parse_profile_lookup_response(src)
        return epic_profile
#endregion
