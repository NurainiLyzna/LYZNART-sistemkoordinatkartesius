"""Konfigurasi Gunicorn untuk production (Render)."""
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
workers = int(os.environ.get("WEB_CONCURRENCY", 2))
threads = int(os.environ.get("GUNICORN_THREADS", 4))
timeout = 60
preload_app = True  # init_db() cukup dijalankan sekali oleh proses master
accesslog = "-"
errorlog = "-"
forwarded_allow_ips = "*"
