# school-incidents-project
The aim of this project is to help inform a parent's decision-making on which schools their children should attend, and to provide recommendations to schools on what to improve.

Data source: https://data.gov.au/data/dataset/nsw-nsw-education-incident-reports-nsw-government-schools

Tools: Python, SQL (PostgreSQL), Power BI

# School Incident Data Cleaning Pipeline (2019-2023)
Goal: Combine 5 years of school incident report files (mix of .xlsx and .csv,
with inconsistent column structures across years) into a single clean
dataframe, ready for SQL/analysis.

Steps:
1. Load every year's files.
2. Standardise each dataframe to match the 2020 file's column structure (chosen as the reference schema since it follows the latest revised schema).
3. Combine everything into one dataframe.
4. Fix two known data quality issues discovered during cleaning:
     - "Connected Communities Team 1/2/3" being treated as 3 separate Operational Directorates instead of 1.
     - Principal Network Names mapping to more than one Operational Directorate, caused by NSW restructuring directorates from 2020 onward. Used the 2023 dataset as the source of truth for the correct network -> directorate mapping.
5. Export the cleaned result to a new CSV.
