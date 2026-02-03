import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8080" # Port-forwarded address of the orchestrator service
TOTAL_REQUESTS = 50  # All requests to send
CONCURRENCY = 10     # Number of concurrent threads

def send_request(i):
    try:
        payload = {"username": "bench-user", "expression": "2 * 2"}
        start = time.time()
        requests.post(URL, json=payload)
        return time.time() - start
    except:
        return 0

print(f"🚀 Starting Benchmark: {TOTAL_REQUESTS} requests...")
start_time = time.time()

with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
    list(executor.map(send_request, range(TOTAL_REQUESTS)))

duration = time.time() - start_time
rps = TOTAL_REQUESTS / duration

print("\n" + "="*30)
print(f"⏱️  Total Time: {duration:.2f} seconds")
print(f"⚡ Throughput: {rps:.2f} Requests/Second")
print("="*30)