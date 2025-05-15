import requests
import validators
from time import time
from typing import Dict, Tuple
from models.website import WebsiteStatus
from prometheus_client import Counter, Gauge

METRIC_REQUESTS = Counter('uptime_checks_total', 'Total checks')
METRIC_FAILURES = Counter('uptime_failures_total', 'Failed checks')
METRIC_RESPONSE_TIME = Gauge('uptime_response_time_ms', 'Response time')

class WebsiteChecker:
    def __init__(self):
        self.website_statuses: Dict[str, WebsiteStatus] = {}

    def validate_url(self, url: str) -> bool:
        return validators.url(url)

    def check_website(self, website: dict) -> Tuple[bool, int, float]:
        if not self.validate_url(website['url']):
            raise ValueError(f"Invalid URL format: {website['url']}")

        try:
            start_time = time()
            response = requests.get(
                website['url'],
                timeout=10,
                headers={'User-Agent': 'UptimeChecker/2.0'},
                allow_redirects=False
            )
            response_time = (time() - start_time) * 1000
            
            METRIC_REQUESTS.inc()
            METRIC_RESPONSE_TIME.set(response_time)
            
            return (response.ok, response.status_code, response_time)
        except Exception as e:
            METRIC_FAILURES.inc()
            return (False, 0, 0)
