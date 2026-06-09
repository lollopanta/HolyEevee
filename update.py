import requests
import json
import os
from datetime import datetime

REPO = "estrogencat/EeveeIPA"
SOURCE_FILE = "apps.json"

def get_releases():
    url = f"https://api.github.com/repos/{REPO}/releases"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def update_source():
    with open(SOURCE_FILE, "r") as f:
        source = json.load(f)

    releases = get_releases()
    
    standard_versions = []
    patched_versions = []

    for release in releases:
        version_tag = release["tag_name"]
        date = release["published_at"]
        # Format date for AltStore (YYYY-MM-DD)
        formatted_date = date.split("T")[0]
        changelog = release["body"]

        for asset in release["assets"]:
            if asset["name"].endswith(".ipa"):
                version_obj = {
                    "version": version_tag,
                    "date": formatted_date,
                    "downloadURL": asset["browser_download_url"],
                    "size": asset["size"],
                    "localizedDescription": changelog
                }
                
                if "Patched" in asset["name"]:
                    patched_versions.append(version_obj)
                else:
                    standard_versions.append(version_obj)

    # Update apps in source
    for app in source["apps"]:
        if app["bundleIdentifier"] == "com.eevee.spotify":
            app["versions"] = standard_versions
        elif app["bundleIdentifier"] == "com.eevee.spotify.patched":
            app["versions"] = patched_versions

    with open(SOURCE_FILE, "w") as f:
        json.dump(source, f, indent=2)

if __name__ == "__main__":
    update_source()
    print("Source updated successfully.")
