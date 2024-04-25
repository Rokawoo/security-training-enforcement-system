"""
Script Name: FileMover.py

Description:
This script facilitates the movement of files between directories based on predefined mappings. It offers options for flushing files and logging operations.

Usage:
1. Run the script.
2. Depending on the operation:
    a. For moving files based on mappings, no user input is required.
    b. For flushing files, users can choose manual mode for confirmation prompts.
3. The script logs operations for future reference.

Author: Roka
Date: 4/10/2024

Dependencies:
- shutil
- logging
- Helper.Format.Style.Color
"""

import os
import shutil
import logging

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def yes_no_input(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ('yes', 'y'):
            return True
        elif response in ('no', 'n'):
            return False
        else:
            print(f"Please enter {Color.GREEN}'yes'{Color.RED} or {Color.RESET}'no'{Color.RESET}.")

def move_files_to_buffer(workspace_path, buffer_path):
    folder_name_mapping = {
        "security awareness training": "Security Awareness Training",
        "sensitive data training": "Sensitive Data at Rhoads Training - Records",
        "pii training": "PII Training - Records",
        "level 1 antiterrorism": "Level 1 Antiterrorism Awareness Training - Records",
        "cui training": "DoD Mandatory CUI Training - Records",
        "dod annual security awareness": "DoD Annual Security Refresher for Cleared Personnel"
    }

    for root, _, files in os.walk(workspace_path):
        for filename in files:
            base_filename_lower = filename.lower()
            matched_folder_name = None
            for standard_name, folder_name in folder_name_mapping.items():
                if standard_name in base_filename_lower:
                    matched_folder_name = folder_name
                    break
            
            if matched_folder_name:
                source_file_path = os.path.join(root, filename)
                destination_folder_path = os.path.join(buffer_path, matched_folder_name)
                if not os.path.exists(destination_folder_path):
                    os.makedirs(destination_folder_path)
                
                try:
                    os.rename(source_file_path, os.path.join(destination_folder_path, filename))
                    print(f"Moved: {Color.MAGENTA}{filename}{Color.RESET} to {Color.BLUE}{matched_folder_name}{Color.RESET} folder.")
                except OSError as e:
                    print(f"{Color.YELLOW}Error{Color.RESET} moving {Color.MAGENTA}{filename}{Color.RESET} to {Color.BLUE}{matched_folder_name}{Color.RESET} folder. folder: {e}")
            else:
                print(f"{Color.YELLOW}ATTENTION{Color.RESET}: No matching folder for {Color.RED}{filename}{Color.RESET}.")

def flush_files(source_top_dir, dest_top_dir, manual_mode=False):
    """
    Move files from source directory to destination directory.

    Args:
    - source_top_dir (str): Path to the source top directory.
    - dest_top_dir (str): Path to the destination top directory.
    - manual_mode (bool): Flag indicating whether to run in manual mode.

    Returns:
    None
    """

    logging.basicConfig(filename='move_files.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        active_dir = None
        for root, dirs, files in os.walk(source_top_dir):
            for file in files:
                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(source_file, source_top_dir)
                dest_file = os.path.join(dest_top_dir, relative_path)

                source_dirname, source_filename = os.path.split(source_file)
                dest_dirname, dest_foldername = os.path.split(dest_file)

                if source_dirname != active_dir:
                    active_dir = source_dirname
                    print(f"{Color.YELLOW}Active folder: {active_dir}{Color.RESET}")
                
                if manual_mode:
                    #response = yes_no_input(f"Move {Color.RED}{source_filename}{Color.RESET} from {Color.MAGENTA}{source_dirname}{Color.RESET} to {Color.GREEN}{dest_foldername}{Color.RESET} in {Color.BLUE}{dest_dirname}{Color.RESET}? (y/n): ")
                    response = yes_no_input(f"Move {Color.RED}{source_filename}{Color.RESET} from {Color.BLUE}{source_dirname}{Color.RESET} to\n{Color.GREEN}{dest_foldername}{Color.RESET} in {Color.BLUE}{dest_dirname}{Color.RESET}? (y/n): ")
                    if response is False:
                        logging.info(f"Skipped moving {Color.MAGENTA}{source_filename}{Color.RESET} from {Color.MAGENTA}{source_dirname}{Color.RESET} to {Color.BLUE}{dest_foldername}{Color.RESET} in {Color.BLUE}{dest_dirname}{Color.RESET}")
                        continue
                
                dest_dir = os.path.dirname(dest_file)
                if not os.path.exists(dest_dir):
                    raise FileNotFoundError(f"{Color.RED}No matching directory found in destination:{Color.RESET} {Color.BLUE}{dest_dir}{Color.RESET}. Check File Names.")
                
                shutil.move(source_file, dest_file)
                logging.info(f"Moved {source_file} to {dest_file}")
                if not manual_mode:
                    print(f"Moved {Color.RED}{source_filename}{Color.RESET} from {Color.BLUE}{source_dirname}{Color.RESET} to\n{Color.GREEN}{dest_foldername}{Color.RESET} in {Color.BLUE}{dest_dirname}{Color.RESET}")
                

        print(f"{Color.YELLOW}Flush Complete.{Color.RESET}")

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise