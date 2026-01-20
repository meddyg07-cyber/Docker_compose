from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # <-- autorise le frontend

TOR_PROXY = os.getenv("TOR_PROXY", "socks5://tor:9050")

@app.route("/users")
def users():
    url = "https://randomuser.me/api/?results=10"
    proxies = {"http": TOR_PROXY, "https": TOR_PROXY}

    response = requests.get(url, proxies=proxies, timeout=10)
    data = response.json()

    simplified = []
    for user in data["results"]:
        simplified.append({
            "name": f"{user['name']['first']} {user['name']['last']}",
            "photo": user["picture"]["thumbnail"],
            "email": user["email"],
        })

    return jsonify(simplified)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
