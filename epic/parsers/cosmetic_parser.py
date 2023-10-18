# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: PullsS

from epic.models.cosmetic import Cosmetic
from constants import COSMETIC_IDS

from typing import (
    List,
    Union
)

def parse_all_cosmetics(src: dict) -> Union[List[Cosmetic], None]:
    cosmetic_locker = __get_cosmetic_locker(src)
    if cosmetic_locker is None:
        return

    cosmetics = __parse_all_locker_slots(cosmetic_locker)
    if cosmetics is None:
        return

    unique_cosmetics = __remove_duplicate_cosmetics(cosmetics)
    return unique_cosmetics


#region Private functions
def __get_cosmetic_locker(src: dict) -> dict:
    if "profileChanges" not in src:
        return

    profile_changes = src["profileChanges"]
    if len(profile_changes) == 0:
        return

    profile = profile_changes[0]["profile"]
    items = profile["items"]

    # Extract Cosmetic Locker items
    cosmetic_locker = [cosmetic for cosmetic in items.values() \
        if "CosmeticLocker" in cosmetic.get("templateId", "")]

    return cosmetic_locker

def __parse_all_locker_slots(cosmetic_locker: list) -> List[Cosmetic]:
    # A list of skins, emotes, and pickaxes
    # from the epic games response
    found_cosmetics: List[Cosmetic] = []

    for cosmetic in cosmetic_locker:
        locker_slots = cosmetic["attributes"]["locker_slots_data"]["slots"]
        cosmetics = __parse_cosmetic_types(locker_slots)
        found_cosmetics.extend(cosmetics)

    # Remove the empty cosmetics
    found_cosmetics = [cosmetic for cosmetic in found_cosmetics if cosmetic is not None]

    # Find the cosmetics that aren't in the response by matching
    # the ones found with the set they came in
    all_cosmetics = __get_all_cosmetic_pairs(found_cosmetics)
    return all_cosmetics

def __parse_cosmetic_types(locker_slots: list) -> List[Cosmetic]:
    cosmetics: List[Cosmetic] = []
    cosmetic_types = ["Character", "Backpack", "Dance", "Pickaxe"]

    for cosmetic_type in cosmetic_types:
        verify_variant = cosmetic_type == cosmetic_types[0] # Only verify if the type is Character (skin)
        cosmetic = __parse_cosmetic_slot(locker_slots, cosmetic_type, verify_variant)
        if cosmetic is not None:
            cosmetics.extend(cosmetic)

    return cosmetics

def __parse_cosmetic_slot(
    locker_slots: dict,
    cosmetic_type: str,
    verify_variant: bool = False
) -> Union[List[Cosmetic], None]:
    if cosmetic_type not in locker_slots:
        return

    cosmetic_slot = locker_slots[cosmetic_type]
    cosmetic_items = cosmetic_slot["items"]

    cosmetics: List[Cosmetic] = []
    for item in cosmetic_items:
        if item == "" or item is None:
            continue

        if verify_variant and "activeVariants" not in cosmetic_slot:
            continue # ignore the skin if there are no active variants and it needs to be verified

        if "activeVariants" in cosmetic_slot and verify_variant:
            variants = cosmetic_slot["activeVariants"] # get the current variants
            if not __is_og_variant(item, variants):
                continue

        if ":" in item:
            colon_index = item.index(":")
            item = item[colon_index + 1:]

        if item not in COSMETIC_IDS:
            continue

        cosmetic_name = COSMETIC_IDS[item]
        cosmetic = Cosmetic(item, cosmetic_name)
        cosmetics.append(cosmetic)

    return cosmetics
#endregion

#region Helper functions
def __is_og_variant(
    cosmetic_id: str,
    cosmetic_variants: dict
) -> bool:
    # input(f"{cosmetic_variants} \n\n {cosmetic_id}")
    # Remove null variants
    cosmetic_variants = [variant for variant in cosmetic_variants
        if variant is not None]

    # Skull and Ghoul Trooper skins have
    # OG and NON OG variants.
    # We only want the OG one
    skins_with_variants = [
        "cid_030_athena_commando_m_halloween",
        "cid_029_athena_commando_f_halloween"
    ]

    if len(cosmetic_variants) == 0:
        if any(x in cosmetic_id for x in skins_with_variants):
            # if there are no variants and the skin
            # is the skull or ghoul trooper ignore it
            return False

        return True

    active_variant = cosmetic_variants[0]["variants"][0]["active"]
    if "cid_030_athena_commando_m_halloween" in cosmetic_id: # Skull Trooper
        return active_variant == "Mat1"

    if "cid_029_athena_commando_f_halloween" in cosmetic_id: # Ghoul Trooper
        return active_variant == "Mat3"

    # No other skins need to be verified
    return True

def __remove_duplicate_cosmetics(
    all_cosmetics: List[Cosmetic]
) -> List[Cosmetic]:
    seen_cosmetic_ids: List[str] = []
    retained_cosmetics: List[Cosmetic] = []

    for cosmetic in all_cosmetics:
        cosmetic_id = cosmetic.id
        if cosmetic_id in seen_cosmetic_ids:
            continue

        seen_cosmetic_ids.append(cosmetic_id)
        retained_cosmetics.append(cosmetic)

    return retained_cosmetics

def __get_all_cosmetic_pairs(
    cosmetics: List[Cosmetic]
) -> List[Cosmetic]:
    cosmetic_pairs = [[
        "cid_175_athena_commando_m_celestial",
        "bid_138_celestial",
        "pickaxe_id_116_celestial"
    ], [
        "cid_313_athena_commando_m_kpopfashion",
        "eid_kpopdance03"
    ], [
        "cid_035_athena_commando_m_medieval",
        "bid_004_blackknight"
    ], [
        "cid_441_athena_commando_f_cyberscavengerblue",
        "bid_288_cyberscavengerfemaleblue"
    ], [
        "cid_516_athena_commando_m_blackwidowrogue",
        "bid_346_blackwidowrogue"
    ], [
        "cid_660_athena_commando_f_bandageninjablue",
        "bid_452_bandageninjablue"
    ], [
        "cid_089_athena_commando_m_retrogrey",
        "bid_029_retrogrey"
    ]]

    for cosmetic_pair in cosmetic_pairs:
        pairs = __get_cosmetic_pairs_for_type(cosmetics, cosmetic_pair)
        cosmetics.extend(pairs)

    return cosmetics

def __get_cosmetic_pairs_for_type(
    cosmetics: List[Cosmetic],
    cosmetic_ids: List[str]
) -> List[Cosmetic]:
    if __has_any_cosmetic(cosmetics, cosmetic_ids):
        for comestic_id in cosmetic_ids:
            if __has_cosmetic(cosmetics, comestic_id):
                continue

            name = COSMETIC_IDS[comestic_id]
            cosmetic = Cosmetic(comestic_id, name)
            cosmetics.append(cosmetic)

    return cosmetics

def __has_any_cosmetic(
    cosmetics: List[Cosmetic],
    cosmetic_ids: List[str]
) -> bool:
    return any(__has_cosmetic(cosmetics, cosmetic_id) for cosmetic_id in cosmetic_ids)

def __has_cosmetic(cosmetics: List[Cosmetic], cosmetic_id: str):
    return any(cosmetic.id == cosmetic_id for cosmetic in cosmetics)
#endregion
