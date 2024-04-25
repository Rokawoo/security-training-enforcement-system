"""
Script Name: Style.py

Description:
This script provides functions for printing colored terminal output and drawing horizontal lines.

Usage:
1. Utilize the provided functions to print colored text and draw horizontal lines in the terminal.

Author: Roka
Date: 4/10/2024

Dependencies:
- os
"""

import os

# ANSI color codes
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def print_terminal_line():
    terminal_width = os.get_terminal_size().columns
    line = "-" * terminal_width
    print(f"{Color.MAGENTA}{line}{Color.RESET}")