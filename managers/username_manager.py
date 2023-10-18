# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

from typing import List
from threading import Lock

class UsernameManager:
    def __init__(self, usernames: List[str]):
        self.usernames = usernames
        self.lock = Lock()

    def next_username(self):
        with self.lock:
            if len(self.usernames) == 0:
                return
            
            username = self.usernames.pop(0)
            return username