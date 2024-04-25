"""
Script Name: FileUtilities.py

Description:
This script provides various utility functions for file manipulation, including extracting usernames and normalizing filenames.

Usage:
1. Run the script.
2. Utilize the provided functions for extracting usernames, normalizing filenames, and converting images to PDFs.

Author: Roka
Date: 4/10/2024

Dependencies:
- os
- re
- PIL (Pillow)
- reportlab
"""

import os
import re
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def extract_username(workspace_path):
    files = [f for f in os.listdir(workspace_path) if os.path.isfile(os.path.join(workspace_path, f))]
    
    for file_name in files:
        pattern = r'([A-Za-z]+)\s([A-Za-z]+)\s-\s.*'
        match = re.search(pattern, file_name)
        
        if match:
            first_name, last_name = match.group(1).capitalize(), match.group(2).capitalize()
            while True:
                use_extracted_name = input(f"{Color.YELLOW}Use{Color.RESET}: {Color.CYAN}{last_name}{Color.RESET}, {Color.CYAN}{first_name}{Color.RESET}? ({Color.GREEN}yes{Color.RESET}/{Color.RED}no{Color.RESET}/{Color.YELLOW}switch{Color.RESET}): ").strip().lower()
                if use_extracted_name in ('yes', 'y'):
                    return last_name, first_name
                elif use_extracted_name in ('switch', 's'):
                    return first_name, last_name
                elif use_extracted_name in ('no', 'n'):
                    break
                else:
                    print(f"Please enter {Color.GREEN}'yes'{Color.RED}, {Color.RESET}'no'{Color.RESET}, or {Color.YELLOW}'switch'{Color.RESET}.")
    print(f"{Color.RED}No Name Found{Color.RESET}")                
    return None, None

def extract_basename(filename):
    pattern = r'-\s*([^(-]+)\s*\('
    match = re.search(pattern, filename)
    if match:
        return match.group(1).strip()
    
    pattern = r'(?<=-)\s*([^0-9]+)'
    match = re.search(pattern, filename)
    if match:
        return match.group(1).strip()
    
    return filename

def normalize_filename(base_filename):
    base_filename_lower = base_filename.lower().strip()
    
    switch = {
        "security awareness training course": "Security Awareness Training Course",
        "sensitive data training": "Sensitive Data Training",
        "pii": "PII Training",
        "identifying and safeguarding personally identifiable information": "PII Training",
        "antiterrorism": "Level 1 Antiterrorism Awareness Training",
        "level 1 antiterrorism": "Level 1 Antiterrorism Awareness Training",
        "antiterrorism level 1": "Level 1 Antiterrorism Awareness Training",
        "dod mandatory controlled unclassified information": "CUI Training",
        "cui": "CUI Training",
        "dod annual security awareness": "DoD Annual Security Awareness Refresher"
    }
    
    matches = [value for key, value in switch.items() if key in base_filename_lower]
    
    return matches[0] if matches else extract_basename(base_filename)

def format_name(name):
    return name.capitalize()

def convert_image_to_pdf(image_path, pdf_path):
    try:
        image = Image.open(image_path)
        pdf_canvas = canvas.Canvas(pdf_path, pagesize=image.size)
        pdf_canvas.drawImage(image_path, 0, 0)
        pdf_canvas.save()
    except Exception as e:
        print(f"{Color.RED}An error occurred while converting{Color.RESET} {image_path} {Color.RED}to PDF{Color.RESET}: {e}")

def yes_no_input(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ('yes', 'y'):
            return True
        elif response in ('no', 'n'):
            return False
        else:
            print(f"Please enter {Color.GREEN}'yes'{Color.RED} or {Color.RESET}'no'{Color.RESET}.")
