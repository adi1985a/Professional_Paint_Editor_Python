import logging
from datetime import datetime
import os

class ErrorLogger:
    def __init__(self):
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, f'paint_errors_{datetime.now().strftime("%Y%m%d")}.log')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        self.logger = logging.getLogger('PaintApp')

    def log_error(self, error, context=""):
        self.logger.error(f"{context}: {str(error)}")

    def log_warning(self, message):
        self.logger.warning(message)
