import os
import subprocess
import uuid
from flask import Flask, request, jsonify, send_file

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_file('spotrack.html')

@app.route('/api/json', methods=['POST'])
def cobalt_mock():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"status": "error", "text": "No URL provided"}), 400

    if "youtube.com/results?search_query=" in url:
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query).get('search_query', [None])[0]
        if query:
            url = f"ytsearch1:{query}"

    print(f"[*] Downloading: {url}")
    
    filename = f"downloads/{uuid.uuid4()}.mp3"
    try:
        # Download and convert to mp3
        cmd = ["yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "mp3", "-o", filename, url]
        subprocess.run(cmd, check=True)
        
        # In a real app we'd return a URL to the file, but here we can just return the path for the UI to request
        # Actually, let's just return the filename and add a /download route.
        return jsonify({
            "status": "stream",
            "url": f"/download/{os.path.basename(filename)}",
            "thumbnail": None
        })
    except Exception as e:
        print(f"[!] Error: {e}")
        return jsonify({"status": "error", "text": str(e)}), 500

@app.route('/download/<filename>')
def serve_file(filename):
    return send_file(os.path.join('downloads', filename))

if __name__ == '__main__':
    if not os.path.exists('downloads'): os.makedirs('downloads')
    app.run(port=5000)
