import logging 
import os

LOG_DIR="logs"
os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE=os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  
        logging.StreamHandler()  
    ]
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)