#!/usr/bin/env python3
#
# Title: RhoadsSEC - RecordNameFormatter
# Description: Renames files in a specified folder with the format "Last Name, First Name - Filename (Date)". 
# Author: Roka
# Date: 4/5/2024

# Note!!!: Set working directory in folder_path var.

import os
import datetime

def format_name(name):
    return name.capitalize()

def rename_files(folder_path, first_name, last_name):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"Folder '{folder_path}' does not exist.")
        return

    for filename in files:
        base_filename, extension = os.path.splitext(filename)
        new_filename = f"{last_name}, {first_name} - {base_filename} ({current_date}){extension}"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)
        
        try:
            os.rename(old_path, new_path)
            print(f"Renamed {filename} to {new_filename}")
        except Exception as e:
            print(f"Error renaming {filename}: {e}")

def main():
    folder_path = "./Temp Docs"
    
    while True:
        last_name = input("Enter last name: (type 'end' to exit): ")
        if last_name.lower() == 'end':
            break
        
        first_name = input("Enter first name: ")
        if first_name.lower() == 'end':
            break
        
        first_name = format_name(first_name)
        last_name = format_name(last_name)
        
        rename_files(folder_path, first_name, last_name)

if __name__ == "__main__":
    main()
