# school-incidents-project
The aim of this project is to analyse reported incidents in NSW public schools to identify patterns and trends in incident frequency, type, location, time, and distribution across principal networks and operational directorates. The findings are intended to provide insights that can support informed decision-making and help schools identify areas where preventative measures or additional attention may be beneficial.

Data source: https://data.gov.au/data/dataset/nsw-nsw-education-incident-reports-nsw-government-schools

Tools: Python, SQL (PostgreSQL), Power BI

# Dataset Overview
- 17964 records.
- Date range from 16/01/2019 - 22/12-2023.
- 114 total principal network's.
- 11 operational directorate's.
- 7 incident groups.
- 36 primary categories.

# Data Cleaning
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

# Analysis
The following questions are answered:

**1. What are the most common incident groups and categories?**
Assault is the most common, followed by Indecent Assault and Possession of a Weapon.

**2. How has incident volume changed over time?**
There is a trend of increasing incidents over time. Incidents dipped in 2020/2021 because of COVID, but sharply rose afterwards, exceeding pre-COVID (2019) years. 2023 has almost double the number of incidents in 2019.

**3. How does incident volume vary by school term?**
No noticeable pattern. The most recent years (2022, 2023) suggest a pattern of increasing incidents in Term 1 and 4.
Incidents consistently peak during March, May, August, November. Most likely due to assessments and exams.
Incidents consistently dip during January, April, July, September, December. Most likely due to school holidays.

**4. Where do incidents most commonly occur?**
Vast majority of incidents occur at school. However, most incidents outside of school won’t be reported, so the number of incidents outside of school cannot be accurately measured.

**5. How does incident type vary by location/context?**
Assault is the most common incident type, followed by indecent assault. However, during excursions indecent assault is more common.

**6. How does the incident profile differ between operational directorates?**
Rural North and Regional South are the most vulnerable to floods. The three principal network's hit the hardest are Camden, Lennox Coast and Richmond.
Regional North takes the lead in suicidality (attempted suicide, self-harm, suicidal intentions).
Metropolitan South and West have the highest counts of sexual incidents and police operations.

**7. Has the composition of incidents changed over time?**
Assault is consistently the highest category.
Composition remains largely the same, with incident count increasing across most categories.

**8. Top 10 Worst Principal Networks (highest incident count).**
See report for full list. Tuggerah Lakes has highest incident count of all principal network's.

**9. Top 10 Best Principal Networks (lowest incident count).**
See report for full list. Barwon has lowest overall incident count of all principal network's.

**10. The 10 principal network's with the highest incident count each year.**
See sql_query_tables folder.
**11. The 10 principal network's with the lowest consecutive incident counts each year.**
See sql_query_tables folder.
**12. Deeper dive into the three main incident categories (assault, indecent assault, possession of a weapon).**
See sql_query_tables folder.

# Recommendations
- Increase vigilance and take extra measures when planning these activities. Indecent/sexual assault incidents were more common during off-site activities and excursions in the dataset. Schools should consider additional supervision, clear safeguarding procedures, appropriate staff-to-student ratios, and risk assessments when planning these activities.
- Increase access to student wellbeing and mental health support. The number of recorded incidents increased over the years, with a notable rise following the COVID-19 period. Schools should consider investing in accessible counselling and wellbeing services, while strengthening strategies for the early identification and intervention of students experiencing difficulties.
- Provide additional support during periods when incidents are more frequent. Incidents peak in March, May, August and November, which broadly coincide with periods of increased academic assessment and examination activity, including NAPLAN, HSC examinations and school assignments. While this pattern does not establish that academic pressure causes incidents, schools can use these periods to increase wellbeing check-ins, promote awareness of counselling and support services, provide quiet spaces, and offer additional study and academic support.

# Limitations
- Incident counts do not account for differences in school/student population.
- Reported incidents may not represent all incidents that occurred.
- The analysis identifies associations/patterns rather than causes.
- The dataset lists the date and time an incident is reported, not the actual time an incident occurred.
