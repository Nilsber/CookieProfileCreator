import requests
import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException
import time

# Define file paths to save data
PROFILE_FILE = 'roblox_profiles.json'
GAME_IDS_FILE = 'roblox_game_ids.json'

# Function to load profiles from a JSON file
def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save profiles to a JSON file
def save_profiles(profiles):
    with open(PROFILE_FILE, 'w') as file:
        json.dump(profiles, file, indent=4)

# Function to load game IDs from a JSON file
def load_game_ids():
    if os.path.exists(GAME_IDS_FILE):
        with open(GAME_IDS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save game IDs to a JSON file
def save_game_ids(game_ids):
    with open(GAME_IDS_FILE, 'w') as file:
        json.dump(game_ids, file, indent=4)

# Function to join a game using a new browser window with the specified cookie
def join_game_with_cookie(cookie, game_id):
    # Set up Chrome options for a new instance
    options = Options()
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--incognito")  # Open in incognito mode to avoid using current session

    # Start a new instance of Chrome
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open Roblox and set the cookie
        driver.get("https://www.roblox.com")
        driver.add_cookie({
            'name': '.ROBLOSECURITY',
            'value': cookie,
            'domain': '.roblox.com'
        })

        # Navigate to the game page
        driver.get(f'https://www.roblox.com/games/{game_id}')

        # Wait for the Play button to be present in the DOM
        print("Waiting for Play button...")
        play_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Play')]"))
        )

        # Wait until the Play button is clickable
        print("Waiting for Play button to be clickable...")
        play_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Play')]"))
        )

        play_button.click()
        print("Clicked Play button successfully.")

    except NoSuchWindowException:
        print("The browser window was closed before the action completed.")
    except Exception as e:
        messagebox.showerror('Error', f'Failed to click Play button: {e}')
    finally:
        # Optionally close the browser after some time
        # driver.quit()  # Uncomment this line if you want to close the browser automatically
        pass  # Manage the driver lifecycle as needed


# Function to handle adding a new profile
def add_new_profile():
    new_cookie = simpledialog.askstring("New Profile", "Enter your Roblox .ROBLOSECURITY cookie:")
    if new_cookie:
        profile_name = simpledialog.askstring("Profile Name", "Enter a name for this profile:")
        if profile_name:
            profiles[profile_name] = new_cookie
            save_profiles(profiles)
            # Update profile dropdown menu
            profile_var.set(profile_name)  # Select the new profile
            update_profile_menu()
            messagebox.showinfo('Success', f'Saved profile for {profile_name}')

# Function to update profile dropdown menu
def update_profile_menu():
    menu = profile_menu["menu"]
    menu.delete(0, "end")  # Clear current menu
    for profile in profiles:
        menu.add_command(label=profile, command=tk._setit(profile_var, profile))
    menu.add_command(label="Add New Profile", command=add_new_profile)

# Function to handle adding a new game
def add_new_game():
    new_game_name = simpledialog.askstring("New Game", "Enter the name of the game:")
    new_game_id = simpledialog.askstring("New Game", "Enter the Game ID:")
    if new_game_name and new_game_id:
        game_ids[new_game_name] = new_game_id
        save_game_ids(game_ids)
        # Update game dropdown menu
        game_var.set(new_game_name)  # Select the new game
        update_game_menu()
        messagebox.showinfo('Success', f'Saved game: {new_game_name}')

# Function to update game dropdown menu
def update_game_menu():
    menu = game_menu["menu"]
    menu.delete(0, "end")  # Clear current menu
    for game in game_ids:
        menu.add_command(label=game, command=tk._setit(game_var, game))
    menu.add_command(label="Add New Game", command=add_new_game)

# Function to handle logging in and joining the game
def login_and_join_game():
    selected_profile = profile_var.get()
    selected_game = game_var.get()

    if selected_profile == "Add New Profile":
        add_new_profile()
        return  # Return after adding new profile
    elif selected_game == "Add New Game":
        add_new_game()
        return  # Return after adding new game

    # Proceed to join game with the selected profile and game
    cookie = profiles[selected_profile]
    game_id = game_ids[selected_game]
    join_game_with_cookie(cookie, game_id)

# Load profiles and game IDs
profiles = load_profiles()
game_ids = load_game_ids()

# Create the main window
root = tk.Tk()
root.title("Roblox Game Joiner")

# Profile selection
tk.Label(root, text="Select Profile:").grid(row=0, column=0, padx=10, pady=10)
profile_var = tk.StringVar(root)
profile_var.set("Add New Profile")  # Default value
profile_menu = tk.OptionMenu(root, profile_var, "Add New Profile")
profile_menu.grid(row=0, column=1, padx=10, pady=10)

# Game selection
tk.Label(root, text="Select Game:").grid(row=1, column=0, padx=10, pady=10)
game_var = tk.StringVar(root)
game_var.set("Add New Game")  # Default value
game_menu = tk.OptionMenu(root, game_var, "Add New Game")
game_menu.grid(row=1, column=1, padx=10, pady=10)

# Button to login and join the game
join_button = tk.Button(root, text="Join Game", command=login_and_join_game)
join_button.grid(row=2, columnspan=2, pady=20)

# Initial population of dropdown menus
update_profile_menu()
update_game_menu()

# Run the application
root.mainloop()
