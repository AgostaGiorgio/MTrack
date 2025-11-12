from src.utils.charts import create_trend_chart, create_category_chart
from src.config.logger import *
from io import BytesIO, StringIO
from jinja2 import Environment, FileSystemLoader
import csv, datetime
from weasyprint import HTML

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
    
def export_annual(expenses: list[Expense], currency: str = "AED") -> BytesIO | None:
    def format_currency(value):
        return f"{currency} {value:,.0f}"
    
    year = expenses[0].timestamp.year

    total_gross = 0
    total_reimbursed = 0
    monthly_trend = [0] * 12
    categories = {}
    category_counts = {}
    pay_methods = {}

    for exp in expenses:
        total_gross += exp.amount
        total_reimbursed += exp.reimbursed
        monthly_trend[exp.timestamp.month - 1] += exp.amount

        cat = exp.primary_category
        categories[cat] = categories.get(cat, 0) + exp.amount
        category_counts[cat] = category_counts.get(cat, 0) + 1

        pm = exp.card_account
        pay_methods[pm] = pay_methods.get(pm, 0) + exp.amount

    total_net = total_gross - total_reimbursed
    monthly_avg = total_net / 12
    
    pay_methods_list = []
    for name, amount in pay_methods.items():
        percent = int((amount / total_gross) * 100) if total_gross > 0 else 0
        pay_methods_list.append({
            'name': name, 
            'amount': format_currency(amount), 
            'percent': percent
        })
    pay_methods_list.sort(key=lambda x: x['percent'], reverse=True)

    sorted_expenses = sorted(expenses, key=lambda x: x.amount, reverse=True)[:10]
    top_expenses_formatted = [{
        'date_str': e.timestamp.strftime("%d/%m/%Y"),
        'desc': e.description,
        'cat': e.primary_category,
        'amount': format_currency(e.amount)
    } for e in sorted_expenses]

    category_analysis_list = []
    for cat_name, total_spend in categories.items():
        count = category_counts.get(cat_name, 0)
        average_spend = total_spend / count if count > 0 else 0
        category_analysis_list.append({
            'name': cat_name,
            'total': total_spend,
            'count': count,
            'average': average_spend
        })

    top_5_categories = sorted(category_analysis_list, key=lambda x: x['total'], reverse=True)[:5]

    top_5_categories_formatted = [{
        'name': cat['name'],
        'total_formatted': format_currency(cat['total']),
        'count': cat['count'],
        'average_formatted': format_currency(cat['average'])
    } for cat in top_5_categories]

    b64_trend = create_trend_chart(monthly_trend)
    b64_cat = create_category_chart(categories, format_currency)

    date_from = datetime.datetime(year, 1, 1).strftime("%B %d, %Y")
    date_to = datetime.datetime.now().strftime("%B %d, %Y")

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("export_template.html")

    html_content = template.render(
        date_from=date_from,
        date_to=date_to,
        generation_date=datetime.datetime.now().strftime("%Y-%m-%d"),
        
        total_gross=format_currency(total_gross),
        total_net=format_currency(total_net),
        monthly_avg=format_currency(monthly_avg),
        monthly_transactions=len(expenses),
        
        chart_trend_b64=b64_trend,
        chart_category_b64=b64_cat,
        
        payment_methods=pay_methods_list,
        top_expenses=top_expenses_formatted,
        
        top_5_categories=top_5_categories_formatted
    )

    content_bytes = HTML(string=html_content).write_pdf()

    return content_bytes