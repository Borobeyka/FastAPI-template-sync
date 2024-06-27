import logging
import logging.handlers as handlers
import sys
from os import environ
from pathlib import Path

import uvicorn
from fastapi.logger import logger

LOG_DIR = Path("/logs") if not environ.get("LOG_DIR") else Path(environ.get("LOG_DIR"))

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

logHandler = handlers.TimedRotatingFileHandler(
    LOG_DIR / "info.log", when="D", interval=7, backupCount=0
)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)

errorLogHandler = handlers.TimedRotatingFileHandler(
    LOG_DIR / "error.log", when="D", interval=7, backupCount=0
)
errorLogHandler.setLevel(logging.ERROR)
errorLogHandler.setFormatter(formatter)

logger.handlers.clear()
logger.addHandler(logHandler)
logger.addHandler(errorLogHandler)


log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["default"][
    "fmt"
] = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
log_config["handlers"]["accessfile"] = {
    "class": "logging.handlers.TimedRotatingFileHandler",
    "formatter": "default",
    "filename": LOG_DIR / "access.log",
    "when": "D",
    "interval": 7,
    "backupCount": 0,
}
log_config["handlers"]["error"] = {
    "class": "logging.handlers.TimedRotatingFileHandler",
    "formatter": "default",
    "filename": LOG_DIR / "error.log",
    "when": "D",
    "interval": 7,
    "backupCount": 0,
    "level": "ERROR",
}
log_config["loggers"]["uvicorn.access"]["handlers"] = ["access", "accessfile"]
log_config["loggers"]["uvicorn.error"]["handlers"] = ["error"]
log_config["loggers"]["uvicorn.error"]["level"] = "INFO"
# print(log_config)
