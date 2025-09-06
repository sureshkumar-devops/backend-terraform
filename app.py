# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
required_env_vars = ["DB_HOST", "DB_USER", "DB_PASS", "DB_NAME"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT", "3306"),
    "pool_name": "mypool",
    "pool_size": 5
}

# Initialize the connection pool
try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(**DB_CONFIG)
except Exception as e:
    print(f"Error: Could not initialize database connection pool: {str(e)}")
    sys.exit(1)


@app.route("/health")
def health():
    """Health check endpoint"""
    try:
        # Get a connection from the pool to test DB connectivity
        conn = connection_pool.get_connection()
        conn.close()
        return jsonify({
            "status": "healthy",
            "database": "connected"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route("/api")
def api():
    """Get all users from the database"""
    try:
        # Get connection from pool
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, name, email FROM users")
            result = cursor.fetchall()
            return jsonify({
                "status": "success",
                "message": "Data retrieved successfully",
                "users": result
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Database query failed",
                "error": str(e)
            }), 500
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to connect to database",
            "error": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Resource not found"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == "__main__":
    # Add some debug information
    print(f"Starting server on port 8080...")
    print(f"Database host: {DB_CONFIG['host']}")
    print(f"Database name: {DB_CONFIG['database']}")
    
    # Run the application
    app.run(host="0.0.0.0", port=8080, debug=False)
