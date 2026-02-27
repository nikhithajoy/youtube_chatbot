import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import get_settings

LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

def configure_logging():
    # Delay reading settings until this function is called so importing this
    # module doesn't trigger pydantic validation (which can raise if required
    # env vars are missing). This prevents ImportError during application
    # startup (for example when uvicorn imports `app.main`).
    settings = get_settings()
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler(
                LOG_FILE,
                maxBytes=5*1024*1024,
                backupCount=3,
            ),
        ],
    )
    

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)