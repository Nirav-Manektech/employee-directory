# app/utils/rate_limiter.py

import time
from collections import defaultdict

# Simple memory-based limiter: {key: [timestamps]}
rate_store = defaultdict(list)

# Configuration
RATE_LIMIT = 100
WINDOW_SECONDS = 600  # 10 minutes


def is_rate_limited(key: str) -> bool:
    now = time.time()
    window_start = now - WINDOW_SECONDS

    recent_requests = [ts for ts in rate_store[key] if ts >= window_start]
    rate_store[key] = recent_requests

    if len(recent_requests) >= RATE_LIMIT:
        return True

    rate_store[key].append(now)
    return False