"""
Script Name: SecTrainingEnforcementHelper.py

Description:
This script automates the renaming of certificate files by adding the individual's name and the date of the certificate. It also copies the last name to the clipboard for convenience.

Usage:
1. Run the script.
2. Enter the last name and first name of the individual. Type 'end' to exit, 'redo' to re-enter a name, and 'get' to auto-extract the name from a predefined workspace.
3. The script will rename the files in the specified workspace directory based on the provided names and move them to a record buffer directory.
4. It provides reminders to update Excel sheets and allows manual flushing of the record buffer.

Author: Roka
Date: 4/10/2024

Dependencies:
- Helper.Format.Style.Color
- Helper.Format.Style.print_terminal_line
- Helper.Format.Normalization.normalize_filename
- Helper.DateHandler.extract_dates
- Helper.DateHandler.verify_date
- Helper.DateHandler.display_pdf_image_and_prompt_for_date
- Helper.DateHandler.get_screen_position
- Helper.DateHandler.prompt_for_date
- Helper.FilePlacement.convert_image_to_pdf
- Helper.FilePlacement.move_files_to_buffer
- Helper.FilePlacement.flush_files
"""

import os
import subprocess, sys
from Helper.Format.Style import Color, print_terminal_line
from Helper.Format.FileUtilities import *
from Helper.DateHandler import *
from Helper.FileMover import *

def copy2clip(txt):
    cmd = 'clip' if sys.platform.startswith('win') else 'pbcopy'
    subprocess.Popen([cmd], stdin=subprocess.PIPE, text=True).communicate(txt)

def get_names(workspace_path):
    while True:
        print_terminal_line()
        last_name = input(f"Enter {Color.CYAN}last{Color.RESET} name: ").strip().lower()

        if last_name == 'end':
            return 'end', 'end'

        elif last_name == 'get':
            last_name, first_name = extract_username(workspace_path)
            if first_name is not None and last_name is not None:
                return last_name, first_name
            else:
                continue

        elif last_name == 'redo':
            continue

        first_name = input(f"Enter {Color.CYAN}first{Color.RESET} name: ").strip().lower()

        if first_name == 'get':
            last_name, first_name = extract_username(workspace_path)
            if first_name is not None and last_name is not None:
                return last_name, first_name
            else:
                continue

        elif first_name == 'redo':
            continue

        return last_name, first_name

def rename_files(folder_path, first_name, last_name):
    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"Folder {Color.YELLOW}'{folder_path}'{Color.RESET} does not exist.")
        return

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(folder_path, filename)
                pdf_filename = os.path.splitext(filename)[0] + ".pdf"
                pdf_path = os.path.join(folder_path, pdf_filename)
                convert_image_to_pdf(image_path, pdf_path)
                os.remove(image_path)
            elif filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(folder_path, filename)
            else:
                continue
            
            base_filename, extension = os.path.splitext(filename)
            base_filename = normalize_filename(base_filename)
            
            latest_certificate_date = extract_dates(pdf_path, filename)
            if latest_certificate_date:
                if not verify_date(latest_certificate_date, 7):
                    print(f"{Color.YELLOW}ATTENTION:{Color.RESET} Invalid date in {Color.RED}{filename}{Color.RESET}. Displaying for review.")
                    latest_certificate_date = display_pdf_image_and_prompt_for_date(pdf_path, get_screen_position, prompt_for_date)
            else:
                print(f"{Color.YELLOW}ATTENTION:{Color.RESET} No date found in {Color.RED}{filename}{Color.RESET}. Displaying for review.")
                latest_certificate_date = display_pdf_image_and_prompt_for_date(pdf_path, get_screen_position, prompt_for_date)

            new_filename = f"{last_name}, {first_name} - {base_filename} ({latest_certificate_date}){extension}"
            new_path = os.path.join(folder_path, new_filename)
            
            try:
                os.rename(pdf_path, new_path)
                print(f"Renamed: {Color.RED}{filename}{Color.RESET} to {Color.GREEN}{new_filename}{Color.RESET}")
            except FileNotFoundError:
                print(f"File not found: {filename}")
            except OSError as e:
                print(f"{Color.YELLOW}Error{Color.RESET} renaming {Color.RED}{filename}{Color.RESET}: {e}")


def main():
    workspace_path = os.path.join(os.getcwd(), 'PyScripts', 'TempDocs')
    record_buffer_path = os.path.join(os.getcwd(), 'PyScripts', 'RecordBuffer')
    security_training_records_path = os.getenv('DESTINATION')

    print(f"{Color.YELLOW}(Type 'end' to exit, 'redo' to re-enter name, and 'get' to auto-extract name.){Color.RESET}")
    while True:
        last_name, first_name = get_names(workspace_path)
        if first_name is None or last_name is None:
            continue

        if last_name.lower() in {'end', 'flush'} or first_name.lower() in {'end', 'flush'}:
            break

        last_name = format_name(last_name)
        first_name = format_name(first_name)

        copy2clip(last_name)
        
        rename_files(workspace_path, first_name, last_name)
        move_files_to_buffer(workspace_path, record_buffer_path)
        print(f"{Color.YELLOW}Reminder:{Color.RESET} Update {Color.GREEN}Excel{Color.RESET} Sheets - {Color.CYAN}Last{Color.RESET} Name Copied")
    
    flush_buffer_bool = yes_no_input(f"{Color.YELLOW}Do you want to flush the Record Buffer?:{Color.RESET} ")
    if flush_buffer_bool is True:
        manual_mode_bool = yes_no_input(f"{Color.YELLOW}Manual flush?:{Color.RESET} ")
        flush_files(record_buffer_path, security_training_records_path, manual_mode_bool)

if __name__ == "__main__":
    #main()
    print(os.join(os.getcwd(), 'PyScripts', 'TempDocs') )
