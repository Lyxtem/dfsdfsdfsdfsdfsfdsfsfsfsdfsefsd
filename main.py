# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import fileio
import console

from capture import Capture
from typing import Union

from constants import (
    RESOURCES_FOLDER_PATH,
    RESULTS_FOLDER_PATH,
    PROXIES_FILE_PATH,
    COSMETIC_IDS_FILE_PATH
)


def get_platform_from_choice() -> Union[str, None]:
    console.print_options()
    choice = console.colored_input("choose config: ")

    if choice not in ["1", "2", "3"]:
        exit(console.fail(f"invalid choice : {choice}", new_line=True))

    print() # new line

    if choice == "1":
        platform = None
    elif choice == "2":
        platform = "xbl"
    elif choice == "3":
        platform = "psn"

    return platform


def main():
    console.print_banner()
    exists, name = fileio.files_exist(
        RESOURCES_FOLDER_PATH,
        RESULTS_FOLDER_PATH,
        PROXIES_FILE_PATH,
        COSMETIC_IDS_FILE_PATH
    )

    if not exists:
        exit(console.error(f"{name} not found."))

    usernames = fileio.read_lines_from_file_dialog()
    if not usernames:
        exit(console.fail("no usernames found in file."))

    proxies = fileio.read_lines(PROXIES_FILE_PATH)
    if not proxies:
        exit(console.fail("no proxies found in file."))

    proxies = [f"http://{proxy}" for proxy in proxies]

    thread_count = console.colored_input_int("threads: ")
    platform = get_platform_from_choice()

    capture = Capture(platform, thread_count, usernames, proxies)
    capture.do_work_for_usernames_parallel()

    print(console.success("completed...", new_line=True))


if __name__ == "__main__":
    main()

