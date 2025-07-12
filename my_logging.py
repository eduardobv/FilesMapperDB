import logging
import os

def setup_logger(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    from datetime import datetime
    fecha = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(log_dir, f'mapper_{fecha}.log')
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
