# backend/app.py
from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")



@app.route("/")
def home():
    return "Backend is running!"

@app.route("/api")
def api():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email FROM users")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"message": "Backend connected to DB!", "users": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
