
import logging

# Configure root logger once
logging.basicConfig(
    filename="logs/application.logs",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s():%(lineno)d- %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create your logger instance
logger = logging.getLogger("application")

# Make sure it propagates logs to root logger which has the handler
logger.propagate = True

# Optional: set level explicitly
logger.setLevel(logging.INFO)

