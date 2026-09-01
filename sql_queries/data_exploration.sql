-- random snapshot of 20 rows for initial exploration
SELECT *
FROM school_incidents
ORDER BY RANDOM()
LIMIT 20;

-- checking total records and validating if case numbers are unique
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT case_number) AS unique_case_numbers
FROM school_incidents;

-- getting date range
SELECT
    MIN(date_opened) AS earliest_incident,
    MAX(date_opened) AS latest_incident
FROM school_incidents;

-- incident count by year
SELECT
    EXTRACT(YEAR FROM date_opened) AS year,
    COUNT(*) AS incident_count
FROM school_incidents
GROUP BY year
ORDER BY year;
