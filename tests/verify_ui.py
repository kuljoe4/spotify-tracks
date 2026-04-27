from playwright.sync_api import sync_playwright
import os
import subprocess
import time

def run_cuj(page):
    # Load the local HTML file
    file_path = "file://" + os.path.abspath("spotrack.html")
    page.goto(file_path)
    page.wait_for_timeout(1000)

    # 1. Open Settings to verify the new default Search URL and Cobalt URL
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    search_url = page.locator("#search-url").input_value()
    cobalt_url = page.locator("#cobalt-url").input_value()
    print(f"Default Search URL: {search_url}")
    print(f"Default Cobalt URL: {cobalt_url}")

    page.screenshot(path="/home/jules/verification/screenshots/1_settings.png")

    # Close settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(500)

    # 2. Load some tracks
    csv_data = "Track Name,Artist Name(s)\nBlinding Lights,The Weeknd\nNever Gonna Give You Up,Rick Astley"
    page.locator("#csv-input").fill(csv_data)
    page.wait_for_timeout(500)

    page.get_by_role("button", name="Load Tracks").click()
    page.wait_for_timeout(1000)

    # Verify the Art column is present using exact match
    art_header = page.get_by_text("Art", exact=True)
    if art_header.is_visible():
        print("Art column is visible")

    page.screenshot(path="/home/jules/verification/screenshots/2_loaded_tracks_with_art_col.png")

    # 3. Simulate a search (we can't easily wait for real network, but we can verify the fetching state)
    # We'll trigger a single download
    # Note: #row-0 corresponds to global index 0
    page.locator("#row-0 button").first.click() # The download button
    page.wait_for_timeout(1000)

    # Take screenshot during fetching state
    page.screenshot(path="/home/jules/verification/screenshots/3_fetching_state.png")

    print("UI verification complete")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
