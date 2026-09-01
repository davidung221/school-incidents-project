/* 
==============================================================================================
This query shows the top 10 principal network names by number of incidents per year.
==============================================================================================
1. First CTE gets the number of incidents for each principal network name per year.
2. Second CTE 'ranked' uses dense_rank() to find the top 10.
3. Final SQL query returns the top 10 for each year.

E.g.,
YEAR | PRINCIPAL_NETWORK_NAME | NUMBER_OF_INCIDENTS | RNK
2019 | GLENFIELD | 94 | 1
==============================================================================================
*/

with cte as (select
    EXTRACT(year from date_opened) as year,
    principal_network_name,
    count(*) as number_of_incidents
    from school_incidents
    group by 1,2),
ranked as (select *,
    dense_rank() over (partition by year order by number_of_incidents desc) as rnk
    from cte)
select * from ranked
where rnk<=10;
