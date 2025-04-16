from loguru import logger
import sys
from pathlib import Path

log_path = Path("logs")
log_path.mkdir(exist_ok=True)

logger.remove()  
logger.add(sys.stderr, level="INFO")  
logger.add("logs/app.log", rotation="500 KB", retention="10 days", level="DEBUG")  

log = logger