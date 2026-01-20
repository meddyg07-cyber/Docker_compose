from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = "/data/users.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()

    return jsonify({"id": user_id, "username": username, "password": password})

@app.route("/users", methods=["GET"])
def read_users():
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()

    result = [dict(u) for u in users]
    return jsonify(result)

@app.route("/users/<int:user_id>", methods=["GET"])
def read_user(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return jsonify(dict(user)) if user else jsonify({}), 404

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    conn.execute(
        "UPDATE users SET username = ?, password = ? WHERE id = ?",
        (username, password, user_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"id": user_id, "username": username, "password": password})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"deleted": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)
