import logging
import os

from flask import Flask

from .views.auth import auth_api

log_level_name = os.environ.get("SFM_LOG_LEVEL", "INFO")
log_level = getattr(logging, log_level_name)
logging.basicConfig(
    format="[%(asctime)s] %(name)s - %(levelname)s: %(message)s", level=log_level
)

app = Flask(__name__)
app.register_blueprint(auth_api)
