
import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logging():
    # Configuração do formato da mensagem de log
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Configuração do manipulador de arquivo rotativo
    # O arquivo de log terá no máximo 10MB e manterá até 5 arquivos de backup.
    log_file_handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=5)
    log_file_handler.setFormatter(log_formatter)
    log_file_handler.setLevel(logging.INFO)

    # Configuração do manipulador de console
    log_console_handler = logging.StreamHandler(sys.stdout)
    log_console_handler.setFormatter(log_formatter)
    log_console_handler.setLevel(logging.INFO)

    # Configuração do logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(log_file_handler)
    root_logger.addHandler(log_console_handler)

    # Redireciona os logs do uvicorn para o nosso manipulador
    logging.getLogger('uvicorn.access').handlers = [log_file_handler, log_console_handler]
    logging.getLogger('uvicorn.error').handlers = [log_file_handler, log_console_handler]
