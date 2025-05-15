import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class WhatsAppNotifier:
    def __init__(self):
        self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        self.from_number = f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}"
        self.to_number = f"whatsapp:{os.getenv('RECIPIENT_WHATSAPP_NUMBER')}"

    def send_alert(self, message: str, priority: str = "normal") -> bool:
        try:
            self.client.messages.create(
                body=f"{'🚨' if priority == 'high' else '⚠️'} {message}",
                from_=self.from_number,
                to=self.to_number
            )
            return True
        except TwilioRestException:
            return False