import logging
import os
from datetime import datetime

def configurar_logger():
    os.makedirs("logs", exist_ok=True)
    data_execucao = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_log = os.path.join("logs", f"log_{data_execucao}.txt")

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(caminho_log, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
