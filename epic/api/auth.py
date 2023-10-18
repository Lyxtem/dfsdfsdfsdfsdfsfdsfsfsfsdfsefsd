# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import requests
import base64

from constants import (
    FORTNITE_IOS_CLIENT_ID,
    FORTNITE_IOS_CLIENT_SECRET,
    OAUTH_URL
)


def query_oauth_url(form_data: dict) -> requests.Response:
    headers = {
        "Authorization": __get_basic_authorization(),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    resp = requests.post(OAUTH_URL, headers=headers, data=form_data)
    return resp
    
def __get_basic_authorization() -> str:
    _bytes = f"{FORTNITE_IOS_CLIENT_ID}:{FORTNITE_IOS_CLIENT_SECRET}".encode()
    encoded = base64.b64encode(_bytes).decode()

    return f"Basic {encoded}"