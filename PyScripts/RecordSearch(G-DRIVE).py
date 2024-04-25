"""
Script Name: RecordSearch(G-DRIVE).py

Description:
This script searches for files matching a specific pattern within a directory structure and displays them with colorized filenames. It also allows users to search for files based on last name and first name.

Usage:
1. Run the script.
2. Enter the last name and first name of the individual you are searching for. Type 'end' to exit or 'redo' to enter names again.
3. The script will search for files matching the provided names within the specified directory.
4. It displays the matching files with colorized filenames. Expired files are marked with a warning.
5. Users can sort files found in the top directory manually.

Author: Roka
Date: 4/10/2024

Dependencies:
- Helper.DateHandler.verify_date
- Helper.DateHandler.extract_date_from_filename
- Helper.Format.Style.Color

"""

import os
import re
from dotenv import load_dotenv
from Helper.DateHandler import verify_date, extract_date_from_filename
from Helper.Format.Style import Color

load_dotenv()

def colorize_filename(filename):
    filename_without_extension = os.path.splitext(filename)[0]

    pattern = r'^(.*?) - ([^(]*?)\((.*?)\)(.*?)$'
    match = re.match(pattern, filename_without_extension)
    if match:
        before_dash = match.group(1).strip()
        within_parentheses = match.group(2).strip()
        #after_parentheses = match.group(3).strip()
        before_dash_colored = f"{Color.RED}{before_dash}{Color.RESET}"
        within_parentheses_colored = f"{Color.GREEN}{within_parentheses}{Color.RESET}"
        #after_parentheses_colored = f"{Color.BLUE}{after_parentheses}{Color.RESET}"
        after_parentheses_colored = f"{Color.BLUE}{extract_date_from_filename(filename)}{Color.RESET}"
        return f"{before_dash_colored} - {within_parentheses_colored} ({after_parentheses_colored})"
    else:
        return filename_without_extension

def find_files_with_pattern(parent_dir, pattern):
    matches = []
    for file in os.listdir(parent_dir):
        if file.startswith(pattern):
            matches.append((os.path.join(parent_dir, file), True))
    for root, dirs, files in os.walk(parent_dir):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            for file in os.listdir(dir_path):
                if file.startswith(pattern):
                    matches.append((os.path.join(dir_path, file), False))
    return matches

def get_names():
    last_name = input(f"{Color.YELLOW}Last name:{Color.RESET} ").capitalize().strip()
    if last_name.lower() == "end":
        return None, None
    elif last_name.lower() == "redo":
        return get_names()
    
    first_name = input(f"{Color.YELLOW}First name:{Color.RESET} ").capitalize().strip()
    if first_name.lower() == "end":
        return None, None
    elif first_name.lower() == "redo":
        return get_names()

    return last_name, first_name

def main():
    parent_dir = os.getenv('DESTINATION')
    print(parent_dir)
    print("You are searching:", parent_dir)
    
    while True:
        print("\nEnter Search Target's...")
        last_name, first_name = get_names()
        if last_name is None or first_name is None:
            print("Exiting program...")
            break

        patterns = (f"{last_name}, {first_name}", f"{first_name}.{last_name}", f"{first_name[0]}.{last_name}")
        found_files = []

        for pattern in patterns:
            found_files.extend(find_files_with_pattern(parent_dir, pattern))


        if found_files:
            print("Found matching files:")
            for file, is_direct in found_files:
                file = os.path.basename(file)
                if verify_date(extract_date_from_filename(file)):
                    if is_direct:
                        print(f"In top dir: {colorize_filename(file)}, please sort it.")
                    else:
                        print(colorize_filename(file))
                else:
                    print(f"{Color.YELLOW}Expired{Color.RESET}: {colorize_filename(file)}")
        else:
            print("No files matching the pattern were found.")

if __name__ == "__main__":
    main()
