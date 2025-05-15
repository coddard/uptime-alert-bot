import os
import requests

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_alert(self, message: str, priority: str = "normal") -> bool:
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "Markdown",
                    "disable_notification": priority == "low"
                },
                timeout=5
            )
            return True
        except Exception:
            return False