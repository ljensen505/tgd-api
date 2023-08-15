from dotenv import load_dotenv
from os import environ

load_dotenv()

workers = 4
bind = f"127.0.0.1:{environ.get('PORT')}"
worker_class = f"uvicorn.workers.UvicornWorker"

# gunicorn -c gunicorn_config.py app.main:app
