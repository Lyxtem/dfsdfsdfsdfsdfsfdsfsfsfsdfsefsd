# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

from os import system
from colorama import Fore, init
init()


def print_banner():
    system("cls")
    print(info("fortnite skin capture\n"))

def print_options():
    options_string = __build_choices_string()
    print(options_string)

def success(string: str, new_line: bool = False) -> str:
    return __build_colored_string(
        __green, "+", string, new_line)

def fail(string: str, new_line: bool = False) -> str:
    string = "failed => " + string
    return __build_colored_string(
        __red, "!", string, new_line)

def error(string: str, new_line: bool = False) -> str:
    string = "error => " + string
    return __build_colored_string(
        __dark_red, "-", string, new_line)

def info(string: str, new_line: bool = False) -> str:
    return __build_colored_string(
        __blue, "*", string, new_line)

def colored_input(prompt: str) -> str:
    prompt = __build_colored_string(
        __yellow, "?", prompt)

    while True:
        print(prompt, end="")
        inp = input()
        if inp:
            return inp
        
def colored_input_int(prompt: str) -> int:
    while True:
        inp = colored_input(prompt)
        if inp.isnumeric():
            return int(inp)


#region Private functions
def __green(string: str) -> str:
    return Fore.GREEN + string + Fore.WHITE

def __red(string: str):
    return Fore.LIGHTRED_EX + string + Fore.WHITE

def __dark_red(string: str) -> str:
    return Fore.RED + string + Fore.WHITE

def __yellow(string: str) -> str:
    return Fore.YELLOW + string + Fore.WHITE

def __blue(string: str) -> str:
    return Fore.BLUE + string + Fore.WHITE

def __build_colored_string(
    color: callable,
    char: str,
    string: str,
    new_line: bool = False
):
    colored_string = ""
    if new_line:
        colored_string += "\n"
    
    colored_string += f"[{color(char)}] {string}"
    return colored_string

def __build_choices_string():
    string = f"\n({__blue('1')}) fn skins by epic username\n"
    string += f"({__blue('2')}) fn skins by xbox username\n"
    string += f"({__blue('3')}) fn skins by psn username\n"
    # string += f"({__blue('4')}) fn skins by epic account id\n"

    return string
#endregion