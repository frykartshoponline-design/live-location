"""
app.py
======
Yeh Flask server:
1. index.html (check-in page) ko serve karta hai
2. /checkin endpoint par student ki location leta hai
3. bot.py ke through us location ko Telegram par teacher ko bhejta hai

Chalane ke liye:
    pip install -r requirements.txt
    python app.py
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from bot import send_location_to_teacher

app = Flask(__name__, static_folder=".", static_url_path="")


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/checkin", methods=["POST"])
def checkin():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "Unknown").strip()
    lat = data.get("lat")
    lng = data.get("lng")
    accuracy = data.get("accuracy", 0)

    if lat is None or lng is None:
        return jsonify({"ok": False, "error": "location missing"}), 400

    sent = send_location_to_teacher(name, float(lat), float(lng), float(accuracy))
    return jsonify({"ok": sent})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
