from fastapi import Request, HTTPException
import time
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self, requests_per_second: int = 10):
        self.requests_per_second = requests_per_second
        self.requests: Dict[str, Tuple[int, float]] = {}

    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        current_time = time.time()
        
        if client_ip in self.requests:
            count, start_time = self.requests[client_ip]
            if current_time - start_time >= 1:
                self.requests[client_ip] = (1, current_time)
            elif count >= self.requests_per_second:
                raise HTTPException(status_code=429, detail="Too many requests")
            else:
                self.requests[client_ip] = (count + 1, start_time)
        else:
            self.requests[client_ip] = (1, current_time) 