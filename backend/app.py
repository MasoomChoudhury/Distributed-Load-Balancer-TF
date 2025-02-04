from flask import Flask, jsonify
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get server ID from environment variable, default to "backend-1"
server_id = os.environ.get("SERVER_ID", "backend-1")

@app.route('/')
def backend_service():
    logging.info(f"Request received at backend server: {server_id}")
    return jsonify({"message": "Hello from backend", "server": server_id}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) # Default port for backend, can be overridden by docker-compose
