# thanks https://github.com/tiangolo/meinheld-gunicorn-flask-docker/blob/master/python3.7/Dockerfile

import json
import multiprocessing
import os

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "2")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
host = os.getenv("HOST", "0.0.0.0")
if os.getenv('FLASK_ENV', 'development') == 'production':
    port = os.getenv("PORT", "8000")
    errorlog = "/logs/web/gunicorn.error.log"
else:
    #  on a unix-like environment, ports < 1024 (like 80) will require superuser privileges.
    # port need as same as config.config.py SERVER_NAME port
    port = os.getenv("PORT", "5000")
bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = int(default_web_concurrency)

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
keepalive = 120

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    # Additional, non-gunicorn variab`les
    "workers_per_core": workers_per_core,
    "host": host,
    "port": port,
}
print(json.dumps(log_data))
