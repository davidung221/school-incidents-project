/* 
==============================================================================================
This query shows the principal network names that have consecutively ranked in the bottom 10
for incident count for 4-5 years in a row.
==============================================================================================
1. First CTE 'yearly' lists the number of incidents each principal network name had per year.
2. Second CTE 'ranked' uses a window function to assign a dense rank.
3. Third CTE 'bottom_10' filters by dense rank to the top 10.
4. The final SQL query calculates how many consecutive years a principal network was ranked
in the bottom 10 by number of incidents.

E.g.,
PRINCIPAL_NETWORK_NAME | YEARS_IN_BOTTOM_10
BARWON | 5
==============================================================================================
*/

with yearly as (
    select
        principal_network_name,
        EXTRACT(year from date_opened) as year,
        count(*) as number_of_incidents
    from school_incidents
    group by principal_network_name, year
),
  
ranked as (
    select *,
        dense_rank() over (partition by year order by number_of_incidents) as drn
    from yearly
),
  
bottom_10 as (
    select year, principal_network_name, number_of_incidents, drn as ranking
    from ranked
    where drn <= 10
)
  
select
    principal_network_name,
    count(distinct year) as years_in_bottom_10
from bottom_10
group by principal_network_name
order by years_in_bottom_10 desc 
limit 10;
