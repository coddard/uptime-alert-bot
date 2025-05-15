from dataclasses import dataclass

@dataclass
class WebsiteStatus:
    url: str
    check_interval: int
    consecutive_failures: int = 0
    last_status: int = 0
    last_response_time: float = 0.0
    is_online: bool = True
    notified: bool = False
