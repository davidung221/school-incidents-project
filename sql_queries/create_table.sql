-- renamed all columns for easier sql handling, importing data from 'school_project_cleaned.csv'
COPY school_incidents (
    case_number,
    date_opened,
    term,
    incident_group,
    operational_directorate,
    principal_network_name,
    primary_category,
    primary_sub_category,
    secondary_category,
    incident_summary,
    incident_priority_rating,
    incident_occurred
)
FROM 'C:\Users\David Ung\Desktop\data_projects\school_project'
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    QUOTE '"'
);
