import os
import psycopg2
import requests
import socks
import socket
from flask import Flask, jsonify

# -------- Tor proxy --------
socks.set_default_proxy(socks.SOCKS5, "tor", 9050)
socket.socket = socks.socksocket

# -------- ENV --------
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# -------- Flask --------
app = Flask(__name__)

# -------- PostgreSQL --------
def get_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

@app.route("/init")
def init():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    """)
    db.commit()
    return "DB OK"

@app.route("/users")
def users():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT name,email FROM users")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route("/fetch")
def fetch_users():
    # This MUST go through TOR
    r = requests.get("https://randomuser.me/api/?results=5")
    data = r.json()["results"]

    db = get_db()
    cur = db.cursor()

    for u in data:
        name = f"{u['name']['first']} {u['name']['last']}"
        email = u["email"]
        cur.execute("INSERT INTO users (name,email) VALUES (%s,%s)", (name,email))

    db.commit()
    return "Inserted via TOR"

app.run(host="0.0.0.0", port=int(os.getenv("BACKEND_PORT")))
