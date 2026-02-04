import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8080" # Portforward to your cloud-calculator instance
TOTAL_REQUESTS = 40          # All Requests to send
CONCURRENT_USERS = 10        # Concurrent requests

def send_request(i):
    try:
        # Simple Calculation 
        payload = {"username": "bench", "expression": "2*2"}
        start = time.time()
        resp = requests.post(f"{URL}/calculate", json=payload)
        latency = time.time() - start
        return latency
    except Exception as e:
        return None

print(f"🚀 Starting Benchmark: {TOTAL_REQUESTS} requests ({CONCURRENT_USERS} concurrent)...")
print("-" * 40)

start_time = time.time()

# Send requests concurrently
with ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:
    results = list(executor.map(send_request, range(TOTAL_REQUESTS)))

duration = time.time() - start_time
successful = len([r for r in results if r is not None])
rps = successful / duration

print("-" * 40)
print(f"✅ Finished in: {duration:.2f} seconds")
print(f"⚡ Throughput:  {rps:.2f} Requests/Second")
print("-" * 40)