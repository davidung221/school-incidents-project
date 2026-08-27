--- top categories by incident type
SELECT
	primary_category,
	count(*) AS incident_count
FROM school_incidents
GROUP BY primary_category
ORDER BY incident_count DESC;
