/* 
==============================================================================================
This query shows the number of incidents per month from Jan 2019 - Dec 2023.
==============================================================================================
1. Used a CTE 'all_months'to manually create a time series in order to capture any month with 0 incidents.
2. The CTE is left joined by the main table 'school_incidents'.
3. The resulting table contains year, month, incident_count.

E.g.,
YEAR | MONTH | INCIDENT_COUNT
2019 | JAN   | 9
==============================================================================================
*/

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
    COUNT(si."date_opened") AS incident_count
FROM all_months AS am
LEFT JOIN school_incidents AS si
    ON DATE_TRUNC('month', si."date_opened") = am.month
GROUP BY am.month
ORDER BY am.month;
