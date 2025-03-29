from downloader import Downloader
import logging

logging.basicConfig(filename="application.logs",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s():%(lineno)d- %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("application")