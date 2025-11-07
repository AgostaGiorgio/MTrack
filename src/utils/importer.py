from src.db.models.expense import Expense
from src.config.logger import *
import io, csv
import datetime

logger = logging.getLogger(__name__)


DATE_FORMAT = "%d/%m/%Y, %H:%M"

def import_from_csv(file_bytes: bytes) -> list[Expense] | None:
    try:
        file_text = file_bytes.decode('utf-8')
        text_buffer = io.StringIO(file_text)
        
        reader = csv.DictReader(text_buffer)
        
        expenses = []
        for expense in reader:
            parsed_date = datetime.datetime.strptime(expense["timestamp"], DATE_FORMAT)
            expense["timestamp"] = parsed_date
            cleaned_amount = expense["amount"].strip().replace('$', '').replace(',', '')
            expense["amount"] = float(cleaned_amount)
            cleaned_reimbursed = expense["reimbursed"].strip().replace('$', '').replace(',', '')
            expense["reimbursed"] = float(cleaned_reimbursed)
            expenses.append(Expense(**expense))
        
        logger.info(f"Imported {len(expenses)} expenses from CSV.")
        return expenses
    except Exception as e:
        logger.error(f"Import Error: {e}")
        return None