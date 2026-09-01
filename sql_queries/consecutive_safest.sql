with cte as (
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
    from cte
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
order by years_in_bottom_10 desc limit 10;
