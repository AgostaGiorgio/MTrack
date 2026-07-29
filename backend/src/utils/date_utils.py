from datetime import datetime
from typing import Optional


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


def get_current_mtrack_year_month() -> tuple[int, int]:
    now = datetime.now()
    if now.day < 3:
        if now.month == 1:
            return (now.year - 1, 12)
        return (now.year, now.month - 1)
    return (now.year, now.month)


def get_mtrack_month_range(
    year: Optional[int] = None, month: Optional[int] = None
) -> tuple[datetime, datetime]:
    if year is None or month is None:
        year, month = get_current_mtrack_year_month()
    start_date = datetime(year, month, 3)
    if month == 12:
        end_date = datetime(year + 1, 1, 3)
    else:
        end_date = datetime(year, month + 1, 3)
    return (start_date, end_date)