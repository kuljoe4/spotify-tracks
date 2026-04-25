# Spotrack — Playlist + Download Manager

Spotrack is a lightweight, browser-based tool to help you manage and download your Spotify playlists (or any list of tracks) by fetching audio from public YouTube-to-MP3 sources. It's designed to be simple, no-login required, and privacy-focused.

## 🚀 Quick Start

### 1. Get your Playlist CSV
The easiest way to import your Spotify library is via **Exportify**:
1. Visit [exportify.net](https://exportify.net).
2. Log in with your Spotify account (it's safe and open-source).
3. Export your "Liked Songs" or any specific playlist as a CSV file.

### 2. Load into Spotrack
1. Open `spotrack.html` in your browser.
2. Drag and drop your CSV file into the drop zone, or paste the content into the text area.
3. (Optional) Adjust the number of tracks to load or the order.
4. Click **▶ Load Tracks**.

### 3. Start Downloading
1. Review your track list.
2. Click **▶ Start All** to begin the sequential download queue.
3. The app will transition tracks through: `Queued` → `Fetching` → `Downloading` → `Done`.
4. Your browser will prompt you to save each MP3 file.

## ✨ Features

- **Sequential Download Queue**: Downloads tracks one-by-one to avoid rate-limiting and ensure stability.
- **Persistence**: Your progress is saved to `localStorage`. You can close the tab and return later; Spotrack will remember which tracks are already done.
- **Fetching vs. Downloading**:
    - **Fetching**: Searching for the best audio match on YouTube.
    - **Downloading**: Triggering the actual file transfer to your device.
- **Manual Overrides**: Tap any status chip to manually mark it as done (if you downloaded it elsewhere) or reset it.
- **yt-dlp Fallback**: If a track fails to download via the browser, click the `Failed` chip to see a pre-formatted `yt-dlp` command to download it manually via terminal.

## 🛠 Troubleshooting & Limitations

### Browser Download Blocks
Modern browsers often block "automatic" multiple downloads for security.
- **If downloads stop**: Check your address bar (usually on the right) for a "Downloads blocked" icon. Click it and select **"Always allow downloads from this site"**.
- **Pop-up Blockers**: Ensure pop-ups are allowed, as some download triggers might be caught by aggressive blockers.

### Rate Limiting & Reliability
Public APIs can occasionally be flaky or rate-limited. Spotrack uses a multi-layered approach to stay working:
- **Search API**: If the app fails to find tracks, open **⚙ Settings** and try a different "Search API" URL (e.g., from a Piped or Invidious instance list).
- **Local Bridge (Experimental)**: For 100% reliability, you can run a small Python script locally that bridges Spotrack to your local `yt-dlp` installation. See Settings for the command.
- **Cobalt Instance**: You can switch the downloader instance if the default is down.
- **Retry**: Use the **↺ Retry Failed** button to attempt failed downloads again after a short wait.
- **Delay**: Increase the delay between tracks in Settings to reduce the chance of being blocked.

### Storage Limits
Spotrack saves your track list in your browser's local storage. If you load thousands of tracks, you might hit the storage limit (typically 5MB).
- If you see a storage warning, try clearing "Done" tracks using the **✕ Clear Done** button.

---

*Note: Spotrack does not host any audio files. It is a client-side tool that interfaces with public search and conversion APIs.*
