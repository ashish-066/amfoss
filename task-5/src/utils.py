# utility functions for quiz
import json
import os
import requests

PROFILE_FILE = os.path.join(os.path.dirname(__file__), '../profiles.json')
CATEGORY_URL = "https://opentdb.com/api_category.php"

def load_profiles():
    if not os.path.exists(PROFILE_FILE):
        return {}
    with open(PROFILE_FILE,'r') as file:
        try:
            profiles=json.load(file)
            return profiles
        except json.JSONDecodeError:
            return {}

def save_profiles(profiles):
    with open(PROFILE_FILE, 'w') as file:
        json.dump(profiles, file, indent=4)

def get_profile(username):
    profiles = load_profiles()
    return profiles.get(username)

def update_profile(new_profile):
    profiles = load_profiles()
    username = new_profile.get("username")
    if username is None:
        raise ValueError("Profile must include a 'username' key")
    profiles[username] = new_profile
    save_profiles(profiles)


def get_categories():
    try:
        response = requests.get(CATEGORY_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("trivia_categories", [])
    except (requests.RequestException, json.JSONDecodeError):
        return []