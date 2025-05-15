import yaml
import logging
import argparse
from dotenv import load_dotenv
from core.checker import WebsiteChecker
from core.scheduler import SchedulerManager
from core.logger import Logger
from notifications.telegram import TelegramNotifier
from notifications.whatsapp import WhatsAppNotifier
from notifications.email import EmailNotifier
from prometheus_client import start_http_server

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description="Website Uptime Checker")
    parser.add_argument("--config", default="config/websites.yaml", help="Config file path")
    parser.add_argument("--no-notify", action="store_true", help="Disable notifications")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING"], default="INFO")
    return parser.parse_args()

def load_config(path: str):
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    args = parse_args()
    logger = logging.getLogger()
    logger.setLevel(args.log_level)
    
    # Prometheus metrik sunucusu
    start_http_server(8000)
    
    websites = load_config(args.config)
    checker = WebsiteChecker()
    scheduler = SchedulerManager()
    notifier = TelegramNotifier()
    whatsapp = WhatsAppNotifier()
    email = EmailNotifier()
    db_logger = Logger()

    for site in websites:
        def check_wrapper(site=site):
            try:
                result, status_code, response_time = checker.check_website(site)
                website_status = checker.website_statuses.get(site['url'], WebsiteStatus(**site))
                
                if result:
                    website_status.consecutive_failures = 0
                    new_status = "up"
                    if not website_status.is_online:
                        message = f"🟢 {site['url']} yeniden çalışıyor! (Yanıt süresi: {response_time}ms)"
                        if not args.no_notify:
                            notifier.send_alert(message, "high")
                            whatsapp.send_alert(message, "high")
                            email.send_alert(message, "Website Yeniden Açıldı", "high")
                        website_status.is_online = True
                        website_status.notified = False
                else:
                    website_status.consecutive_failures += 1
                    new_status = "down"
                    if website_status.consecutive_failures >= 3 and not website_status.notified:
                        message = f"🔴 {site['url']} çöktü! (HTTP {status_code})"
                        if not args.no_notify:
                            notifier.send_alert(message, "high")
                            whatsapp.send_alert(message, "high")
                            email.send_alert(message, "Website Çöktü", "high")
                        website_status.notified = True
                        website_status.is_online = False
                
                db_logger.log_status(site['url'], status_code, response_time, new_status)
                checker.website_statuses[site['url']] = website_status

            except Exception as e:
                logger.error(f"Check error for {site['url']}: {str(e)}")

        scheduler.add_job(check_wrapper, site['check_interval'], site['url'])

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logging.info("Monitoring stopped")

if __name__ == "__main__":
    main()