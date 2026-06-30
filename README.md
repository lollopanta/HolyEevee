# HolyEevee AltStore Source

A self-updating AltStore/SideStore source for [EeveeIPA](https://github.com/estrogencat/EeveeIPA).

<a href="https://stikstore.app/altdirect/?url=https://raw.githubusercontent.com/lollopanta/HolyEevee/main/apps.json" target="_blank">
<img src="https://github.com/CelloSerenity/altdirect/blob/main/assets/png/AltSource_Blue.png?raw=true" alt="Add AltSource" width="200">
</a>

## 🚀 AltStore Source URL

To add this source to AltStore or SideStore, copy and paste the following URL:

```text
https://raw.githubusercontent.com/lollopanta/HolyEevee/main/apps.json
```

## 📦 Included Apps

- **Eevee Spotify**: Standard version (suitable for SideStore, AltStore Classic, LiveContainer, Sideloadly, and other general methods).

The upstream patched IPA is not listed in this AltStore/SideStore source because it currently uses the same bundle identifier as the standard IPA (`com.spotify.client`). Listing it as a separate app would make update detection unreliable.

### Supported sideloaders :
**Use classic with :**
 - SideStore (recommended)
 - AltStore Classic
 - LiveContainer

**Use patched upstream releases with :**
 - Feather (recommended*)
 - ESign
 - KSign
 - TrollApps

<small>*You can easily install an older version with long-click with Feather.</small>

### Unsupported sideloaders :
- AltStore PAL

## 🔄 How it Works

This repository is fully automated. A GitHub Action runs every hour to:
1.  Fetch the latest releases from the official [EeveeIPA repository](https://github.com/estrogencat/EeveeIPA).
2.  Update the `apps.json` file with all available versions.
3.  Commit and push the changes back to this repo.

## 🛠 Installation & Sideloading Info

### How to choose your sideloader?

*   **[SideStore](https://sidestore.io/):** 3 apps and 10 AppID limit without LiveContainer. PC needed for first installation. Hard to install.
*   **[Feather](https://feather.khcrysalis.dev/):** Need to buy licence from Apple Developper Program or certficate from a signing service. Avoid KravaSign, Signulous, FlekSt0re and AppsTesters.
*   **Note on Certificates:** Entreprise certificates (aka "free certs") are not recommended. This method is not reliable, violates Apple's Terms of Service, and may get your iDevice blacklisted.

### Adding the Source
1.  Open **AltStore** or **SideStore** on your iOS device.
2.  Go to the **Browse** tab.
3.  Tap the **Sources** button (top right).
4.  Tap **Add** (or **+**) and paste the Source URL above.

## ✨ About EeveeSpotify

This tweak makes Spotify think you have a Premium subscription, granting free listening, just like Spotilife, and provides some additional features like custom lyrics.

### 💎 Credits & Dedication

Special thanks to **[estrogencat](https://github.com/estrogencat)** for the [EeveeIPA](https://github.com/estrogencat/EeveeIPA) repository.

*   Credit to **[jaydenjcpy](https://github.com/jaydenjcpy)**: [Star his repo!](https://github.com/jaydenjcpy/EeveeSpotifyReincarnated)
*   Credit to **[Skye](https://github.com/Meeep1)**: [Star his repo and donate!](https://github.com/Meeep1/EeveeSpotifyRevivedPublic)

Special dedication to **[whoeevee](https://github.com/whoeevee)**, thank you for keeping the project going for these two years <3
You can still [donate to him](https://github.com/whoeevee) and star his repo :)

---
*Maintained by automation.*
