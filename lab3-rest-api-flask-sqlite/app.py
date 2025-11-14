from flask import Flask, request, jsonify
from functools import wraps
from db import get_db, init_db
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "b2f4cd8d5e93ab4b0cc11dd6ca0bbf59c34e0fca813c45b6afc25c0458a1c3f9"

def log_request(username):
    conn = get_db()
    conn.execute(
        "INSERT INTO logs (username, method, path, ip) VALUES (?, ?, ?, ?)",
        (username, request.method, request.path, request.remote_addr)
    )
    conn.commit()

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split()
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token required"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = data["username"]
        except:
            return jsonify({"error": "Invalid token"}), 401

        log_request(username)
        return f(username, *args, **kwargs)

    return wrapper

@app.route("/token", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?", 
        (username, password)
    ).fetchone()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token})

@app.route("/items", methods=["GET", "POST"])
@token_required
def items(username):
    conn = get_db()

    if request.method == "GET":
        rows = conn.execute("SELECT * FROM items").fetchall()
        return jsonify([dict(r) for r in rows])

    if request.method == "POST":
        data = request.json
        conn.execute(
            "INSERT INTO items (id, name, price) VALUES (?, ?, ?)",
            (data["id"], data["name"], data["price"])
        )
        conn.commit()
        return jsonify({"message": "Item created"}), 201


@app.route("/items/<int:item_id>", methods=["GET", "PUT", "DELETE"])
@token_required
def item(username, item_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()

    if not item:
        return jsonify({"error": "Item not found"}), 404

    if request.method == "GET":
        return jsonify(dict(item))

    if request.method == "PUT":
        data = request.json
        conn.execute(
            "UPDATE items SET name=?, price=? WHERE id=?",
            (data["name"], data["price"], item_id)
        )
        conn.commit()
        return jsonify({"message": "Item updated"})

    if request.method == "DELETE":
        conn.execute("DELETE FROM items WHERE id=?", (item_id,))
        conn.commit()
        return jsonify({"message": "Item deleted"})

if __name__ == "__main__":
    init_db()

    conn = get_db()
    conn.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("admin", "1234")
    )
    conn.commit()

    app.run(debug=True)
