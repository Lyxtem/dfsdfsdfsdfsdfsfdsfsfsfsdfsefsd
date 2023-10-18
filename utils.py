# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import re

from console import colored_input
from datetime import datetime, timezone
from epic.models.epic_profile import EpicProfile


def get_inner_substring(string: str, start: str, end: str) -> str:
    pattern = re.escape(start) + "(.*?)" + re.escape(end)
    match = re.search(pattern, string)

    if match is None:
        return
    
    substring = match.group(1)
    return substring
    

def get_current_utc_datetime() -> datetime:
    now = datetime.utcnow() \
        .replace(tzinfo=timezone.utc)

    return now

def from_iso_format(datetime_str: str) -> datetime:
    datetime_obj = datetime.fromisoformat(datetime_str) \
        .replace(tzinfo=timezone.utc)

    return datetime_obj

def get_results_file_name(platform: str) -> str:
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d_%H-%M-%S")

    file_name = f"/{formatted}-{platform}.txt"
    return file_name

def format_account_info(
    target_username: str,
    epic_profile: EpicProfile
) -> str:
    account_info = [f"{target_username}"]
    account_info.append(f"Username: {epic_profile.display_name}")
    account_info.append(f"Account Id: {epic_profile.account_id}")
    account_info.append(f"Skins: {epic_profile.skins}")
    account_info.append(f"Pickaxes: {epic_profile.pickaxes}")
    account_info.append(f"Backblings: {epic_profile.backblings}")
    account_info.append(f"Emotes: {epic_profile.emotes}")
    account_info.append(f"Other Cosmetics: {epic_profile.other}")

    external_auths = []
    for external_auth in epic_profile.external_auths:
        external_auths.append(f"({external_auth.auth_type}, display name : {external_auth.display_name})")

    account_info.append(f"Accs: {', '.join(external_auths)}")
    return " | ".join(account_info)

def get_user_input_until_valid(prompt: str) -> str:
    return colored_input(prompt)