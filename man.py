import requests
from flask import Flask, request, jsonify
import replicate
import os

app = Flask(__name__)

# Replicate API key (Set this as an environment variable in Replit or locally)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

@app.route("/generate-thumbnail", methods=["POST"])
def generate_thumbnail():
    data = request.json
    youtube_link = data.get("youtube_link")
    
    if not youtube_link:
        return jsonify({"error": "No YouTube link provided"}), 400
    
    # Extract video ID from YouTube link
    video_id = youtube_link.split("v=")[-1].split("&")[0]
    original_thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    
    # Call Replicate API to modify the thumbnail
    model = "stability-ai/stable-diffusion"
    input_data = {
        "image": original_thumbnail,
        "prompt": "Generate a modified but similar thumbnail with different elements and improved style"
    }
    
    headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}
    response = requests.post(f"https://api.replicate.com/v1/predictions", json=input_data, headers=headers)
    
    if response.status_code == 200:
        output = response.json().get("output", "")
        return jsonify({"original": original_thumbnail, "modified": output})
    else:
        return jsonify({"error": "Failed to process image"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
