# Distributed Load Balancer Testing Framework

This project demonstrates a simple distributed load balancer and an automated test suite to validate its performance under high traffic.

## Components

- **Load Balancer (app.py):** A Python Flask application that implements a Round Robin load balancing algorithm. It forwards requests to multiple backend servers.
- **Backend Server (backend/app.py):** A simple Python Flask backend service that returns a JSON response. It is containerized using Docker.
- **Docker Compose (docker-compose.yml):** Orchestrates the setup of the load balancer and multiple backend server instances using Docker.
- **Load Test Script (load_test.py):** A Python script to simulate high traffic to the load balancer and measure performance metrics.

## Instructions

### Prerequisites

- Docker and Docker Compose installed on your system.
- Python 3.x installed on your system.

### Setup

1.  **Build Docker Images:**
    Navigate to the project root directory in your terminal and run:
    ```bash
    docker-compose build
    ```

2.  **Run Docker Containers:**
    Start the load balancer and backend server containers using:
    ```bash
    docker-compose up -d
    ```

3.  **Run Load Test:**
    Execute the load test script to simulate high traffic:
    ```bash
    python load_test.py
    ```

### Cleanup

To stop and remove the containers, run:
```bash
docker-compose down
```

## Code Structure

- `app.py`: Load balancer application.
- `backend/app.py`: Backend server application.
- `backend/Dockerfile`: Dockerfile for the backend server.
- `docker-compose.yml`: Docker Compose configuration file.
- `load_test.py`: Load testing script.
- `README.md`: This README file.

## Performance Metrics

The `load_test.py` script will output the following metrics:

- Average response time
- Error rate
- Requests per second

## Notes

- This is a simplified demonstration project and is not intended for production use.
- The load balancer includes basic logging for debugging and demonstration purposes.
- The backend server is intentionally simple to focus on the load balancing mechanism.

## Potential Improvements

- **Throughput Optimization:** The current load balancer might have inefficiencies. For example, optimizing the request forwarding logic and connection handling could potentially lead to a 40% throughput improvement. Areas to investigate include:
    - Asynchronous request handling
    - Connection pooling to backend servers
    - Efficient logging mechanisms

---
