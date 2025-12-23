"""
TikTok Downloader Tool

Bot Name: t.me/TikTok_DownloaderiBot
Developer: Abdizamed Mohamed 
Contact: https://zamdevio.t.me
Version: 1.0.23
Created Time: 2024-08-15
Last Updated: 2025-12-24

This script allows users to download TikTok videos using a Unix environment.
Developed by Abdizamed Mohamed to provide a fast and reliable backend for the TikTok Downloader Bot.
"""

# =======================
# Third-Party Module Imports
# =======================
import requests

# =======================
# Standard Library Imports
# =======================
import json
import os
import subprocess
import sys
import tempfile
import signal
from time import sleep
import random
import traceback
import re
import unicodedata
from zipfile import ZipFile
from datetime import datetime as WAQTIGA

# =======================
# COLORS 💫
# =======================
BINK = '\033[1;35m'
BLUE = '\033[1;34m'
BLUE1 = '\033[1;38;5;32m'
BOLD = '\033[1m'
CYAN = '\033[1;38;5;51m'
GRAY = '\033[1;30m'
GREEN = '\033[1;32m'
GREEN1 = '\033[1;38;5;46m'
GREEN2 = '\033[1;38;5;47m'
GREEN3 = '\033[1;38;5;48m'
RED = '\033[1;31m'
RESET = '\033[0m'
WHITE = '\033[47m'
YELLOW = '\033[1;33m'

ANDROID_DOWNLOAD_DIR = '/sdcard/DCIM/TIKTOK_DOWNLOADER'

# Check if the script is running inside the Termux environment by looking at the current working directory
if '/data/data/com.termux/files/home' in os.getcwd():
    try:
        os.makedirs(ANDROID_DOWNLOAD_DIR, exist_ok=True)

        with tempfile.NamedTemporaryFile(dir=ANDROID_DOWNLOAD_DIR):
            pass

        default_download_dir = ANDROID_DOWNLOAD_DIR

    except (OSError, PermissionError) as e:
        """
        If there is an error while creating the download directory or if the directory
        is not writable (for example, due to permission issues), we catch the error 
        and print an appropriate message. Instead of stopping the script, we fall back 
        to using the current working directory as the download base.
        """
        print(f"Error: Could not set up the download directory. Details: {e}")
        default_download_dir = os.getcwd()

else:
    default_download_dir = os.getcwd()

download_base = default_download_dir

ToolDir = os.path.join(os.path.expanduser("~"), ".TikTokDownloader")
os.makedirs(ToolDir, exist_ok=True)

config_file = f"{ToolDir}/config_file.txt"
FirstDir = f"{ToolDir}/FirstDir.txt"

FirtTime = f"{ToolDir}/FirtTime.txt"

def format_script_name(script_name, max_length=12):
    """
    This function formats the script name to ensure it doesn't exceed a specified length. If the script name is 
    longer than the maximum length, it trims it from the left, adding ".." to indicate truncation. The formatted 
    string also includes a default directory path and instructions to set a new directory.

    Args:
        script_name (str): The name of the script to format.
        max_length (int, optional): The maximum allowed length for the script name. Defaults to 12.

    Returns:
        str: The formatted script name with a path to set a new directory.
    """
    if len(script_name) > max_length:
        return ".." + script_name[-max_length:] + f" /path/to/download_dir {BLUE}To set new Dir{BLUE}│"
    else:
        return script_name + f" /path/to/download_dir {BLUE}To Set New Dir  {BLUE}│"
    return script_name.ljust(max_length).rstrip()
def usage():
    """
    This function prints the usage instructions for running the script. It formats the script name using 
    `format_script_name()` and outputs a message detailing how to use the script with the required arguments.

    Side Effects:
        - Prints the usage message to the console.
    """
    global script_name
    formatted_script_name = format_script_name(script_name)
    
    print(f"{BLUE}╭────────────────────────── <{WHITE}{GRAY} Download Dir {WHITE}{RESET}{BLUE}> ─────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}#{GRAY}】{BLUE}Use {GREEN2}python3 {formatted_script_name}")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")


def load_download_dir():
    """
    This function loads the download directory path from a configuration file. If the configuration file exists,
    it attempts to read and validate the stored path. If the stored path is invalid or the file does not exist, 
    it falls back to a default directory.

    Returns:
        str: The directory path used for downloading, either from the config file or the default directory.
    """
    global download_base

    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            path = file.read().strip()
            if os.path.exists(path):
                download_base = path
            else:
                print(f"{BLUE}╭────────────────────────── <{WHITE}{GRAY} Download Dir {WHITE}{RESET}{BLUE}> ─────────────────────────╮")
                print(f"{BLUE}│ {RED}Stored path in config file does not exist. {GREEN2}Using default directory. {BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
                download_base = default_download_dir
    else:
        print(f"{BLUE}╭────────────────────────── <{WHITE}{GRAY} Download Dir {WHITE}{RESET}{BLUE}> ─────────────────────────╮")
        print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{YELLOW}Config file not found. Using default directory.                {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        download_base = default_download_dir
    
    return download_base

def format_dir_path(dir_path, max_length=33, complete_length=36):
    """
    This function formats the directory path by ensuring that it does not exceed the specified maximum length. 
    If the path is too long, it truncates it and adds "..." at the beginning. If the path is shorter than the 
    required length, it pads it with spaces.

    Args:
        dir_path (str): The directory path to format.
        max_length (int, optional): The maximum length for the directory path. Defaults to 33.
        complete_length (int, optional): The length to which the path should be padded if it's too short. Defaults to 36.

    Returns:
        str: The formatted directory path.
    """
    if len(dir_path) > max_length:
        return "..." + dir_path[-max_length:]
    elif len(dir_path) < complete_length:
        return dir_path.ljust(complete_length)
    return dir_path

def set_download_dir(path):
    """
    This function sets the download directory for storing files. It verifies the validity of the provided
    directory path and attempts to set it as the base for download. If the directory is valid, it updates
    the configuration file and creates a file to track if it is the first time the directory is set. 

    Args:
        path (str): The path to the directory where downloads should be stored.

    Side Effects:
        - Updates the global variable `download_base` with the provided directory path.
        - Creates or updates a configuration file to store the directory path.
        - Logs any errors if the directory does not exist or if permissions are insufficient.
        - Displays a message indicating the result (success or error) to the user.
    """
    global download_base
    global FirtTime

    if os.path.exists(path):
        download_base = path
        try:
            with tempfile.NamedTemporaryFile(dir=path):
                pass

            with open(config_file, 'w') as file:
                file.write(download_base)
            if not os.path.exists(FirtTime):
                  with open(FirtTime, mode='w') as file:
                       file.write("Hello World")
            formatted_dir = format_dir_path(download_base)
            print(f"{BLUE}╭────────────────────────── <{WHITE}{GRAY} Download Dir {WHITE}{RESET}{BLUE}> ─────────────────────────╮")
            print(f"{BLUE}│ {GRAY}【{RESET}#{GRAY}】{GREEN2}Download Directory set to: {formatted_dir}{BLUE}│")
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        except PermissionError as e:
            log_error(e)
            print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
            print(f"{BLUE}│ {RED}Error: {BINK}Make sure you have the permissions for the Downloaded Dir   {BLUE}│")
            print(f"{BLUE}│ {GREEN3}Logs saved as tiktok_downloader_error_logs.txt                       {BLUE}│")
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            sleep(2)
    else:

        print(f"{BLUE}╭──────────────────────────── <{WHITE}{GRAY} Error {WHITE}{RESET}{BLUE}> ──────────────────────────────╮")
        print(f"{BLUE}│ {GRAY}【{RED}#{GRAY}】{RED}Invalid path. Directory does not exist                         {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

def get_ip_address():
    """
    This function retrieves the public IP address of the user by making an HTTP GET request to 
    the 'api.ipify.org' service, which returns the IP address in JSON format.

    It handles any potential request errors and returns either the retrieved IP address or an error message.
    
    Returns:
        str: The user's public IP address, or an error message if the request fails.
    """
    try:
        response = requests.get('http://api.ipify.org?format=json')
        ip = response.json().get('ip', 'Unknown')
        return f'{ip}'
    except requests.RequestException:
        return f'{RED}Unable to retrieve IP{BLUE}                         │'
def format_ip_address(ip_address, max_length=35):
    """
    This function formats the IP address to fit within a specified length for display purposes.
    If the IP address exceeds the max length, it truncates the string and appends '...' to indicate 
    that the string was shortened.

    Args:
        ip_address (str): The IP address to be formatted.
        max_length (int, optional): The maximum allowed length of the formatted string (default is 35).

    Returns:
        str: The formatted IP address, either truncated or padded to fit the specified length.
    """
    if len(ip_address) > max_length:
        return ip_address[:max_length-3] + "..."
    return ip_address.ljust(max_length) + f"           {BLUE}│"

def format_time(time_str, max_length=12):
    """
    This function formats the time string to fit within a specified length for display purposes.
    If the time string exceeds the max length, it truncates the string and appends '...' to indicate 
    that the string was shortened.

    Args:
        time_str (str): The time string to be formatted.
        max_length (int, optional): The maximum allowed length of the formatted string (default is 12).

    Returns:
        str: The formatted time string, either truncated or padded to fit the specified length.
    """
    if len(time_str) > max_length:
        return time_str[:max_length-3] + "..."
    return time_str.ljust(max_length)

def format_date(date_str, max_length=20):
    """
    This function formats the date string to fit within a specified length for display purposes.
    If the date string exceeds the max length, it truncates the string and appends '...' to indicate 
    that the string was shortened.

    Args:
        date_str (str): The date string to be formatted.
        max_length (int, optional): The maximum allowed length of the formatted string (default is 20).

    Returns:
        str: The formatted date string, either truncated or padded to fit the specified length.
    """
    if len(date_str) > max_length:
        return date_str[:max_length-3] + "..."
    return date_str.ljust(max_length)

def header(do_clear=True):
    """
    This function is responsible for displaying the header section of the program's console output.
    It clears the screen, retrieves the user's IP address, current time, and date, then formats 
    and displays these details in a structured and visually appealing format. The header includes 
    developer and tool information, as well as details about the user's current environment, such as 
    their IP address, current time, and date.

    The function performs the following tasks:
    1. Clears the screen to prepare for fresh output.
    2. Retrieves and formats the user's IP address, current time, and current date.
    3. Displays a custom ASCII art logo and relevant developer information.
    4. Displays the formatted user's IP address, time, and date in the terminal.
    
    The information displayed provides the user with a clear and engaging introduction to the tool,
    as well as a reminder of key information about the tool and its version.
    """
    if do_clear:
        clear_screen()
    query = get_ip_address()
    time = WAQTIGA.now().strftime("%I:%M:%S %p")
    date = WAQTIGA.now().strftime("%d/%B/%Y")
    if not 'Unable' in query:
      formatted_query = format_ip_address(query)
    else:
         formatted_query = query
    formatted_time = format_time(time)
    formatted_date = format_date(date)
    print(f"{BLUE}╭───────────────────── <{WHITE}{GRAY} CODING BY - ABDISAMED {RESET}{BLUE}> ─────────────────────╮")
    print(f"{BLUE}│ {RED}● {YELLOW}● {GREEN1}● {BLUE}                                                              {BLUE}│")
    print(f"{BLUE}│                                                                     {BLUE}│")
    print(f"{BLUE}│{GREEN1}████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗     █████╗ ██████╗ ██╗{BLUE}│")
    print(f"{BLUE}│{GREEN1}╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝    ██╔══██╗██╔══██╗██║{BLUE}│")
    print(f"{BLUE}│{GREEN2}   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝     ███████║██████╔╝██║{BLUE}│")
    print(f"{BLUE}│{GREEN2}   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗     ██╔══██║██╔═══╝ ██║{BLUE}│")
    print(f"{BLUE}│{GREEN3}   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗    ██║  ██║██║     ██║{BLUE}│")
    print(f"{BLUE}│{GREEN3}   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝     ╚═╝{BLUE}│")
    print(f'{BLUE}╭─────────────────────────── <{WHITE}{GRAY} DEV INFO {RESET}{BLUE}> ────────────────────────────╮')
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{YELLOW} DEVELOPER     {RED}➤{GREEN2} Abdisamed Mohamed                             {BLUE}│")
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{YELLOW} VERSION       {RED}➤{GREEN2} 1.0.23                                        {BLUE}│")
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{YELLOW} TELEGRAM      {RED}➤{GREEN2} https://zamdevio.t.me                         {BLUE}│")
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{YELLOW} TELEGRAM BOT  {RED}➤{GREEN2} https://t.me/TikTok_DownloaderiBot            {BLUE}│")
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{YELLOW} GITHUB        {RED}➤{GREEN2} https://github.com/zamdevio                   {BLUE}│")
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{YELLOW} WEBSITE       {RED}➤{GREEN2} clipx.zamdev.dev                              {BLUE}│")
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{YELLOW} TOOL'S NAME   {RED}➤{BINK} TikTok API{RED}                                    {BLUE}│")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯{RESET}")
    print(f'{BLUE}╭─────────────────────────── <{WHITE}{GRAY} YOUR INFO {RESET}{BLUE}> ───────────────────────────╮')
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{CYAN}YOUR IP        {RED}➤{BLUE1} {formatted_query}")
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{CYAN}TODAY TIME     {RED}➤{BLUE1} {formatted_time}                                  {BLUE}│")
    print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{CYAN}TODAY DATE     {RED}➤{BLUE1} {formatted_date}                          {BLUE}│")
    print(f"╰─────────────────────────────────────────────────────────────────────╯{RESET}")

def clear_screen():
    """
    This function clears the terminal screen, allowing for a clean output display.
    It checks the operating system in use: on Windows ('nt'), it uses the 'cls' command, 
    and on other systems (e.g., Linux or macOS), it uses the 'clear' command. This is useful for 
    resetting the console display between different program outputs.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def invalid_link():
    """
    This function is called when the input link is invalid or when a video is not found. 
    It prints an error message to the terminal and provides information to the user that 
    the video might be private or blocked. After displaying the error, the program exits to 
    prevent further processing of invalid data.
    """
    print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{RED}Video not found. Maybe the video is private or blocked.        {BLUE}│")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    sys.exit()

def invalid_download_url(message):
    """
    Prints a styled message explaining why a download URL is invalid or empty.
    """
    print(f"{BLUE}╭────────────────────────── <{WHITE}{GRAY} Download Dir {WHITE}{RESET}{BLUE}> ─────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}#{GRAY}】{RED}{message:<62}{BLUE} │")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

def ensure_subdir(base_dir, *parts):
    path = os.path.join(base_dir, *parts)
    os.makedirs(path, exist_ok=True)
    return path

def read_unlimited_token():
    token_path = os.path.join(os.getcwd(), ".unlimited")
    if not os.path.isfile(token_path):
        return None, None
    try:
        with open(token_path, "r") as handle:
            raw = handle.read().strip()
            if not raw:
                return None, "empty"
            parts = raw.split()
            if len(parts) != 1:
                return None, "invalid"
            return parts[0], None
    except OSError:
        return None, "unreadable"

def fetch_contact_info():
    try:
        response = requests.get("https://clipx.zamdev.workers.dev/")
        data = response.json()
        return data.get("contact") or {}
    except Exception:
        return {}

def format_timestamp_ms(value):
    try:
        ms = int(value)
        return WAQTIGA.fromtimestamp(ms / 1000).strftime("%d/%m/%Y, %H:%M:%S")
    except Exception:
        return value

def format_window_ms(value):
    try:
        ms = int(value)
        seconds = ms / 1000
        if seconds >= 3600 and seconds % 3600 == 0:
            return f"{int(seconds // 3600)}h"
        if seconds >= 60 and seconds % 60 == 0:
            return f"{int(seconds // 60)}m"
        return f"{int(seconds)}s"
    except Exception:
        return value

def get_rate_value(info, *keys):
    for key in keys:
        if key in info and info[key] is not None:
            return info[key]
    return None

def show_rate_limit_box(rate_limit_info):
    unlimited = bool(get_rate_value(rate_limit_info, "unlimited"))
    allowed = get_rate_value(rate_limit_info, "allowed")
    per_remaining = get_rate_value(rate_limit_info, "remaining")
    per_limit = get_rate_value(rate_limit_info, "limit")
    per_reset = get_rate_value(rate_limit_info, "reset_time", "resetTime")
    per_window = get_rate_value(rate_limit_info, "window_ms", "windowMs")
    daily_remaining = get_rate_value(rate_limit_info, "daily_remaining", "dailyRemaining")
    daily_limit = get_rate_value(rate_limit_info, "daily_limit", "dailyLimit")
    daily_reset = get_rate_value(rate_limit_info, "daily_reset_time", "dailyResetTime")
    daily_window = get_rate_value(rate_limit_info, "daily_window_ms", "dailyWindowMs")

    if unlimited:
        allowed = True
        per_remaining = per_limit = daily_remaining = daily_limit = "∞"
        per_reset = daily_reset = per_window = daily_window = "∞"

    print(box_header("Rate Limits"))
    print(format_kv_line("Unlimited", unlimited))
    if allowed is not None:
        print(format_kv_line("Allowed", allowed))
    if per_limit is not None or per_remaining is not None:
        if per_limit is not None:
            print(format_kv_line("Per Minute Limit", per_limit))
        if per_remaining is not None:
            print(format_kv_line("Per Minute Remaining", per_remaining))
        if per_reset is not None:
            print(format_kv_line("Per Minute Reset", format_timestamp_ms(per_reset)))
        if per_window is not None:
            print(format_kv_line("Per Minute Window", format_window_ms(per_window)))
    if daily_limit is not None or daily_remaining is not None:
        if daily_limit is not None:
            print(format_kv_line("Daily Limit", daily_limit))
        if daily_remaining is not None:
            print(format_kv_line("Daily Remaining", daily_remaining))
        if daily_reset is not None:
            print(format_kv_line("Daily Reset", format_timestamp_ms(daily_reset)))
        if daily_window is not None:
            print(format_kv_line("Daily Window", format_window_ms(daily_window)))
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

def token_status():
    token, err = read_unlimited_token()
    if token:
        return "Set"
    if err:
        return "Invalid"
    return "Not set"

def set_unlimited_token():
    print(box_header("Set Unlimited Token"))
    contact_info = fetch_contact_info()
    contact_email = contact_info.get("email") or "clipx@zamdev.dev"
    print(format_kv_line("Info", f"Contact {contact_email} to request a token"))
    if contact_info.get("message"):
        print(format_kv_line("Note", contact_info.get("message")))
    print(format_kv_line("Input", "Paste your token to set it or press Enter to go back"))
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    existing_token, token_err = read_unlimited_token()
    if existing_token:
        print(box_header("Unlimited Token"))
        print(format_kv_line("Status", "Token already set"))
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        confirm = input(f"  {BLUE}Overwrite token? (y/N) {RESET}").strip().lower()
        if confirm != "y":
            return
    elif token_err:
        print(box_header("Unlimited Token"))
        print(format_kv_line("Status", "Current .unlimited is invalid"))
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        confirm = input(f"  {BLUE}Overwrite token? (y/N) {RESET}").strip().lower()
        if confirm != "y":
            return
    token = input(f"  {BLUE}╰─>{RESET} ").strip()
    if not token:
        return
    if len(token.split()) != 1:
        invalid_download_url("Token is invalid. Please paste a single token.")
        return
    try:
        with open(".unlimited", "w") as handle:
            handle.write(token)
        print(box_header("Unlimited Token"))
        print(format_kv_line("Status", "Token saved to .unlimited"))
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    except OSError:
        invalid_download_url("Could not write .unlimited file. Check permissions.")

def remove_unlimited_token():
    token_path = os.path.join(os.getcwd(), ".unlimited")
    if not os.path.isfile(token_path):
        invalid_download_url("No .unlimited file found to remove.")
        return
    confirm = input(f"  {BLUE}Remove token? (y/N) {RESET}").strip().lower()
    if confirm != "y":
        return
    try:
        os.remove(token_path)
        print(box_header("Unlimited Token"))
        print(format_kv_line("Status", "Token removed"))
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    except OSError:
        invalid_download_url("Could not remove .unlimited file. Check permissions.")

def pause_return():
    input(f"  {BLUE}╰─>{RESET} ")

def show_rate_limits():
    headers = {}
    unlimited_token, _ = read_unlimited_token()
    if unlimited_token:
        headers["X-ClipX-Unlimited"] = unlimited_token
    try:
        response = requests.get("https://clipx.zamdev.workers.dev/?rate_limit=true", headers=headers)
        data = response.json()
    except Exception:
        invalid_download_url("Could not fetch rate limits. Try again later.")
        return
    rate_limit_info = (data.get("data") or {}).get("rate_limit") or {}
    show_rate_limit_box(rate_limit_info)

def about_menu():
    contact_info = fetch_contact_info()
    contact_email = contact_info.get("email") or "clipx@zamdev.dev"
    print(box_header("About"))
    print(format_kv_line("Tool", "TikTok Downloader API"))
    print(format_kv_line("Developer", "Abdisamed Mohamed"))
    print(format_kv_line("Telegram", "https://zamdevio.t.me"))
    print(format_kv_line("Telegram Bot", "https://t.me/TikTok_DownloaderiBot"))
    print(format_kv_line("Website", "https://clipx.zamdev.dev"))
    print(format_kv_line("GitHub", "https://github.com/zamdevio"))
    print(format_kv_line("Token Request", f"Email {contact_email} or Telegram @zamdevio"))
    if contact_info.get("message"):
        print(format_kv_line("Note", contact_info.get("message")))
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

def home_menu():
    while True:
        header(do_clear=True)
        print(box_header("Home Menu"))
        print(format_menu_line("01/A", "Download Mode"))
        print(format_menu_line("02/B", "About"))
        print(format_menu_line("03/C", "Visit Telegram Bot"))
        print(format_menu_line("04/D", "Visit ClipX Website"))
        print(format_menu_line("05/E", "Set Unlimited Token"))
        print(format_menu_line("06/F", "Remove Unlimited Token"))
        print(format_menu_line("07/G", "Rate Limits"))
        print(format_menu_line("08/H", "Exit"))
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        print(format_kv_line("Unlimited Token", token_status()))
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        choice = input(f"  {BLUE}╰─>{RESET} ").strip().lower()
        if choice in ("01", "1", "a"):
            return "download"
        if choice in ("02", "2", "b"):
            about_menu()
            pause_return()
            continue
        if choice in ("03", "3", "c"):
            print(box_header("Telegram Bot"))
            print(format_kv_line("URL", "t.me/TikTok_DownloaderiBot"))
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            pause_return()
            continue
        if choice in ("04", "4", "d"):
            print(box_header("ClipX Website"))
            print(format_kv_line("URL", "https://clipx.zamdev.dev"))
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            pause_return()
            continue
        if choice in ("05", "5", "e"):
            set_unlimited_token()
            pause_return()
            continue
        if choice in ("06", "6", "f"):
            remove_unlimited_token()
            pause_return()
            continue
        if choice in ("07", "7", "g"):
            show_rate_limits()
            pause_return()
            continue
        if choice in ("08", "8", "h", "exit"):
            Exit()
        invalid_download_url("Invalid option. Please choose from the menu.")

def log_error(exception):
    """
    This function logs errors that occur during program execution to a file called 'tiktokapi_error_logs.txt'.
    It captures the stack trace of the exception using traceback.format_exc() and writes it to the log file 
    in binary mode to ensure proper encoding. This function helps in diagnosing issues and debugging the application.
    
    Args:
        exception (Exception): The exception object that was raised during execution.
    """
    error_message = f"Error: {str(e)}\nTraceback:\n{traceback.format_exc()}"
    
    with open('tiktok_downloader_error_logs.txt', 'a') as log_file:
        log_file.write(f"{error_message}\n{'-'*80}\n")

    print(f"An error occurred: {str(e)}. Check the log file for details.")

BOX_INNER_WIDTH = 69
ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def strip_ansi(text):
    return ANSI_RE.sub('', text)

def char_width(ch):
    return 0 if unicodedata.combining(ch) else 1

def display_width(text):
    width = 0
    for ch in strip_ansi(text):
        if unicodedata.combining(ch):
            continue
        width += 2 if unicodedata.east_asian_width(ch) in ('W', 'F') else 1
    return width

def truncate_to_width(text, max_width):
    if max_width <= 0:
        return ""
    width = 0
    out = []
    for ch in text:
        ch_width = char_width(ch)
        if width + ch_width > max_width:
            break
        out.append(ch)
        width += ch_width
    if width < display_width(text):
        if max_width >= 3:
            while out and (display_width(''.join(out)) + 3) > max_width:
                out.pop()
            return ''.join(out) + "..."
    return ''.join(out)

def format_kv_line(label, value, label_color=CYAN, value_color=BLUE, inner_width=BOX_INNER_WIDTH):
    value_text = "" if value is None else str(value)
    prefix = f" {GRAY}【{RESET}●{GRAY}】{label_color}{label}: {value_color}"
    max_value_width = inner_width - display_width(prefix)
    value_text = truncate_to_width(value_text, max_value_width)
    content = f"{prefix}{value_text}{BLUE}"
    padding = inner_width - display_width(content)
    if padding < 0:
        padding = 0
    return f"{BLUE}│{content}{' ' * padding}{BLUE}│"

def format_menu_line(index, text, color=GREEN2, inner_width=BOX_INNER_WIDTH):
    prefix = f" {GRAY}【{RESET}{index}{GRAY}】{color}"
    max_text_width = inner_width - display_width(prefix)
    text = truncate_to_width(str(text), max_text_width)
    content = f"{prefix}{text}{BLUE}"
    padding = inner_width - display_width(content)
    if padding < 0:
        padding = 0
    return f"{BLUE}│{content}{' ' * padding}{BLUE}│"

def box_header(title, total_width=BOX_INNER_WIDTH + 2):
    inner = total_width - 2
    label_visible = f" < {title} > "
    label_colored = f" <{WHITE}{GRAY} {title} {WHITE}{RESET}{BLUE}> "
    dash_count = inner - display_width(label_visible)
    left = dash_count // 2
    right = dash_count - left
    return f"{BLUE}╭{'─' * left}{label_colored}{'─' * right}╮"

def get_tiktok_links(tiktok_link):
     """
    This function processes a given TikTok video URL to extract information about the video or images
    associated with it. It first verifies if the input link is a valid TikTok URL, and if not, it returns
    an error message. If the link is valid, it proceeds to make an HTTP request to an API that fetches the
    video or image details, including metadata such as the title, creation time, views, and more.

    The function handles different types of content (video or images), displays formatted information to the
    user, and triggers appropriate download functions based on the content type. If any errors occur during
    the process, it catches the exceptions and provides error messages, ensuring a smooth user experience.
     """
     if not tiktok_link:
          print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
          print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{RED}TikTok link is empty. Please enter a valid link.               {BLUE}│")
          print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
          return
     if not 'tiktok.com' in tiktok_link.lower():
          print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
          print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{RED}Invalid TikTok link 🔗                                         {BLUE}│")
          print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
          return

     try:
        api_url = f'https://clipx.zamdev.workers.dev/?url={tiktok_link}&format=true&rate_limit=true'
        headers = {}
        unlimited_token, _ = read_unlimited_token()
        if unlimited_token:
            headers["X-ClipX-Unlimited"] = unlimited_token
        response = requests.get(api_url, headers=headers)
        response_json = response.json()
        data = response_json.get('data') or {}
        if not data or not response_json.get('success'):
          invalid_link()
        title = data.get('title', '').strip()
        if not title:
          invalid_link()
        if len(title) > 60:
          title = title[:60] + "..."
        formatted_title = format_kv_line("Title", title, value_color=GREEN3)
        thumbnail = data.get('cover') or data.get('origin_cover') or data.get('ai_dynamic_cover')
        mp3_url = data.get('audio', {}).get('play')
        author = data.get('author') or {}
        author_username = author.get('username')
        author_nickname = author.get('nickname')
        if author_nickname and author_username:
            author_label = f"{author_nickname} (@{author_username})"
        elif author_nickname:
            author_label = author_nickname
        elif author_username:
            author_label = f"@{author_username}"
        else:
            author_label = None
        stats = data.get('stats', {})
        cache_info = response_json.get('cache') or {}
        rate_limit_info = response_json.get('rate_limit') or (data.get('rate_limit') or {})
        meta_info = response_json.get('meta') or {}
        api_info = meta_info.get('api_info') or {}
        params_used = meta_info.get('parameters_used') or {}
        contact_info = response_json.get('contact') or {}
        trace_info = response_json.get('trace') or {}
        processing_time = response_json.get('processing_time')
        video_links = data.get('video') if isinstance(data.get('video'), dict) else None
        img_links = data.get('images') if isinstance(data.get('images'), list) else None
        
        if video_links:
            print(box_header("TikTok Video"))
            print(format_kv_line("Content-Type", "Videos", value_color=BINK))
            print(formatted_title)
            if data.get('id'):
                print(format_kv_line("Video ID", data.get('id')))
            if data.get('region'):
                print(format_kv_line("Region", data.get('region')))
            if author_label:
                print(format_kv_line("Author", author_label))
            print(format_kv_line("Create Time", data.get('create_time')))
            print(format_kv_line("Views", stats.get('views')))
            if stats.get('play_count') is not None:
                print(format_kv_line("Play Count", stats.get('play_count')))
            print(format_kv_line("Love Count", stats.get('digg_count')))
            print(format_kv_line("Comment Count", stats.get('comment_count')))
            print(format_kv_line("Favorite Count", stats.get('favourite_count')))
            if stats.get('share_count') is not None:
                print(format_kv_line("Share Count", stats.get('share_count')))
            if stats.get('download_count') is not None:
                print(format_kv_line("Download Count", stats.get('download_count')))
            print(format_kv_line("Duration", data.get('duration')))
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

            links = video_links
        if img_links:
            total_images = len(img_links)
            print(box_header("TikTok Images"))
            print(format_kv_line("Content-Type", "Images", value_color=BINK))
            print(formatted_title)
            if data.get('id'):
                print(format_kv_line("Post ID", data.get('id')))
            if data.get('region'):
                print(format_kv_line("Region", data.get('region')))
            if author_label:
                print(format_kv_line("Author", author_label))
            print(format_kv_line("Create Time", data.get('create_time')))
            print(format_kv_line("Views", stats.get('views')))
            if stats.get('play_count') is not None:
                print(format_kv_line("Play Count", stats.get('play_count')))
            print(format_kv_line("Love Count", stats.get('digg_count')))
            print(format_kv_line("Comment Count", stats.get('comment_count')))
            print(format_kv_line("Favorite Count", stats.get('favourite_count')))
            if stats.get('share_count') is not None:
                print(format_kv_line("Share Count", stats.get('share_count')))
            if stats.get('download_count') is not None:
                print(format_kv_line("Download Count", stats.get('download_count')))
            if total_images > 9:
               print(format_kv_line("Total Images", f"{total_images} images", value_color=BINK))
            elif total_images > 0:
               print(format_kv_line("Total Images", f"{total_images} images", value_color=BINK))
            else:
                print(format_kv_line("Total Images", f"{total_images} image", value_color=BINK))
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

        if api_info or cache_info or trace_info or contact_info or processing_time is not None:
            print(box_header("API Info"))
            if api_info.get('name'):
                print(format_kv_line("API", api_info.get('name')))
            if api_info.get('version'):
                print(format_kv_line("Version", api_info.get('version')))
            if params_used.get('quality'):
                print(format_kv_line("Quality", params_used.get('quality')))
            if cache_info.get('hit') is not None:
                print(format_kv_line("Cache Hit", cache_info.get('hit')))
            if cache_info.get('expiresIn'):
                print(format_kv_line("Cache Expires In", cache_info.get('expiresIn')))
            if trace_info.get('worker_location'):
                print(format_kv_line("Worker", trace_info.get('worker_location')))
            if trace_info.get('request_id'):
                print(format_kv_line("Request ID", trace_info.get('request_id')))
            if processing_time is not None:
                print(format_kv_line("Processing Time", processing_time))
            if contact_info.get('email'):
                print(format_kv_line("Contact", contact_info.get('email')))
            if contact_info.get('message'):
                print(format_kv_line("Contact Note", contact_info.get('message')))
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

        if rate_limit_info:
            show_rate_limit_box(rate_limit_info)

        if not video_links and not img_links:
            invalid_link()
        if img_links:
            download_img(img_links, total=total_images, mp3_url=mp3_url, title=title, thumbnail=thumbnail)
        else:
            download_vid(links, title=title, thumbnail=thumbnail, mp3_url=mp3_url)

     except PermissionError as e:
        log_error(e)
        print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
        print(f"{BLUE}│ {RED}Error: {BINK}Make sure you have the  permissions for the Downloaded Dir   {BLUE}│")
        print(f"{BLUE}│ {GREEN3}Logs saved as tiktokapi_error_logs.txt                              {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        sys.exit()
     except requests.exceptions.RequestException as err:
        print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
        print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{RED}Error occurred during the request                              {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        sys.exit()
     except Exception as e:
        print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
        print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{RED}An unexpected error occurred                                   {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        print(e)
        sys.exit()

def download_img(links, total=1, mp3_url=None, title=None, thumbnail=None):
    """
    Provides a menu for downloading various media related to a TikTok video, including images, MP3 audio, and thumbnails.

    This function displays an interactive menu that allows the user to:
    - Download all images in a zip file
    - Download a specific image by its number
    - Download all images individually
    - Download the MP3 audio file
    - Download the thumbnail image
    - Go back to the main menu

    The function also handles validation for user input, ensuring that only valid options and image numbers are selected.
    It uses helper functions to manage the actual downloading of images, audio, and thumbnails.

    Parameters:
    - links (dict): A dictionary containing links to media files (images, MP3, thumbnail).
    - total (int, optional): The total number of images available for download. Default is 1.
    - mp3_url (str, optional): The URL for downloading the MP3 audio file. Default is None.
    - title (str, optional): The title of the TikTok video, used for naming downloaded files. Default is None.
    - thumbnail (str, optional): The URL for downloading the thumbnail image. Default is None.

    Returns:
    - None: The function interacts with the user and handles file downloads, but does not return a value.
    """
    download_dir = load_download_dir()
    while True:
        print(box_header("TikTok Links"))
        print(format_menu_line("1", "Download all images in a zip file"))
        print(format_menu_line("2", "Download specific image by number"))
        print(format_menu_line("3", "Download all images"))
        print(format_menu_line("4", "Download MP3 Audio"))
        print(format_menu_line("5", "Download Thumbnail"))
        print(format_menu_line("6", "Go Back"))
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        print(f"{BLUE}│ {GRAY}【{RESET}#{GRAY}】{GREEN2}Choose an option                                               {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯{RESET}")
        choice = input(f'    {GREEN2}└──{BLUE}⫸{RESET} ').strip()

        if choice == '1':
            download_zip(links, total, mp3_url=mp3_url, title=title, download_dir=download_dir)
        elif choice == '2':
            if total > 9:
              print(box_header("TikTok Images"))
              print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{GREEN2}Enter image number to download:{RESET}    {BLUE}Total Images: {BINK}{total} images     {BLUE}│")
              print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            elif total > 0:
                print(box_header("TikTok Images"))
                print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{GREEN2}Enter image number to download:{RESET}    {BLUE}Total Images: {BINK}{total} image       {BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            try:
               img_number = int(input(f"  {BLUE}╰─>{RESET} "))
               if 1 <= img_number <= total:
                   download_specific_image(links[img_number - 1], img_number, title=title, download_dir=download_dir)
               else:
                   print(f"{BLUE}╭──────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ──────────────────────────────╮")
                   print(f"{BLUE}│ {GRAY}【{RED}#{GRAY}】{RED}Error: Invalid image number, please try again.                 {BLUE}│")
                   print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            except Exception as e:
               print(f"{BLUE}╭──────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ──────────────────────────────╮")
               print(f"{BLUE}│ {GRAY}【{RED}#{GRAY}】{RED}Error: {GREEN2}Please use only numeric values to download the image.   {BLUE}│")
               print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        elif choice == '3':
            download_all_images(links, total, title=title, download_dir=download_dir)
        elif choice == '4':
            download_url = mp3_url
            file_extension = '.mp3'
            if download_url:
                random_num = random.randint(1, 100000)
                audio_dir = ensure_subdir(download_dir, "audio")
                file_name = os.path.join(audio_dir, f"{title}" + file_extension)
                print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading {BINK}Audio {CYAN}as {BINK}MP3                                       {BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
                response = requests.get(download_url, stream=True)
                with open(file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                file_name = shorten_path(file_name, max_length=40, line_length=76)
                print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download Done {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading Complete: {BINK}{file_name}{BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            else:
                print(f"{BLUE}╭──────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ──────────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RED}#{GRAY}】{RED}Error: No valid download URL, please try again.                {BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        elif choice == '5':
            download_url = thumbnail
            file_extension = '.jpg'
            if download_url:
                random_num = random.randint(1, 100000)
                thumb_dir = ensure_subdir(download_dir, "thumbnail")
                file_name = os.path.join(thumb_dir, f"{title}" + file_extension)
                print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading {BINK}Thumbnail                                          {BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
                response = requests.get(download_url, stream=True)
                with open(file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                file_name = shorten_path(file_name, max_length=40, line_length=76)
                print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download Done {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading Complete: {BINK}{file_name}{BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            else:
                print(f"{RED}No valid download URL, please try again.{RESET}")
        elif choice == '6':
            main()
            return
        else:
            print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
            print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{RED}Invalid option, please try again                               {BLUE}│")
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            continue

def shorten_path(path, max_length=30, line_length=60):
    """
    Shortens a file path to fit within a specified maximum length, and adds padding to align the output to a given line length.

    The function truncates the path in the middle and inserts '.....' if the path exceeds the maximum length. It also ensures that the
    final string fits within the specified line length by adding appropriate padding.

    Parameters:
    - path (str): The file path to shorten.
    - max_length (int, optional): The maximum allowed length for the shortened path. Default is 30 characters.
    - line_length (int, optional): The desired total length of the output string (including padding). Default is 60 characters.

    Returns:
    - str: A string representing the shortened file path with added padding, if necessary.
    """
    if len(path) > max_length:
        part_length = (max_length - 5) // 2  # 5 for the "....."
        shortened = f"{path[:part_length]}.....{path[-part_length:]}"
    else:
        shortened = path

    padding_length = line_length - len(shortened) - 35
    return shortened.ljust(len(shortened) + padding_length)


def download_vid(links, title=None, thumbnail=None, mp3_url=None):
    """
    This function provides a menu for downloading various media associated with a TikTok video. The user is prompted to
    select from the following options:
    - Download the standard MP4 video.
    - Download the HD MP4 video.
    - Download the MP3 audio of the video.
    - Download the thumbnail image of the video.
    After the user selects an option, the corresponding file is downloaded and saved to the specified directory.
    
    Parameters:
    - links (dict): A dictionary containing download links for standard MP4, HD MP4, and other related media.
    - title (str, optional): The title of the video or media, used to create file names for saving the media. Default is None.
    - thumbnail (str, optional): A URL to the video’s thumbnail image. Default is None.
    - mp3_url (str, optional): A URL to download the MP3 audio version of the video. Default is None.

    The function operates as follows:
    1. Displays a menu of options for the user to choose from.
    2. Based on the user’s selection, it attempts to download the corresponding media (video, audio, or thumbnail).
    3. Downloads the selected file and saves it to the appropriate directory.
    4. If the file is successfully downloaded, a confirmation message is shown with the path to the saved file.
    5. If an error occurs, such as an invalid download URL or permission error, an error message is displayed.

    The user can return to the main menu or continue downloading other files by selecting the relevant options.
    """
    download_dir = load_download_dir()
    while True:
        standard_url = links.get('standard_mp4') if isinstance(links, dict) else None
        hd_url = links.get('hd_mp4') if isinstance(links, dict) else None
        standard_label = "Download MP4 Standard"
        hd_label = "Download MP4 HD"
        if not standard_url:
            standard_label = "Download MP4 Standard (empty URL)"
        if not hd_url:
            hd_label = "Download MP4 HD (empty URL)"
        print(box_header("TikTok Links"))
        print(format_menu_line("1", standard_label))
        print(format_menu_line("2", hd_label))
        print(format_menu_line("3", "Download MP3 Audio"))
        print(format_menu_line("4", "Download Thumbnail"))
        print(format_menu_line("5", "Go Back"))
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        print(f"{BLUE}│ {GRAY}【{RESET}#{GRAY}】{GREEN2}Choose an option                                               {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯{RESET}")
        option = input(f'    {GREEN2}└──{BLUE}⫸{RESET} ').strip()

        if option == '1':
            if not standard_url:
                invalid_download_url("MP4 Standard URL is empty or invalid. Try another option.")
                continue
            download_link = standard_url
            standard_dir = ensure_subdir(download_dir, "video", "standard")
            file_name = os.path.join(standard_dir, f"{title}.mp4")
        elif option == '2':
            if not hd_url:
                invalid_download_url("MP4 HD URL is empty or invalid. Try another option.")
                continue
            download_link = hd_url
            hd_dir = ensure_subdir(download_dir, "video", "hd")
            file_name = os.path.join(hd_dir, f"{title}.mp4")
        elif option == '3':
            file_extension = ".mp3"
            if mp3_url:
                random_num = random.randint(1, 100000)
                audio_dir = ensure_subdir(download_dir, "audio")
                file_name = os.path.join(audio_dir, f"{title}" + file_extension)
                print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading {BINK}Audio {CYAN}as {BINK}MP3                                       {BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
                response = requests.get(mp3_url, stream=True)
                with open(file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                file_name = shorten_path(file_name, max_length=40, line_length=76)
                print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download Done {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading Complete: {BINK}{file_name}{BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            else:
                print(f"{BLUE}╭──────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ──────────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RED}#{GRAY}】{RED}Error: No valid download URL, please try again.                {BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            continue
            file_name = os.path.join(download_dir, f"{title}.mp3")
        elif option == '4':
            download_url = thumbnail
            file_extension = '.jpg'
            if download_url:
                random_num = random.randint(1, 100000)
                thumb_dir = ensure_subdir(download_dir, "thumbnail")
                file_name = os.path.join(thumb_dir, f"{title}" + file_extension)
                print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading {BINK}Thumbnail                                          {BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
                response = requests.get(download_url, stream=True)
                with open(file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                file_name = shorten_path(file_name, max_length=40, line_length=76)
                print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download Done {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading Complete: {BINK}{file_name}{BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
                continue
            else:
                print(f"{BLUE}╭──────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ──────────────────────────────╮")
                print(f"{BLUE}│ {GRAY}【{RED}#{GRAY}】{RED}Error: No valid download URL, please try again.                {BLUE}│")
                print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
                continue
        elif option == '5':
            main()
            return
        else:
            print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
            print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{RED}Invalid option, please try again                               {BLUE}│")
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
            continue

        print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
        print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading {BINK}Video {CYAN}as {BINK}MP4                                       {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        response = requests.get(download_link, stream=True)
        try:
           with open(file_name, 'wb') as file:
               for chunk in response.iter_content(chunk_size=8192):
                   file.write(chunk)
           file_name = shorten_path(file_name, max_length=40, line_length=76)
           print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download Done {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
           print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading Complete: {BINK}{file_name}{BLUE}│")
           print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        except PermissionError as e:
            log_error(e)
            print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
            print(f"{BLUE}│ {RED}Error: {BINK}Make sure you have the  permissions for the Downloaded Dir   {BLUE}│")
            print(f"{BLUE}│ {GREEN3}Logs saved as tiktokapi_error_logs.txt                              {BLUE}│")
            print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        

def download_zip(links, total=1, mp3_url=None, title=None, download_dir=None):
    """
    This function downloads a set of images from the given URLs ('links') and stores them in a ZIP archive.
    The ZIP file is saved to the specified directory ('download_dir') with a file name based on the provided 'title'.
    Each image is downloaded individually, written to the disk, and then added to the ZIP file. Afterward, the downloaded 
    image files are removed from the local directory to save space.

    Parameters:
    - links (list): A list of URLs for the images to be downloaded.
    - total (int, optional): The total number of images to download. Default is 1.
    - mp3_url (str, optional): An optional URL for an MP3 file. Not used in this function but can be included for future functionality.
    - title (str, optional): A string to be included in the ZIP file name and the individual image file names. Default is None.
    - download_dir (str, optional): The directory where images and the ZIP file will be saved. Default is None.

    The function performs the following tasks:
    1. Constructs a file name for the ZIP archive using the 'title' and saves it to the 'download_dir'.
    2. Prints a progress message indicating that the images are being downloaded and stored in a ZIP file.
    3. Iterates over the list of image URLs ('links') and downloads each image.
    4. For each image, a temporary file is created, the image is saved, and then the file is added to the ZIP archive.
    5. The temporary image file is deleted after it has been added to the ZIP archive.
    6. After all images have been processed, a completion message is displayed with the path to the saved ZIP file.
    """
    random_num = random.randint(1, 100000)
    zip_name = os.path.join(download_dir, f"{title}_images.zip")
    print(f"{BLUE}╭───────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ─────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading all images into {BINK}ZIP File                           {BLUE}│")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    with ZipFile(zip_name, 'w') as zipf:
        for i, img_url in enumerate(links, start=1):
            img_name = f"{title}_imges_{i}.jpg"
            img_path = os.path.join(download_dir, img_name)
            response = requests.get(img_url, stream=True)
            with open(img_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            zipf.write(img_path, img_name)
            os.remove(img_path)
    file_name = shorten_path(zip_name, max_length=40, line_length=76)
    print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download Done {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading Complete: {BINK}{file_name}{BLUE}│")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

def download_specific_image(img_url, img_number, title=None, download_dir=None):
    """
    This function handles the downloading of a specific image from a given URL ('img_url') and saves it to the 
    specified directory ('download_dir'). The image is named based on the provided title and image number ('img_number').
    The function also provides feedback to the user about the download process with styled console output.

    Parameters:
    - img_url (str): The URL of the image to be downloaded.
    - img_number (int): The number used to differentiate the images. It is used for naming the downloaded file.
    - title (str, optional): A string to be included in the downloaded image's file name to identify it. Default is None.
    - download_dir (str, optional): The directory where the image will be saved. Default is None.

    The function performs the following tasks:
    1. Constructs a unique file name for the image based on the 'img_number' and 'title'.
    2. Displays a styled message indicating which image is being downloaded.
    3. Sends a GET request to fetch the image from the 'img_url'.
    4. Downloads the image in chunks to avoid large memory consumption.
    5. Saves the image to the specified directory.
    6. Displays a completion message with the path of the downloaded file.
    """
    random_num = random.randint(1, 100000)
    file_name = os.path.join(download_dir, f"{title}_images_{img_number}.jpg")
    if img_number > 9:
      print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
      print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading {BINK}Image {img_number}                                           {BLUE}│")
      print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    elif img_number > 0:
        print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
        print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading {BINK}Image {img_number}                                            {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    response = requests.get(img_url, stream=True)
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    file_name = shorten_path(file_name, max_length=40, line_length=76)
    print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download Done {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading Complete: {BINK}{file_name}{BLUE}│")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

def download_all_images(links, total, title=None, download_dir=None):
    """
    This function handles the downloading of multiple images from the provided list of image URLs ('links').
    It downloads each image and saves it locally with a unique file name in the specified directory ('download_dir').
    It also provides feedback to the user on the download progress with a visually styled output.

    Parameters:
    - links (list): A list of URLs pointing to the images to be downloaded.
    - total (int): The total number of images to be downloaded, used for progress indication.
    - title (str, optional): A string to be used in the downloaded image file names to distinguish them. 
                              Default is None.
    - download_dir (str, optional): The directory where the images will be saved. Default is None.

    The function performs the following tasks:
    1. Loops through each image URL in the 'links' list.
    2. Constructs a file path using the provided 'download_dir' and 'title' for naming the images.
    3. Downloads each image in chunks and saves it to the local directory.
    4. Displays progress updates in the terminal, showing which image is being downloaded and how many are left.
    5. Once all images are downloaded, it prints a completion message to the user, including the path where the images are saved.
    """
    random_num = random.randint(1, 100000)
    print("")
    clear = '\033[4A\033[K'
    for i, img_url in enumerate(links, start=1):
        file_name = os.path.join(download_dir, f"{title}_images_{i}.jpg")
        print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
        print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading image {i} of {total} images...{RESET}")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        response = requests.get(img_url, stream=True)
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(clear)
    print(f'\033[K\033[A\033[K')
    print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download File {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
    if total == 1:
      print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloaded images {total} of {total} image{RESET}")
    elif total > 0:
        print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloaded images {total} of {total} images{RESET}")
    elif total > 9:
        print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloaded images {total} of {total} images{RESET}")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    file_name = shorten_path(f'{download_dir}/*', max_length=40, line_length=76)
    print(f"{BLUE}╭──────────────────────── <{WHITE}{GRAY} Download Done {WHITE}{RESET}{BLUE}> ──────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}●{GRAY}】{CYAN}Downloading Complete: {BINK}{file_name}{BLUE}│")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")

def ask_exit():
    """
    This function is designed to prompt the user for confirmation when the script detects a 'CTRL + C' signal,
    indicating the user may want to exit the program. It prints a styled message to the console, asking whether
    the user wants to exit or not.

    The function handles user input by waiting for a response:
    - If the user inputs 'Y' or 'yes', the 'Exit()' function is called to terminate the script.
    - If the user inputs 'N' or 'no', the 'bak()' function is called to invoke the main process again.
    - If the input is invalid (anything other than 'Y', 'N', 'yes', or 'no'), an error message is shown, and the script exits by calling 'Exit()'.
    """
    print(f"{BLUE}╭────────────────────────── <{WHITE}{GRAY} CTRL + C {WHITE}{RESET}{BLUE}> ─────────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}+{GRAY}】{GREEN3}{BINK}CTRL+C{YELLOW} Detected                                                {BLUE}│")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    print(f"{BLUE}╭────────────────────────── <{WHITE}{GRAY} CTRL + C {WHITE}{RESET}{BLUE}> ─────────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}+{GRAY}】{GREEN3}Do you wanna exit {GREEN}【{YELLOW}Y{RESET}|{YELLOW}n{GREEN}】{GRAY}                                      {BLUE}│")
    try:
        exit_opt = input(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯\n   {GREEN2}╰─>{BOLD} {RESET}").strip()
    except KeyboardInterrupt:
        Exit()

    if exit_opt.lower() in ['yes', 'y']:
        Exit()
    elif exit_opt.lower() in ['no', 'n']:
        return
    else:
        print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} ERROR {WHITE}{RESET}{BLUE}> ───────────────────────────────╮")
        print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{RED}Invalid option                                                 {BLUE}│")
        print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
        Exit()

def exit_on_signal_SIGINT(signal_received, frame):
    """
    This function is called when the script receives a 'SIGINT' signal, typically triggered by the user pressing
    'CTRL + C'. It calls the 'ask_exit()' function to ask the user if they want to exit or continue.

    The 'SIGINT' signal is intercepted using the 'signal' module, and this function handles the prompt and user
    interaction when such a signal is received.
    """
    print()
    raise KeyboardInterrupt

def Exit():
    """
    This function is responsible for gracefully exiting the script. It prints a styled exit message
    to the console to thank the user for using the tool, followed by an exit command that terminates
    the program. The exit message is formatted with different colors to provide a visually appealing
    output to the user.

    The sys.exit(0) command is called at the end to stop the script execution with a success status.
    """
    print(f"{BLUE}╭─────────────────────────── <{WHITE}{GRAY} EXIT {WHITE}{RESET}{BLUE}> ────────────────────────────────╮")
    print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{RED}EXIT                                                           {BLUE}│")
    print(f"{BLUE}│ {GRAY}【{RESET}={GRAY}】{GREEN1}THANKS FOR USING THIS TOOL!                                   {BLUE} │")
    print(f"{BLUE}╰─────────────────────────────────────────────────────────────────────╯")
    sys.exit(0)

signal.signal(signal.SIGINT, exit_on_signal_SIGINT)

def bak():
    """
    This function serves as a backup to the main function. It simply calls the 'main()' function,
    which is the entry point of the script. The purpose of this function is to ensure that the main
    functionality of the script can be invoked easily in case of any required backup or fallback.
    """
    return


def main():
    """
    This is the main entry point of the script, responsible for the core functionality and logic 
    of the tool. It performs the following tasks:
    
    1. Displays a header for the script to inform the user of the tool's purpose.
    2. Checks if there are command-line arguments provided, specifically the download path, 
       and sets it if provided.
    3. Checks if necessary configuration files exist. If not, it calls a usage function to guide
       the user on how to use the tool.
    4. Enters an infinite loop, continuously prompting the user to input a TikTok video link.
       If the user types 'Exit', the 'Exit()' function is called to gracefully terminate the script.
    5. If a valid TikTok link is entered, the script processes it by calling the 'get_tiktok_links()' function.
    
    This loop continues until the user opts to exit the program by typing 'Exit'.
    """
    if home_menu() != "download":
        return
    path = None
    if len(sys.argv) > 1:
        path = sys.argv[1]
        set_download_dir(path)
    if not os.path.exists(FirtTime):
           if not os.path.exists(config_file):
                usage()
    while True:
         print(f'{BLUE}╭─────────── <{WHITE}{GRAY} ENTER LINK {RESET}{BLUE}> ────────╮╭────╮╭──── <{WHITE}{GRAY} EXIT OPTION {RESET}{BLUE}> ─────╮')
         print(f"{BLUE}│ {GRAY}【{RESET}•{GRAY}】{CYAN}Enter TikTok Video Link 🔗   {BLUE}││{RESET} OR {BLUE}││ {BLUE}Type {RED}Exit {BLUE}To {RED}Quit        {BLUE}│")
         print(f"╰───────────────────────────────────╯╰────╯╰──────────────────────────╯")
         tiktok_link = input(f"  {BLUE}╰─>{RESET} ").strip()
         if tiktok_link.lower() == "exit":
            Exit()
         get_tiktok_links(tiktok_link)
         continue

if __name__ == "__main__":
    """
    This block checks if the script is being run as the main program. If so, it executes the 'main()' function.
    The script name is stored in the 'script_name' variable, though it is not used here, and the main function
    is called to start the program.
    """
    script_name = sys.argv[0]
    while True:
        try:
            main()
            break
        except KeyboardInterrupt:
            ask_exit()
