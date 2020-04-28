import logging
import os

from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy

log_level_name = os.environ.get("SFM_LOG_LEVEL", "INFO")
log_level = getattr(logging, log_level_name)
logging.basicConfig(
    format="[%(asctime)s] %(name)s - %(levelname)s: %(message)s", level=log_level
)

db = SQLAlchemy()
alembic = Alembic()
