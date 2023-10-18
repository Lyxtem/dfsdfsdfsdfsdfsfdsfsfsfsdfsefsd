from xbox.models.achievement import Achievement

class Profile:
    def __init__(self, gamertag: str, xuid: str):
        self.gamertag = gamertag
        self.xuid = xuid
        self.achievement: Achievement = None