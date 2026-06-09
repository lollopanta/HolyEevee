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
    
    # Use dictionaries to ensure version uniqueness
    standard_versions_dict = {}
    patched_versions_dict = {}

    for release in releases:
        tag_name = release["tag_name"]
        # Extract base version (e.g., "9.1.58" from "9.1.58-6.6.4-...")
        # AltStore requires this to match the internal CFBundleShortVersionString
        base_version = tag_name.split("-")[0]
        
        date = release["published_at"]
        # Format date for AltStore (YYYY-MM-DD)
        formatted_date = date.split("T")[0]
        
        # Include the full tag in the description so users know the tweak version
        changelog = f"Build: {tag_name}\n\n" + release["body"]

        # Track if we've already added an IPA for this release object
        has_standard_in_release = False
        has_patched_in_release = False

        for asset in release["assets"]:
            asset_name = asset["name"].lower()
            if asset_name.endswith(".ipa"):
                version_obj = {
                    "version": base_version,
                    "date": formatted_date,
                    "downloadURL": asset["browser_download_url"],
                    "size": asset["size"],
                    "localizedDescription": changelog
                }
                
                if "patched" in asset_name:
                    if not has_patched_in_release and base_version not in patched_versions_dict:
                        patched_versions_dict[base_version] = version_obj
                        has_patched_in_release = True
                else:
                    if not has_standard_in_release and base_version not in standard_versions_dict:
                        standard_versions_dict[base_version] = version_obj
                        has_standard_in_release = True

    # Convert dictionaries back to lists and sort by date (descending)
    standard_versions = sorted(standard_versions_dict.values(), key=lambda x: x["date"], reverse=True)
    patched_versions = sorted(patched_versions_dict.values(), key=lambda x: x["date"], reverse=True)

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
