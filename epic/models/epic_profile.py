# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

from constants import RESULTS_FOLDER_PATH

from epic.models.cosmetic import Cosmetic
from epic.models.external_auth import ExternalAuth

from typing import (
    Union,
    List
)

class EpicProfile:
    def __init__(
        self,
        display_name: str,
        account_id: str,
        external_auths: Union[List[ExternalAuth], None]
    ):
        self.display_name = display_name
        self.account_id = account_id
        self.external_auths = external_auths
        self.cosmetics: List[Cosmetic] = None

    #region Properties
    @property
    def skins(self) -> List[str]:
        return self.__get_cosmetics_by_type('Skin')

    @property
    def emotes(self) -> List[str]:
        return self.__get_cosmetics_by_type("Emote")

    @property
    def pickaxes(self) -> List[str]:
        return self.__get_cosmetics_by_type("Pickaxe")

    @property
    def backblings(self) -> List[str]:
        return self.__get_cosmetics_by_type("Backbling")

    @property
    def other(self) -> List[str]:
        return self.__get_cosmetics_by_type("Unknown")

    @property
    def cosmetic_specific_file_name(self) -> str:
        if self.__has_og_cosmetic():
            file_name = "/og-cosmetics.txt"
        elif self.__has_black_knight():
            file_name = "/black-knights.txt"
        else:
            file_name = "/other-cosmetics.txt"

        return RESULTS_FOLDER_PATH + file_name

    #endregion
    
    #region Helper functions
    def __get_cosmetics_by_type(
        self,
        cosmetic_type: str
    ) -> List[str]:
        cosmetics = [cosmetic for cosmetic in self.cosmetics
            if cosmetic.type == cosmetic_type \
            and cosmetic.name is not None]
        
        cosmetic_names = [cosmetic.name for cosmetic in cosmetics]
        return ", ".join(cosmetic_names)

    def __has_og_cosmetic(self):
        og_skins = [
            "Renegade Raider",
            "OG Ghoul Trooper",
            "OG Skull Trooper",
            "Aerial Assault Trooper"
        ]

        return any(cosmetic.name in og_skins for cosmetic in self.cosmetics) or \
            any(cosmetic.name == "Raider's Revenge" for cosmetic in self.cosmetics)

    def __has_black_knight(self):
        return any(skin.name == "Black Knight" for skin in self.cosmetics)
    #endregion

