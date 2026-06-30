import requests
import json
import plistlib
import tempfile
import zipfile

REPO = "estrogencat/EeveeIPA"
SOURCE_FILE = "apps.json"
MAX_VERSIONS = 5
REQUEST_TIMEOUT = 60

session = requests.Session()

def get_releases():
    url = f"https://api.github.com/repos/{REPO}/releases"
    response = session.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()

def get_ipa_metadata(download_url):
    with tempfile.NamedTemporaryFile(suffix=".ipa") as ipa_file:
        with session.get(download_url, stream=True, timeout=REQUEST_TIMEOUT) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    ipa_file.write(chunk)

        ipa_file.flush()

        with zipfile.ZipFile(ipa_file.name) as ipa:
            plist_name = next(
                name for name in ipa.namelist()
                if name.startswith("Payload/")
                and name.endswith(".app/Info.plist")
                and name.count("/") == 2
            )
            info = plistlib.loads(ipa.read(plist_name))

    return {
        "bundleIdentifier": info["CFBundleIdentifier"],
        "version": info["CFBundleShortVersionString"],
        "buildVersion": info["CFBundleVersion"],
    }

def get_existing_metadata(source):
    metadata = {}
    for app in source["apps"]:
        for version in app.get("versions", []):
            if version.get("buildVersion"):
                metadata[version["downloadURL"]] = {
                    "version": version["version"],
                    "buildVersion": version["buildVersion"],
                }
    return metadata

def update_source():
    with open(SOURCE_FILE, "r") as f:
        source = json.load(f)

    releases = get_releases()
    
    # Use dictionaries to ensure version uniqueness
    standard_versions_dict = {}
    metadata_cache = get_existing_metadata(source)

    for release in releases:
        if len(standard_versions_dict) >= MAX_VERSIONS:
            break

        tag_name = release["tag_name"]
        
        # Extract base version (e.g., "9.1.58" from "9.1.58-6.6.4-...")
        # We look for the first part that looks like a version number
        parts = tag_name.split("-")
        base_version = None
        for part in parts:
            if part[0].isdigit():
                base_version = part
                break
        
        if not base_version:
            continue # Skip tags that don't contain a version number (like "ios-15-latest")

        # Clean the version to match CFBundleShortVersionString (typically 3 components, e.g., 9.1.60 instead of 9.1.60.383)
        version_parts = base_version.split(".")
        if len(version_parts) > 3:
            base_version = ".".join(version_parts[:3])
        
        date = release["published_at"]
        # Format date for AltStore (YYYY-MM-DD)
        formatted_date = date.split("T")[0]
        
        # Include the full tag in the description so users know the tweak version
        changelog = f"Build: {tag_name}\n\n" + release["body"]

        # Track if we've already added an IPA for this release object
        has_standard_in_release = False

        for asset in release["assets"]:
            asset_name = asset["name"].lower()
            if asset_name.endswith(".ipa") and "patched" not in asset_name:
                if asset["browser_download_url"] not in metadata_cache:
                    if not standard_versions_dict:
                        print(f"Reading metadata from {asset['name']}...", flush=True)
                        metadata_cache[asset["browser_download_url"]] = get_ipa_metadata(asset["browser_download_url"])
                    else:
                        metadata_cache[asset["browser_download_url"]] = {
                            "version": base_version,
                            "buildVersion": base_version,
                        }

                metadata = metadata_cache[asset["browser_download_url"]]
                version_obj = {
                    "version": metadata["version"],
                    "buildVersion": metadata["buildVersion"],
                    "date": formatted_date,
                    "downloadURL": asset["browser_download_url"],
                    "size": asset["size"],
                    "localizedDescription": changelog
                }
                
                if not has_standard_in_release and base_version not in standard_versions_dict:
                    standard_versions_dict[base_version] = version_obj
                    has_standard_in_release = True
                    break

    # Convert dictionaries back to lists and sort by date (descending)
    standard_versions = sorted(standard_versions_dict.values(), key=lambda x: x["date"], reverse=True)

    # Update apps in source
    source["apps"] = [app for app in source["apps"] if app["name"] == "Eevee Spotify"]
    for app in source["apps"]:
        if app["name"] == "Eevee Spotify":
            app["bundleIdentifier"] = "com.spotify.client"
            app["versions"] = standard_versions

    with open(SOURCE_FILE, "w") as f:
        json.dump(source, f, indent=2)

if __name__ == "__main__":
    update_source()
    print("Source updated successfully.")
