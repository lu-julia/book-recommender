import os
import sys

from loguru import logger


# Create logs directory
os.makedirs("logs", exist_ok=True)

# Remove default logger
logger.remove()

# Add console output
logger.add(
    sink=sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>"
)

# Add file output
logger.add(
    "logs/app.log",
    level="INFO",
    rotation="500 KB",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    encoding='utf-8',
)
