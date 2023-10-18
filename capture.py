# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import threading
import utils
import fileio
import console

from epic.session import Session
from epic.target import Target
from epic.models.epic_profile import EpicProfile


from managers.proxy_manager import ProxyManager
from managers.username_manager import UsernameManager

from typing import List


class Capture:
    def __init__(
        self,
        platform: str,
        thread_count: int,
        usernames: List[str],
        proxies: List[str]
    ):
        self.session = Session()
        if not self.session.get_refresh_token():
            exit(console.fail("couldn't create epic games api session."))

        self.platform = platform
        self.thread_count = thread_count

        self.username_manager = UsernameManager(usernames)
        self.proxy_manager = ProxyManager(proxies)

        self.lock = threading.Lock()
        self.is_running = True
        self.is_token_refreshing = False

    def do_work_for_usernames_parallel(self):
        threads = [threading.Thread(target=self.__do_work_for_usernames)
            for _ in range(self.thread_count)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    #region Private functions
    def __do_work_for_usernames(self):
        while self.is_running:
            if self.is_token_refreshing:
                continue

            # Verify the token is valid
            if self.session.is_access_token_expired:
                with self.lock:
                    self.is_token_refreshing = True

                # Refresh the access 
                if not self.session.refresh_access_token():
                    self.is_running = False
                    return

                self.is_token_refreshing = False

            # Get the next username in the list and do work
            username = self.username_manager.next_username()
            if username is None: # reached the end of the list
                self.is_running = False
                return

            # Get cosmetics for username
            self.__do_work_for_username(username)

    def __do_work_for_username(self, username: str):
        while True: # keep trying to find the profile until the request succeeds
            try:
                proxy = self.proxy_manager.next_proxy()
                profile = Target(username, self.session)

                if not profile.get_visible_cosmetics(proxy, self.platform):
                    self.__safe_print(console.fail(f"username '{username}' not found on platform."))
                    return

                epic_profile = profile.epic_profile
                self.__print_epic_profile_info(epic_profile)

                # Save the account info
                self.__save_account_info(username, epic_profile)
                return # exit the loop
            except Exception as e:
                if "received status code : 404" in str(e): # profile not found
                    return

                self.__safe_print(console.error(f"exception occurred on username '{username}' | {e}"))
                continue
    #endregion

    #region Helper functions
    def __safe_print(self, string: str):
        with self.lock:
            print(string)

    def __print_epic_profile_info(self, epic_profile: EpicProfile):
        msg = self.__build_epic_profile_message(epic_profile)
        self.__safe_print(msg)

    def __save_account_info(
        self,
        username: str,
        epic_profile: EpicProfile
    ):
        with self.lock:
            contents = utils.format_account_info(username, epic_profile)
            fileio.append_text(epic_profile.cosmetic_specific_file_name, contents)

    def __build_epic_profile_message(self, epic_profile: EpicProfile) -> str:
        msg = console.success(f"profile found => account id : {epic_profile.account_id} | display name : {epic_profile.display_name}\n")
        msg += ("-" * 35) + "\n"

        # Add the cosmetics to the message
        for c in epic_profile.cosmetics:
            msg += console.success(f"{c.type} found => {c.name}\n")

        # Info delimiter
        msg += ("-" * 35) + "\n"

        # Add the external auths to the message
        external_auths = epic_profile.external_auths

        if external_auths is not None:
            for e in external_auths:
                msg += console.success(f"external auth found => type : {e.auth_type} | display name : {e.display_name}\n")

        msg += ("=" * 35) + "\n"
        return msg
    #endregion


