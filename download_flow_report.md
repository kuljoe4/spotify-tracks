# Spotrack Download Flow Test Report

## Summary
The investigation found that the current default configuration of Spotrack is largely broken due to the instability of public Piped and Cobalt instances. The "Local Bridge" method remains the only 100% reliable way to download tracks.

---

## 1. Search API Flow (Piped/Invidious)
**Tested Instances:** 9 public instances.
- **Default (pipedapi.kavin.rocks):** ❌ **FAILED**. Returns Cloudflare Error 526 (Invalid SSL Certificate).
- **Working Instance found:** ✅ `api.piped.private.coffee`. Successfully returns video IDs and titles.
- **Others (Leptons, Lunar, etc.):** ❌ **FAILED**. Most return 502 Bad Gateway, 403 Forbidden, or have expired SSL certificates.
- **Why Failure?** Public Piped/Invidious instances are frequently rate-limited by YouTube or lack maintenance, leading to SSL issues and server errors.

## 2. Cobalt Downloader Flow
**Tested Instances:**
- **Default (co.wuk.sh):** ❌ **FAILED**. Host no longer resolves (NXDOMAIN).
- **Official (api.cobalt.tools):** ❌ **FAILED**. Now requires JWT authentication (`error.api.auth.jwt.missing`).
- **Public Instances:** ❌ **FAILED**. Most found via search are either down or have implemented aggressive Cloudflare protection that blocks API access.
- **Why Failure?** Public Cobalt instances are expensive to run and often face legal pressure or high traffic, leading to shutdowns or the implementation of mandatory authentication.

## 3. Direct Search Mode
- **Status:** ❌ **FAILED** (in current default setup).
- **Why Failure?** Since the default Cobalt instance is down, sending queries directly to it fails. Even when using a local bridge, `yt-dlp` can sometimes be rate-limited by YouTube when processing search result pages (`429: Too Many Requests`).

## 4. Local Bridge Flow (`bridge.py`)
- **Status:** ✅ **WORKING**.
- **Test Result:** Successfully extracted direct `googlevideo.com` audio stream URLs using local `yt-dlp`. Verified that the stream URLs are functional by fetching sample data chunks.
- **Note:** This is currently the only reliable way to use the application as it bypasses the CORS and rate-limiting issues of public infrastructure.

---

## Recommendations
1.  **Update Defaults:** The default Search API should be updated to a more stable instance (e.g., `api.piped.private.coffee`), although public instances will always be volatile.
2.  **UI Feedback:** Improve the error message when Cobalt fails to explicitly mention that public instances are often restricted and suggest the Local Bridge more prominently.
3.  **Documentation:** Clearly state that `co.wuk.sh` is down and users should find a new instance or run their own.
