from datetime import datetime

def get_mtrack_month(date: datetime) -> str:
    if date.day < 3:
        if date.month == 1:
            month = 12
            year = date.year - 1
        else:
            month = date.month - 1
            year = date.year
    else:
        month = date.month
        year = date.year

    result = datetime(year, month, 1).strftime("%B %Y")
    return result