import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8080" # Frontend port-forwarded service
TOTAL_REQUESTS = 50           # All requests to send
CONCURRENT_THREADS = 50       # They are all concourrent

def send_request(i):
    try:
        start = time.time()
        # A simple calculation request
        requests.post(f"{URL}/calculate", json={"expression": "2*2+2", "username": "benchmark"}, timeout=5)
        return time.time() - start
    except Exception as e:
        return None

print(f"🚀 Starting Load Test: {TOTAL_REQUESTS} parallel requests...")
print("-" * 40)

global_start = time.time()

# Send all requests concurrently
with ThreadPoolExecutor(max_workers=CONCURRENT_THREADS) as executor:
    results = list(executor.map(send_request, range(TOTAL_REQUESTS)))

total_time = time.time() - global_start
successful = len([r for r in results if r is not None])
rps = successful / total_time

print(f"📊 Results:")
print(f"✅ Successful Requests: {successful}/{TOTAL_REQUESTS}")
print(f"⏱️  Total Time Taken:   {total_time:.2f} seconds")
print(f"⚡ System Throughput:  {rps:.2f} Req/Sec")
print("-" * 40)