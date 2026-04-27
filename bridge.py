import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/json', methods=['POST'])
def cobalt_mock():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"status": "error", "text": "No URL provided"}), 400

    print(f"[*] Processing: {url}")

    try:
        # Use yt-dlp to get the direct audio URL
        # We use -g to get the URL without downloading
        cmd = ["yt-dlp", "-f", "bestaudio", "-g", url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # yt-dlp -g can return multiple URLs (e.g. for different formats), we take the first one
        direct_url = result.stdout.strip().split('\n')[0]

        # Extract Video ID for thumbnail
        video_id = None
        if "watch?v=" in url:
            import re
            match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
            if match:
                video_id = match.group(1)
        elif "youtu.be/" in url:
            video_id = url.split("/")[-1].split("?")[0]

        return jsonify({
            "status": "stream",
            "url": direct_url,
            "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else None
        })
    except Exception as e:
        print(f"[!] Error: {e}")
        return jsonify({"status": "error", "text": str(e)}), 500

if __name__ == '__main__':
    print("--- Spotrack Local Bridge ---")
    print("This script allows Spotrack to use your local yt-dlp installation.")
    print("Keep this running and set 'Cobalt Instance' in Spotrack to: http://localhost:5000")
    print("-----------------------------")
    app.run(port=5000)
