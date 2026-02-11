from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "No URL"}), 400

    # These settings are specialized for Vercel's speed
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            link = info.get('url') or (info.get('entries') and info['entries'][0].get('url'))
            
            if link:
                return jsonify({"status": "success", "link": link})
            else:
                return jsonify({"status": "error", "message": "Could not extract link"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": "Instagram blocked the request. Try again in a few minutes."}), 500

# This is required for Vercel
def handler(event, context):
    return app(event, context)
