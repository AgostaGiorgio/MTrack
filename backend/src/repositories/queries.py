from sqlalchemy import text, TextClause

GET_CARD_SUMMARIES = text("""
    SELECT SUM(amount) AS amount, card as name 
    FROM transactions
    WHERE created_at >= (
        CASE
        WHEN EXTRACT(DAY FROM current_date) >= 3
            THEN date_trunc('month', current_date) + interval '2 days'
        ELSE
            date_trunc('month', current_date) - interval '1 month' + interval '2 days'
        END
    )
    AND created_at < (
        CASE
        WHEN EXTRACT(DAY FROM current_date) >= 3
            THEN date_trunc('month', current_date) + interval '2 days'
        ELSE
            date_trunc('month', current_date) - interval '1 month' + interval '2 days'
        END
    ) + interval '1 month'
    GROUP BY card;
""")

GET_CATEGORIES_SUMMARY = text("""
    SELECT SUM(t.amount) AS amount, c.name, c.id
    FROM transactions t
    LEFT JOIN categories c ON c.id = t.primary_category_id
    WHERE t.created_at >= (
        CASE
        WHEN EXTRACT(DAY FROM current_date) >= 3
            THEN date_trunc('month', current_date) + interval '2 days'
        ELSE
            date_trunc('month', current_date) - interval '1 month' + interval '2 days'
        END
    )
    AND t.created_at < (
        CASE
        WHEN EXTRACT(DAY FROM current_date) >= 3
            THEN date_trunc('month', current_date) + interval '2 days'
        ELSE
            date_trunc('month', current_date) - interval '1 month' + interval '2 days'
        END
    ) + interval '1 month'
    GROUP BY c.name, c.id;
""")

GET_SUBCATEGORIES_SUMMARY = text("""
    SELECT SUM(t.amount) AS amount, c.name, c.id
    FROM transactions t
    INNER JOIN categories c ON c.id = t.secondary_category_id
    WHERE t.created_at >= (
        CASE
        WHEN EXTRACT(DAY FROM current_date) >= 3
            THEN date_trunc('month', current_date) + interval '2 days'
        ELSE
            date_trunc('month', current_date) - interval '1 month' + interval '2 days'
        END
    )
    AND t.created_at < (
        CASE
        WHEN EXTRACT(DAY FROM current_date) >= 3
            THEN date_trunc('month', current_date) + interval '2 days'
        ELSE
            date_trunc('month', current_date) - interval '1 month' + interval '2 days'
        END
    ) + interval '1 month'
    AND t.primary_category_id = :primary_id
    GROUP BY c.name, c.id;
""")

GET_MONTHLY_TRENDS = text("""
    SELECT
        to_char(
            date_trunc('month', created_at - interval '2 days'),
            'Mon YYYY'
        ) AS month,
        SUM(amount) AS amount
    FROM transactions
    WHERE created_at >= date_trunc('year', current_date)
    AND created_at < date_trunc('year', current_date) + interval '1 year'
    GROUP BY 1
    ORDER BY MIN(date_trunc('month', created_at - interval '2 days'));
""")