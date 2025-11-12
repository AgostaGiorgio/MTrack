import base64, io
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

MONTHS_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def create_trend_chart(monthly_data):
    fig, ax = plt.subplots(figsize=(10, 4))
    x = np.arange(len(MONTHS_LABELS))

    x_smooth = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, monthly_data, k=3)
    y_smooth = spline(x_smooth)

    ax.fill_between(x_smooth, y_smooth, color='#1f2937', alpha=0.1, zorder=1)
    ax.plot(x_smooth, y_smooth, color='#1f2937', linewidth=2, zorder=2)
    ax.scatter(x, monthly_data, color='#1f2937', zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(MONTHS_LABELS)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_ylim(bottom=0)

    for xi, yi in zip(x, monthly_data):
        ax.text(
            xi, yi + (max(monthly_data) * 0.05),
            f"{yi:.0f}",
            ha='center', va='bottom',
            fontsize=9,
            color='#111827', 
            fontweight='bold',
            zorder=4,
            bbox=dict(
                boxstyle='round,pad=0.15',
                facecolor='white',
                edgecolor='none',
                alpha=0.7
            )
        )

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def create_category_chart(categories_dict, format_currency_func):
    filtered_cats = {k: v for k, v in categories_dict.items() if v > 0}
    if not filtered_cats:
        return ""

    labels = list(filtered_cats.keys())
    sizes = list(filtered_cats.values())
    sorted_pairs = sorted(zip(sizes, labels), reverse=True)
    sizes = [s for s, l in sorted_pairs]
    labels = [l for s, l in sorted_pairs]
    
    colors = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#9ca3af']

    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors[:len(sizes)],
        wedgeprops=dict(width=0.5, edgecolor='white'),
        pctdistance=0.75,
        textprops={'fontsize': 9}
    )
    plt.setp(autotexts, size=8, weight="bold", color="white")

    legend_labels = [
        f"{label} — {format_currency_func(value)}" 
        for label, value in zip(labels, sizes)
    ]
    ax.legend(
        wedges,
        legend_labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=12,
        title_fontsize=14
    )
    ax.axis('equal')

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')
