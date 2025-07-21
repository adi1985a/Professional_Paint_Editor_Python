import logging
import os

# Ustawienia loggera do pliku error_log.txt w katalogu programu
log_file = os.path.join(os.path.dirname(__file__), 'error_log.txt')
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_error(msg):
    """Loguje błąd do pliku error_log.txt"""
    logging.error(msg)
