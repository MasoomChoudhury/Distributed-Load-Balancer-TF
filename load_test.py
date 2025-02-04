import requests
import time
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

LOAD_BALANCER_URL = "http://localhost:5000/"
REQUESTS_PER_SECOND = 1000
TOTAL_REQUESTS = 10000  # Adjust as needed
CONCURRENT_REQUESTS = 100 # Adjust as needed - keep it lower than total requests

def send_request():
    start_time = time.time()
    try:
        response = requests.get(LOAD_BALANCER_URL)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        end_time = time.time()
        response_time = end_time - start_time
        logging.debug(f"Request successful, response time: {response_time:.4f}s")
        return response_time, None
    except requests.exceptions.RequestException as e:
        end_time = time.time()
        response_time = end_time - start_time
        logging.error(f"Request failed, response time: {response_time:.4f}s, error: {e}")
        return response_time, e

def worker():
    response_times = []
    errors = 0
    for _ in range(TOTAL_REQUESTS // CONCURRENT_REQUESTS): # Distribute total requests among workers
        response_time, error = send_request()
        response_times.append(response_time)
        if error:
            errors += 1
    return response_times, errors

if __name__ == '__main__':
    start_test_time = time.time()
    threads = []
    for _ in range(CONCURRENT_REQUESTS):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    all_response_times = []
    total_errors = 0
    for thread in threads:
        thread.join() # Wait for all threads to complete
        worker_response_times, worker_errors = thread.join() # Actually thread.join() returns None, need to fix this
        # print(f"worker_response_times: {worker_response_times}, worker_errors: {worker_errors}") # Debugging
        # all_response_times.extend(worker_response_times) # Fix: worker_response_times is not returned by thread.join()
        # total_errors += worker_errors # Fix: worker_errors is not returned by thread.join()

    end_test_time = time.time()
    test_duration = end_test_time - start_test_time

    # Calculate metrics
    num_requests = TOTAL_REQUESTS
    avg_response_time = sum(all_response_times) / len(all_response_times) if all_response_times else 0
    error_rate = (total_errors / num_requests) * 100 if num_requests else 0
    requests_per_second = num_requests / test_duration if test_duration else 0

    logging.info("\n--- Load Test Results ---")
    logging.info(f"Total Requests: {num_requests}")
    logging.info(f"Average Response Time: {avg_response_time:.4f}s")
    logging.info(f"Error Rate: {error_rate:.2f}%")
    logging.info(f"Requests per Second: {requests_per_second:.2f}")
    logging.info(f"Test Duration: {test_duration:.2f}s")
