import sqlite3
from datetime import datetime

class Logger:
    def __init__(self):
        self.conn = sqlite3.connect("uptime.db")
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS uptime_logs (
                id INTEGER PRIMARY KEY,
                url TEXT,
                status_code INTEGER,
                response_time REAL,
                timestamp DATETIME,
                status TEXT
            )''')

    def log_status(self, url: str, status_code: int, response_time: float, status: str):
        with self.conn:
            self.conn.execute('''INSERT INTO uptime_logs 
                              (url, status_code, response_time, timestamp, status)
                              VALUES (?,?,?,?,?)''',
                              (url, status_code, response_time, datetime.now(), status))
