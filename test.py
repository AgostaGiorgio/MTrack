import datetime
import io
import base64
import matplotlib.pyplot as plt
from jinja2 import Template
from weasyprint import HTML, CSS

# --- 1. CONFIGURAZIONE GRAFICA MATPLOTLIB ---
plt.style.use('ggplot')
params = {
    'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 10, 'axes.labelsize': 10, 'xtick.labelsize': 9, 'ytick.labelsize': 9,
    'figure.facecolor': 'white', 'axes.facecolor': 'white', 'axes.grid': True,
    'grid.color': '#f0f0f0', 'grid.linestyle': '--',
}
plt.rcParams.update(params)

# --- 2. TEMPLATE HTML (Include Metodi di Pagamento) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Report Spese</title>
    <style>
        @page { size: A4; margin: 15mm; }
        body { font-family: sans-serif; -webkit-print-color-adjust: exact; color: #333; }
        h1, h2, h3 { color: #1f2937; }
        .page-break { page-break-after: always; }
        
        /* Layout */
        .header { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #1f2937; padding-bottom: 10px; margin-bottom: 25px; }
        .kpi-grid { margin-bottom: 25px; }
        .kpi-box { width: 22%; float: left; padding: 10px; border-radius: 5px; box-sizing: border-box; }
        .kpi-box:not(:last-child) { margin-right: 2.66%; }
        .kpi-box .label { font-size: 10px; color: #666; text-transform: uppercase; font-weight: bold; }
        .kpi-box .value { font-size: 20px; font-weight: bold; }
        
        .chart-container { margin-bottom: 25px; border: 1px solid #eee; padding: 10px; border-radius: 5px; }
        .chart-container h2 { margin-top: 0; padding-left: 8px; border-left: 4px solid #1f2937; }
        
        /* Tabelle */
        table { width: 100%; border-collapse: collapse; margin-bottom: 25px; }
        th { text-align: left; background-color: #1f2937; color: white; padding: 8px; font-size: 12px; }
        td { padding: 8px; border-bottom: 1px solid #eee; font-size: 13px; }
        tbody tr:nth-child(even) { background-color: #f9f9f9; }
        .text-right { text-align: right; }
        .font-mono { font-family: monospace; }
        .font-bold { font-weight: bold; }
        .text-sm { font-size: 13px; }
        .text-xs { font-size: 11px; }
        
        /* Barra % */
        .progress-bar { display: flex; align-items: center; }
        .progress-track { width: 100%; background: #eee; border-radius: 5px; height: 10px; }
        .progress-fill { background: #2563eb; height: 10px; border-radius: 5px; }
        
    </style>
</head>
<body>
    <!-- PAGINA 1 -->
    <div class="header">
        <div>
            <h1 style="font-size: 28px; font-weight: bold; text-transform: uppercase; margin: 0;">Report Finanziario</h1>
            <p style="font-size: 14px; color: #555; margin: 5px 0 0 0;">Periodo: 01 Gennaio {{ year }} – 31 Dicembre {{ year }}</p>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 11px; color: #777; text-transform: uppercase;">Data Report</div>
            <div style="font-weight: bold; font-size: 13px;">{{ generation_date }}</div>
        </div>
    </div>

    <!-- KPI -->
    <div class="kpi-grid">
        <div class="kpi-box" style="background: #f9fafb; border: 1px solid #ddd;">
            <div class="label">Totale Lordo</div>
            <div class="value" style="color: #1f2937;">{{ total_gross }}</div>
        </div>
        <div class="kpi-box" style="background: #eff6ff; border: 1px solid #bfdbfe;">
            <div class="label" style="color: #1d4ed8;">Totale Netto</div>
            <div class="value" style="color: #1e3a8a;">{{ total_net }}</div>
        </div>
        <div class="kpi-box" style="background: #f9fafb; border: 1px solid #ddd;">
            <div class="label">Media Mensile (Netta)</div>
            <div class="value" style="color: #1f2937;">{{ monthly_avg }}</div>
        </div>
        <div class="kpi-box" style="background: #f9fafb; border: 1px solid #ddd;">
            <div class="label">Transazioni</div>
            <div class="value" style="color: #1f2937;">{{ monthly_transactions }}</div>
        </div>
        <div style="clear: both;"></div>
    </div>

    <!-- Grafici -->
    <div class="chart-container">
        <h2>Andamento Spesa Lorda Mensile</h2>
        <img src="data:image/png;base64,{{ chart_trend_b64 }}" style="width: 100%;">
    </div>
    <div class="chart-container" style="text-align: center;">
        <h2>Distribuzione Categorie (Lordo)</h2>
        <img src="data:image/png;base64,{{ chart_category_b64 }}" style="width: 75%; height: auto;">
    </div>

    <div class="page-break"></div>

    <!-- PAGINA 2 -->
    <h3 style="font-size: 14px; font-weight: bold; text-transform: uppercase; margin-top: 25px; margin-bottom: 10px;">Analisi Metodi di Pagamento</h3>
    <table>
        <thead>
            <tr>
                <th>Strumento</th>
                <th style="width: 50%">Volume Utilizzo</th>
                <th class="text-right">Importo Totale (Lordo)</th>
            </tr>
        </thead>
        <tbody>
            {% for pm in payment_methods %}
            <tr>
                <td class="font-medium text-sm">{{ pm.name }}</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-track">
                            <div class="progress-fill" style="width: {{ pm.percent }}%;"></div>
                        </div>
                        <span style="font-size: 12px; color: #555; margin-left: 8px;">{{ pm.percent }}%</span>
                    </div>
                </td>
                <td class="text-right font-mono font-bold text-sm">{{ pm.amount }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <h3 style="font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 10px;">Top 10 Transazioni (Per Valore Lordo)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 15%">Data</th>
                <th>Descrizione</th>
                <th style="width: 20%">Categoria</th>
                <th class="text-right" style="width: 15%">Importo</th>
            </tr>
        </thead>
        <tbody>
            {% for tx in top_expenses %}
            <tr>
                <td class="font-mono text-xs text-gray-600">{{ tx.date_str }}</td>
                <td class="font-medium text-sm">{{ tx.desc }}</td>
                <td class="text-xs uppercase"><span style="background: #eee; padding: 2px 6px; border-radius: 4px;">{{ tx.cat }}</span></td>
                <td class="text-right font-mono font-bold text-sm">{{ tx.amount }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

# --- 3. Funzioni Helper per Matplotlib (Invariate) ---

def create_trend_chart(monthly_data, months_labels):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(months_labels, monthly_data, marker='o', color='#1f2937', linewidth=2)
    ax.fill_between(months_labels, monthly_data, color='#1f2937', alpha=0.1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_ylim(bottom=0)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def create_category_chart(categories_dict):
    # Filtra solo categorie con importo > 0
    filtered_cats = {k: v for k, v in categories_dict.items() if v > 0}
    if not filtered_cats:
        return "" # Ritorna stringa vuota se non ci sono dati

    labels = list(filtered_cats.keys())
    sizes = list(filtered_cats.values())
    sorted_pairs = sorted(zip(sizes, labels), reverse=True)
    sizes = [s for s, l in sorted_pairs]
    labels = [l for s, l in sorted_pairs]

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#9ca3af']
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        wedgeprops=dict(width=0.5, edgecolor='white'), pctdistance=0.85,
        textprops={'fontsize': 9}
    )
    plt.setp(autotexts, size=8, weight="bold", color="white")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# --- 4. FUNZIONE PRINCIPALE (Logica Adattata) ---

def generate_static_pdf_report(expenses_list, year, currency="AED"):
    """
    Genera un report PDF statico da una lista di oggetti Expense (SQLAlchemy).
    """
    
    # Helper per formattare la valuta
    def format_currency(value):
        return f"{currency} {value:,.0f}"

    print(f"1. Inizio elaborazione report per l'anno {year}...")
    
    # Filtra spese per l'anno corretto
    current_year_expenses = [e for e in expenses_list if e.timestamp.year == year]
    
    if not current_year_expenses:
        print(f"Nessuna spesa trovata per il {year}.")
        return None

    # --- AGGREGAZIONE DATI ---
    
    # 1. Calcolo KPI
    total_gross = sum(e.amount for e in current_year_expenses)
    total_reimbursed = sum(e.reimbursed for e in current_year_expenses)
    total_net = total_gross - total_reimbursed
    monthly_avg = total_net / 12

    # 2. Trend Mensile (basato sul Lordo)
    monthly_trend = [0] * 12
    for e in current_year_expenses:
        monthly_trend[e.timestamp.month - 1] += e.amount

    # 3. Categorie (basato sul Lordo)
    categories = {}
    for e in current_year_expenses:
        cat = e.primary_category
        categories[cat] = categories.get(cat, 0) + e.amount

    # 4. Metodi di Pagamento (basato sul Lordo)
    pay_methods = {}
    for e in current_year_expenses:
        pm = e.card_account
        pay_methods[pm] = pay_methods.get(pm, 0) + e.amount
    
    pay_methods_list = []
    for name, amount in pay_methods.items():
        percent = int((amount / total_gross) * 100) if total_gross > 0 else 0
        pay_methods_list.append({
            'name': name, 
            'amount': format_currency(amount), 
            'percent': percent
        })
    pay_methods_list.sort(key=lambda x: x['percent'], reverse=True)

    # 5. Top 10 Spese (basato sul Lordo)
    sorted_expenses = sorted(current_year_expenses, key=lambda x: x.amount, reverse=True)[:10]
    top_expenses_formatted = [{
        'date_str': e.timestamp.strftime("%d/%m/%Y"),
        'desc': e.description,
        'cat': e.primary_category,
        'amount': format_currency(e.amount)
    } for e in sorted_expenses]

    # --- GENERAZIONE GRAFICI ---
    print("2. Generazione grafici con Matplotlib...")
    months_labels = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']
    
    b64_trend = create_trend_chart(monthly_trend, months_labels)
    b64_cat = create_category_chart(categories)

    # --- RENDER HTML ---
    print("3. Rendering Template Jinja...")
    template = Template(HTML_TEMPLATE)
    html_content = template.render(
        year=year,
        generation_date=datetime.datetime.now().strftime("%d/%m/%Y"),
        
        # KPI formattati
        total_gross=format_currency(total_gross),
        total_net=format_currency(total_net),
        monthly_avg=format_currency(monthly_avg),
        monthly_transactions=len(current_year_expenses),
        
        # Dati per grafici (immagini base64)
        chart_trend_b64=b64_trend,
        chart_category_b64=b64_cat,
        
        # Dati per tabelle
        payment_methods=pay_methods_list,
        top_expenses=top_expenses_formatted
    )

    # --- CONVERSIONE PDF (WEASYPRINT) ---
    print("4. Generazione PDF con WeasyPrint...")
    pdf_filename = f"Report_Spese_{year}.pdf"
    
    # WeasyPrint scrive il PDF
    HTML(string=html_content).write_pdf(pdf_filename)
    
    print(f"✅ PDF Generato: {pdf_filename}")
    return pdf_filename

# --- 5. ESECUZIONE (con Mock Class) ---
if __name__ == "__main__":
    
    # Creiamo una Mock Class semplice per simulare il tuo modello SQLAlchemy
    class MockExpense:
        def __init__(self, timestamp, card_account, amount, reimbursed, description, primary_category):
            self.timestamp = timestamp
            self.card_account = card_account
            self.amount = amount
            self.reimbursed = reimbursed
            self.description = description
            self.primary_category = primary_category

    # Creiamo dati di prova
    mock_expenses_list = [
        MockExpense(datetime.datetime(2025, 1, 15), "Visa-1234", 5000, 0, "Affitto Gennaio", "Abitazione"),
        MockExpense(datetime.datetime(2025, 1, 20), "Amex-5678", 450.50, 0, "Spesa Carrefour", "Alimentari"),
        MockExpense(datetime.datetime(2025, 2, 10), "Amex-5678", 1200, 100, "Volo Dubai (rimborso parziale)", "Viaggi"),
        MockExpense(datetime.datetime(2025, 3, 5), "Visa-1234", 300, 300, "Cena di lavoro (rimborsata)", "Ristoranti"),
        MockExpense(datetime.datetime(2025, 5, 12), "Visa-1234", 2100, 0, "Assicurazione Auto", "Trasporti"),
        MockExpense(datetime.datetime(2025, 8, 15), "Amex-5678", 4500, 0, "Hotel Tokyo", "Viaggi"),
    ]
    
    # Aggiungiamo dati random
    import random
    cats = ["Shopping", "Salute", "Svago", "Alimentari"]
    cards = ["Visa-1234", "Amex-5678", "Mastercard-9876"]
    for i in range(50):
        m = random.randint(1, 12)
        d = random.randint(1, 28)
        mock_expenses_list.append(
            MockExpense(
                datetime.datetime(2025, m, d),
                cards[random.randint(0,2)],
                random.uniform(50, 500),
                0,
                "Transazione Random",
                cats[random.randint(0,3)]
            )
        )

    # Genera il report
    generate_static_pdf_report(mock_expenses_list, year=2025, currency="AED")