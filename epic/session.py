# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import utils

from datetime import datetime
from epic.api import auth


class Session:
    def __init__(self):
        self.authorization_code = \
            Session.__get_authorization_code_from_user()

        self.access_token = None
        self.refresh_token = None
        self.access_token_expires_at = None
        self.refresh_token_expires_at = None

    #region Properties
    @property
    def is_access_token_expired(self) -> bool:
        return Session.__is_token_expired(self.access_token_expires_at)

    @property
    def is_refresh_token_expired(self) -> bool:
        return Session.__is_token_expired(self.refresh_token_expires_at)

    @property
    def access_authorization_header(self) -> str:
        return f"Bearer {self.access_token}"
    #endregion

    def get_refresh_token(self) -> bool:
        form_data = {
            "grant_type": "authorization_code",
            "code": self.authorization_code
        }

        return self.__do_query_oauth_url(form_data)

    def refresh_access_token(self) -> bool:
        # If the refresh token has expired,
        # we need to request a new one
        # with a new authorization code.
        if self.is_refresh_token_expired:
            self.authorization_code = Session.__get_authorization_code_from_user()
            if not self.get_refresh_token():
                return False

        # We have a valid refresh token
        return self.__refresh_access_token()

    #region Private functions
    def __refresh_access_token(self) -> bool:
        form_data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        return self.__do_query_oauth_url(form_data)

    def __do_query_oauth_url(self, form_data: dict) -> dict:
        with auth.query_oauth_url(form_data) as resp:
            if resp.status_code != 200:
                return False

            src = resp.json()

            if not self.__set_token_values(src):
                return False

            # Convert the expiry times from ISO formatted
            # strings to datetime objects of the same timezone
            self.__set_expiry_times(src)
            return True

    def __set_token_values(self, src: dict):
        if "access_token" not in src:
            return False

        access_token = src["access_token"]
        refresh_token = src["refresh_token"]

        self.access_token = access_token
        self.refresh_token = refresh_token

        return True

    def __set_expiry_times(self, src: dict):
        access_expiry = src["expires_at"]
        refresh_expiry = src["refresh_expires_at"]

        self.access_token_expires_at = \
            utils.from_iso_format(access_expiry)

        self.refresh_token_expires_at = \
            utils.from_iso_format(refresh_expiry)

    #endregion

    @staticmethod
    def __get_authorization_code_from_user() -> str:
        authorization_code = utils.get_user_input_until_valid(
            "authorization code: ")

        return authorization_code

    @staticmethod
    def __is_token_expired(expiry_time: datetime) -> bool:
        now = utils.get_current_utc_datetime()
        expired = now > expiry_time
        return expired

