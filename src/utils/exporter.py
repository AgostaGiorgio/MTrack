from src.config.logger import *
from io import BytesIO, StringIO

import csv

from src.db.models.expense import Expense

logger = logging.getLogger(__name__)

EXPORT_FILE_NAME = "transactions.csv"

def export_csv(expenses: list[Expense]) -> BytesIO | None:
    data_list = [exp.to_dict() for exp in expenses]
    keys = data_list[0].keys()

    try:
        text_buffer = StringIO()
        
        writer = csv.DictWriter(text_buffer, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data_list)
        
        csv_bytes = text_buffer.getvalue().encode('utf-8')
        byte_buffer = BytesIO(csv_bytes)
        byte_buffer.name = EXPORT_FILE_NAME
        
        logger.debug(f"Successfully sent in-memory file: {EXPORT_FILE_NAME}")
        return byte_buffer
    except Exception as e:
        logger.error(f"Error generating or sending in-memory CSV: {e}")
        return None