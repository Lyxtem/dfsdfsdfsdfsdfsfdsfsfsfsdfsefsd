# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

from epic.api import profile
from epic.session import Session
from epic.models.epic_profile import EpicProfile

from typing import Optional

class Target:
    def __init__(
        self,
        username: str,
        session: Session
    ):
        self.username = username
        self.session = session
        self.epic_profile: EpicProfile = None

    def get_visible_cosmetics(
        self,
        proxy: str,
        platform: Optional[str] = None
    ) -> bool:
        # The epic account's id is required
        # to get information about the account.
        if not self.__get_epic_profile_by_platform(proxy, platform):
            return False

        # Using the account's id we can get
        # the information we want.
        cosmetics = profile.get_cosmetics_list(
            self.epic_profile.account_id, proxy, self.session)

        if cosmetics is None:
            return False

        self.epic_profile.cosmetics = cosmetics
        return True

    #region Private functions
    def __get_epic_profile_by_platform(
        self,
        proxy: str,
        platform: Optional[str] = None
    ) -> bool:
        if platform is None:
            epic_profile = profile.get_epic_profile_by_username(
                self.username, proxy, self.session)
        else:
            epic_profile = profile.get_epic_profile_by_external_username(
                self.username, platform, proxy, self.session)

        if epic_profile is None:
            return False

        self.epic_profile = epic_profile
        return True
    #endregion
