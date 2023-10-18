class Cosmetic:
    def __init__(
        self,
        cosmetic_id: str,
        cosmetic_name: str,
        # active_variant: str
    ):
        self.id = cosmetic_id
        self.name = cosmetic_name
        # self.variant = active_variant
        self.type = Cosmetic.__get_cosmetic_type_from_id(cosmetic_id)

    @staticmethod
    def __get_cosmetic_type_from_id(cosmetic_id: str):
        if cosmetic_id.startswith("cid"):
            return "Skin"
        elif cosmetic_id.startswith("eid"):
            return "Emote"
        elif cosmetic_id.startswith("bid"):
            return "Backbling"
        elif cosmetic_id.startswith("pickaxe"):
            return "Pickaxe"

        return "Unknown"

