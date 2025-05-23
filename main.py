from flask import Flask, request, send_file, jsonify
import os
import yt_dlp
import uuid

app = Flask(__name__)

API_KEY = "your_secret_key_here"
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.route("/download/song/<video_id>", methods=["GET"])
def download_song(video_id):
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 403

    try:
        filename = f"{video_id}.mp3"
        filepath = os.path.join(DOWNLOADS_DIR, filename)

        if os.path.exists(filepath):
            return send_file(filepath, mimetype="audio/mpeg")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filepath,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        url = f"https://www.youtube.com/watch?v={video_id}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(filepath):
            return send_file(filepath, mimetype="audio/mpeg")
        else:
            return jsonify({"error": "Download failed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return jsonify({"status": "YouTube MP3 API is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
