# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import itertools

from typing import List
from threading import Lock

class ProxyManager:
    def __init__(
        self,
        proxies: List[str]
    ):
        self.proxies = itertools.cycle(proxies)
        self.lock = Lock()

    def next_proxy(self) -> str:
        with self.lock:
            return next(self.proxies)
