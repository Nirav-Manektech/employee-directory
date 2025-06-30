from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import FastAPI,Request, HTTPException
from starlette.responses import Response
from collections import defaultdict
import time
from starlette.responses import JSONResponse



# Configuration
RATE_LIMIT = 100
WINDOW_SECONDS = 10  # 10 minutes


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self,app: FastAPI):
        super().__init__(app)
        self.rate_store = defaultdict(list)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        now = time.time()
        window_start = now - WINDOW_SECONDS
        org_id = request.headers.get("X-Org-ID")
        client_ip = request.client.host
        key = f"org:{org_id}-ip:{client_ip}"
        recent_requests = [ts for ts in self.rate_store[key] if ts >= window_start]

        self.rate_store[key] = recent_requests

        if len(recent_requests) >= RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many request"},
            )


        self.rate_store[key].append(now)
        response = await call_next(request)

        return response


