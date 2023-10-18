# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import requests
import time

from xbox.models.account import Account
from xbox.models.profile import Profile
from xbox.models.achievement import Achievement

from xbox.api import auth
from typing import Union


def get_gunsmith_achievement(
    profile: Profile,
    account: Account
) -> bool:
    # Get all Fortnite achievements by XUID
    achievements = __get_fortnite_achievements(profile, account)
    if not achievements:
        return False

    # Check if the `Gunsmith` achievement has been unlocked
    for achievement in achievements:
        name = achievement["name"]
        if name != "Gunsmith":
            continue

        if achievement["progressState"] == "Achieved":
            # Create new Achievement object with name and time unlocked
            time_unlocked = achievement["progression"]["timeUnlocked"]
            profile.achievement = Achievement(
                name=name,
                time_unlocked=time_unlocked
            )

            return True

    return False

def get_profile(
    gamertag: str,
    account: Account,
    reauth: bool = True
) -> Profile:
    headers = {
        "Authorization": account.xbl2_authorization_header,
        "x-xbl-contract-version": "2"
    }

    url = f"https://services.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag"
    with requests.get(url, headers=headers) as resp:
        if resp.status_code != 200:
            if resp.status_code == 401 and reauth and not account.is_reauthorizing:
                account.is_reauthorizing = True
                if not auth.try_account_reauth(account):
                    return

            time.sleep(5)
            account.is_reauthorizing = False
            return get_profile(gamertag, account, reauth=False)

        src = resp.json()
        profile_users = src["profileUsers"]

        current_gamertag = profile_users[0]["settings"][0]["value"]
        xuid = profile_users[0]["id"]

        return Profile(
            gamertag=current_gamertag,
            xuid=xuid
        )

def __get_fortnite_achievements(
    profile: Profile,
    account: Account,
    reauth: bool = True
) -> list:
    headers = {
        "x-xbl-contract-version": "4",
        "authorization": account.xbl3_authorization_header
    }

    url = f"https://achievements.xboxlive.com/users/xuid({profile.xuid})/achievements?titleId=267695549&maxItems=100"
    with requests.get(url, headers=headers) as resp:
        if resp.status_code != 200:
            if resp.status_code == 401 and reauth and not account.is_reauthorizing:
                account.is_reauthorizing = True
                if not auth.try_account_reauth(account):
                    return

            time.sleep(5)
            account.is_reauthorizing = False
            return __get_fortnite_achievements(profile, account, reauth=False)

        src = resp.json()
        achievements = src["achievements"]

        return achievements
