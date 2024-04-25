"""
Script Name: DateHandler.py

Description:
This script provides functions to extract dates from PDF files, filenames, and user input. It also verifies date formats and prompts users for date input.

Usage:
1. Run the script.
2. Depending on the operation, the script may prompt for user input to extract dates or display PDF images.
3. The script verifies and extracts dates from various sources, including PDF text content and filenames.

Author: Roka
Date: 4/10/2024

Dependencies:
- pdfplumber
- tkinter
- datefinder
- PIL
"""

import pdfplumber
from datetime import datetime, timedelta
import re
import fitz
import tkinter as tk
from datefinder import find_dates
from PIL import Image, ImageTk

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def get_screen_position(window_width, window_height):
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return 0, 0

def display_pdf_image_and_prompt_for_date(pdf_path, get_screen_position, prompt_for_date):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(background='black')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    image.thumbnail((screen_width, screen_height))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo)
    label.place(x=0, y=0)

    def close_window():
        small_window.destroy()

    def on_enter(event=None):
        close_window()

    root.bind('<Return>', on_enter)

    window_width, window_height = 500, 375
    x_pos, y_pos = get_screen_position(window_width, window_height)

    small_window = tk.Toplevel()
    small_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    small_window.title("Review Certificate Date")
    small_window.attributes("-topmost", True)

    image.thumbnail((window_width, window_height))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(small_window, image=photo)
    label.pack()

    current_date = prompt_for_date()

    close_window()
    root.destroy()

    return current_date

def verify_date(date_str, attention_threshold=365):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.now()
        if date <= today and date >= today - timedelta(days=365):
            if date <= today - timedelta(attention_threshold):
                print(f"{Color.YELLOW}ATTENTION{Color.RESET}: Certificate is more than {attention_threshold} days old.")
            return True
        else:
            return False
    except ValueError:
        return False

def verify_date_format(date):
    try:
        datetime.strptime(date.strftime('%Y-%m-%d'), '%Y-%m-%d')
        return True
    except ValueError:
        return False

def extract_dates(pdf_path, filename):
    dates_from_pdf = extract_dates_from_pdf(pdf_path)
    if dates_from_pdf:
        return dates_from_pdf
    
    date_from_filename = extract_date_from_filename(filename)
    if date_from_filename:
        return date_from_filename
    return None

def extract_dates_from_pdf(pdf_path):
    latest_date = None
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            extracted_dates = list(find_dates(text))
            if extracted_dates:
                valid_dates = [date.strftime('%Y-%m-%d') for date in extracted_dates if verify_date_format(date)]
                if valid_dates:
                    latest_date = max(valid_dates) if not latest_date else max(latest_date, max(valid_dates))
    return latest_date

def extract_date_from_filename(filename):
    match = re.search(r'\((\d{4}-\d{2}-\d{2})\)', filename)
    if match:
        return match.group(1)
    return None

def prompt_for_date():
    while True:
        user_input = input(f"Enter the date ({Color.RED}DD{Color.RESET}, {Color.GREEN}MM{Color.RESET}-{Color.RED}DD{Color.RESET}, or {Color.BLUE}YYYY{Color.RESET}-{Color.GREEN}MM{Color.RESET}-{Color.RED}DD{Color.RESET}): ").strip()
        components = user_input.split('-')

        if len(components) == 1:
            try:
                day = int(components[0])
                month = datetime.now().month
                year = datetime.now().year
                if 1 <= day <= 31:
                    try:
                        datetime(year, month, day)
                        date = datetime(year, month, day).strftime('%Y-%m-%d')
                        return date
                    except ValueError:
                        print(f"{Color.YELLOW}Invalid date:{Color.RESET} Day is out of range for the current month and year.")
                else:
                    print(f"{Color.YELLOW}Invalid date:{Color.RESET} Day must be between 1 and 31.")
            except ValueError:
                print(f"{Color.YELLOW}Invalid date:{Color.RESET} Please enter a valid number for day.")
        
        elif len(components) == 2:
            try:
                month, day = map(int, components)
                if 1 <= month <= 12:
                    days_in_month = (datetime(datetime.now().year, month+1, 1) - timedelta(days=1)).day
                    if 1 <= day <= days_in_month:
                        year = datetime.now().year
                        date = datetime(year, month, day).strftime('%Y-%m-%d')
                        return date
                    else:
                        print(f"{Color.YELLOW}Invalid date:{Color.RESET} Day is out of range for the current month.")
                else:
                    print(f"{Color.YELLOW}Invalid date:{Color.RESET} Month must be between 1 and 12.")
            except ValueError:
                print(f"{Color.YELLOW}Invalid date:{Color.RESET} Please enter valid numbers for month and day.")
        
        elif len(components) == 3:
            try:
                year, month, day = map(int, components)
                if month in range(1, 13):
                    days_in_month = (datetime(year, month+1, 1) - timedelta(days=1)).day
                    if 1 <= day <= days_in_month:
                        date = datetime(year, month, day).strftime('%Y-%m-%d')
                        return date
                    else:
                        print(f"{Color.YELLOW}Invalid date:{Color.RESET} Day is out of range for the entered month and year.")
                else:
                    print(f"{Color.YELLOW}Invalid date:{Color.RESET} Month must be between 1 and 12.")
            except ValueError:
                print(f"{Color.YELLOW}Invalid date:{Color.RESET} Please enter valid numbers for year, month, and day.")
        
        else:
            print(f"{Color.YELLOW}Invalid date:{Color.RESET} Please enter the date in MM-DD or YYYY-MM-DD format.")

