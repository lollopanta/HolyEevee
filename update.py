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

        # Track if we've already added an IPA for this release to prevent duplicates
        has_standard = False
        has_patched = False

        for asset in release["assets"]:
            asset_name = asset["name"].lower()
            if asset_name.endswith(".ipa"):
                version_obj = {
                    "version": version_tag,
                    "date": formatted_date,
                    "downloadURL": asset["browser_download_url"],
                    "size": asset["size"],
                    "localizedDescription": changelog
                }
                
                # Use case-insensitive check and ensure we only take the first matching IPA per category
                if "patched" in asset_name:
                    if not has_patched:
                        patched_versions.append(version_obj)
                        has_patched = True
                else:
                    if not has_standard:
                        standard_versions.append(version_obj)
                        has_standard = True

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
