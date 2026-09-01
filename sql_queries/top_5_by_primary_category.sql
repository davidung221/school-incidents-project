-- top 5 by assault
select
	primary_category,
	principal_network_name,
	count(*) as incident_count
from school_incidents
where primary_category = 'Assault'
group by primary_category, principal_network_name
order by incident_count desc
limit 5;

-- top 5 by indecent assault
select
	primary_category,
	principal_network_name,
	count(*) as incident_count
from school_incidents
where primary_category = 'Indecent Assault'
group by primary_category, principal_network_name
order by incident_count desc
limit 5;

-- top 5 by possession of a weapon
select
	primary_category,
	principal_network_name,
	count(*) as incident_count
from school_incidents
where primary_category ILIKE 'possession%'
group by primary_category, principal_network_name
order by incident_count desc
limit 5;
