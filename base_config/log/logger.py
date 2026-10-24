import logging
import os
from pathlib import Path
import colorlog

path_file = Path(__file__).parents[2] / "log" / "dialog.log"



def set_logger(path_file):
    os.makedirs(os.path.dirname(path_file), exist_ok=True)
    logger = logging.getLogger("Ecomm_log")
    logger.setLevel("INFO")
    if not logger.handlers:
        file_handler = logging.FileHandler(path_file,encoding='utf-8')
        file_handler.setLevel("INFO")
        cmd_handler = logging.StreamHandler()
        cmd_handler.setLevel("INFO")
        format_template = colorlog.ColoredFormatter("%(log_color)s%(asctime)s-%(name)s-%(levelname)s-%(message)s")
        file_handler.setFormatter(format_template)
        cmd_handler.setFormatter(format_template)
        logger.addHandler(file_handler)
        logger.addHandler(cmd_handler)
    return logger

logger = set_logger(path_file)
