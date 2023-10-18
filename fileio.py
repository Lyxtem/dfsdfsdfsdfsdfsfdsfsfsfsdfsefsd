# Fortnite Skin Capture
# Telegram: @Pulls
# Telegram Channel: @EpicAOV
# Discord: Pulls

import os
import json

import tkinter as tk
from tkinter import filedialog

from typing import (
    Tuple,
    List,
    Dict,
    Union
)


def files_exist(*files: list) -> Tuple[bool, Union[str, None]]:
    for _file in files:
        if not os.path.exists(_file):
            return False, _file
        
    return True, None

def read_lines(file_name: str) -> List[str]:
    with open(file_name, encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line]
        return lines

def read_json(file_name: str) -> Dict[str, Union[dict, str]]:
    with open(file_name, encoding="utf-8") as f:
        obj = json.load(f)
        return dict(obj)

def read_lines_from_file_dialog() -> Union[List[str], None]:
    while True:
        file_name = __get_file_name_from_dialog()
        if file_name == "":
            continue

        exists, _ = files_exist(file_name)
        if exists:
            return read_lines(file_name)

def append_text(file_name: str, contents: str):
    with open(file_name, "a+", encoding="utf-8") as f:
        f.write(contents + "\n")

def __get_file_name_from_dialog() -> str:
    root = tk.Tk()
    root.withdraw()

    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")],
            title="Select a list of usernames",
            parent=root
        )

        return file_path
    finally:
        root.destroy()
