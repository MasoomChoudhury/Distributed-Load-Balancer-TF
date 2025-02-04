from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Backend servers list
backend_servers = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]

# Round Robin counter
rr_counter = 0

# Inefficiencies for demonstration (simulated bottleneck)
import time
SIMULATED_DELAY = 0.01  # 10ms delay

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def load_balancer(path):
    global rr_counter

    # Simulate processing delay (inefficiency)
    time.sleep(SIMULATED_DELAY) # Simulate a small delay in processing each request

    backend_url = backend_servers[rr_counter % len(backend_servers)]
    rr_counter += 1

    forward_url = f"{backend_url}/{path}"
    logging.info(f"Forwarding request to: {forward_url}")

    try:
        response = requests.request(
            method=request.method,
            url=forward_url,
            headers=request.headers,
            data=request.get_data(),
            params=request.args
        )
        logging.info(f"Backend responded with status code: {response.status_code}")
        return jsonify(response.json()), response.status_code
    except requests.ConnectionError as e:
        logging.error(f"Error connecting to backend: {e}")
        return jsonify({"error": "Error connecting to backend server"}), 502

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
