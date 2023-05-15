import os
import win32api, win32con
import ctypes
import requests
from requests.exceptions import RequestException
import json
from json.decoder import JSONDecodeError


APOD_URL = "https://api.nasa.gov/planetary/apod"


# --------------
# Config support
# --------------


def get_config(config_path):
    """
    Loads user configuration from a JSON file in the specified path.

    Args:
        config_path (str): The path where config (json) file is expected.

    Returns:
        dict: A dictionary with the configuration values.
    """
    
    if not os.path.exists(config_path):
        create_config(config_path)
        
    with open(config_path) as f:
        return json.load(f)


def create_config(config_path):
    """
    Creates default configuration file in the specified path with default values for 'api_key', 'default_wallpaper', and 'style'. 

    Args:
        config_path (str): The path where config (json) file will be created.
    """
    
    config = {
        "api_key": "",
        "default_wallpaper": "",
        "style": ""
    }
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
        
    print(f"Config file has been created in {os.path.abspath(config_path)}. Complete it and run script again. \n"
          f"  Hint 1: You can generate NASA API key here: https://api.nasa.gov/ \n"
          f"  Hint 2: There are 6 available styles: fill, fit, stretch, tile, center, span.")
    exit(0)


# -----------------
# Setting wallpaper
# -----------------


def get_image(api_key):
    """
    Retrieves APOD image using provided NASA API key and stores the image and its metadata locally.


    Args:
        api_key (str): The NASA API key used to request the APOD image. 

    Returns:
        tuple: A tuple containing the path to the saved image file (str) and the image's metadata (dict).
    """

    try:
        response = requests.get(APOD_URL, params={"api_key": api_key})
        response.raise_for_status()
    except RequestException as e:
        print(f"Problem with request to APOD: {e}")
        raise
    
    try:
        metadata = response.json()
    except JSONDecodeError as e:
        print(f"Problem with decoding response: {e}")
        raise
    
    url = metadata['url']
    apod_json_path = 'data/apod.json'
    with open(apod_json_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    try:
        response = requests.get(url)
        response.raise_for_status()
    except RequestException as e:
        print(f"Problem with request to download wallpaper: {e}")
        raise
    
    apod_image_path = 'data/apod.jpg'
    with open(apod_image_path, 'wb') as f:
        f.write(response.content)
        
    return apod_image_path, metadata


def set_wallpaper(apod_image_path, style):
    """
    Sets the specified image as the current system wallpaper with a given style.

    Args:
        apod_image_path (str): The path to the image file.
        style (str): The style of the wallpaper display ('fill', 'fit', 'stretch', 'tile', 'center', 'span').
    """
    
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(apod_image_path), 0)

    # Set style
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    if style == 'fill':
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, '10')
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, '0')
    elif style == 'fit':
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, '6')
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, '0')
    elif style == 'stretch':
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, '2')
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, '0')
    elif style == 'tile':
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, '0')
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, '1')
    elif style == 'center':
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, '0')
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, '0')
    elif style == 'span':
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, '22')
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, '0')
    else:
        print(f"Chosen style is incorrect! Please, rewrite your config file and get sure, that you have one of "
              f"the following styles: fill, fit, stretch, tile, center, span.")
        exit(0)


# ---------------
# Other functions
# ---------------


def print_wallpaper_info(metadata):
    """
    Prints the brief information about the wallpaper.

    Args:
        metadata (dict): The metadata of the wallpaper image.
    """
    
    date, title, copyright = metadata['date'], metadata['title'], metadata['copyright']
    explanation = metadata['explanation']
    print(f"[{date}] {title} | {copyright}")
    print(explanation)


if __name__ == "__main__":
    # Get configurations from JSON file
    config_path = './config/config.json'
    try:
        config = get_config(config_path)
    except FileNotFoundError or JSONDecodeError as e:
        print(f"Problem with reading or decoding config file: {e}")
        exit(1)
        
    api_key = config['api_key']
    default_wallpaper_path = config['default_wallpaper']
    style = config['style']
    
    # Setting wallpaper procedure
    try:
        apod_image_path, metadata = get_image(api_key)
        set_wallpaper(apod_image_path, style)
        print("Wallpaper is set successfully!")
        print_wallpaper_info(metadata)
    except Exception:
        set_wallpaper(default_wallpaper_path, style)
        print(f"Problem with getting APOD image: {e}")
