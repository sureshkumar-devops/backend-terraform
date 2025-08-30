from flask import Flask, jsonify
import mysql.connector


import os

app = Flask(__name__)

db_config = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "admin"),
    'password': os.getenv("DB_PASS", "password"),
    'database': os.getenv("DB_NAME", "myappdb")
}

@app.route("/users")
def get_users():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
