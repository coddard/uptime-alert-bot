from flask import Flask, render_template
import sqlite3
from datetime import datetime
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

@app.route("/")
def dashboard():
    conn = sqlite3.connect("uptime.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM uptime_logs ORDER BY timestamp DESC LIMIT 50")
    logs = cursor.fetchall()
    conn.close()
    
    return render_template(
        "index.html",
        logs=logs,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})
