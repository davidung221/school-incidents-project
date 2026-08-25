WITH all_months AS (
    SELECT generate_series(
        DATE '2019-01-01',
        DATE '2023-12-01',
        INTERVAL '1 month'
    ) AS month
)
SELECT
    EXTRACT(YEAR FROM am.month)::int AS year,
    TO_CHAR(am.month, 'Mon') AS month,
    COUNT(si."date_opened") AS number_of_incidents
FROM all_months AS am
LEFT JOIN school_incidents AS si
    ON DATE_TRUNC('month', si."date_opened") = am.month
GROUP BY am.month
ORDER BY am.month;
