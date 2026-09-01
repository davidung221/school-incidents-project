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
