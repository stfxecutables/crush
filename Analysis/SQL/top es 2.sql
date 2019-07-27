select roistart,roiend,method,effectsize_meanstddevadc,
(select count(1) 
From tall where [ROI Label]=roistart 
and [ROI END Label]=roiend 
and tall.method=effectsize.method 
and stddevADC is not null
) Cnt
--into effectsize_stddevadc
from effectsize 
order by cast(effectsize_meanstddevadc as float) desc


select  *From effectsize

select distinct [ROI Label],[roi end label],method,gender,
(select avg(stddevadc) from tall tm where gender='Male' and stddevadc is not null and tm.[ROI Label]=tall.[ROI Label] and tm.[ROI END Label]=tall.[ROI END Label] and tm.method=tall.method) mean_male,
(select avg(stddevadc) from tall t2 where gender='Female' and stddevadc is not null and t2.[ROI Label]=tall.[ROI Label] and t2.[ROI END Label]=tall.[ROI END Label] and t2.method=tall.method) mean_female,
(select stdev(stddevadc) from tall t2 where  stddevadc is not null  and t2.[ROI Label]=tall.[ROI Label] and t2.[ROI END Label]=tall.[ROI END Label] and t2.method=tall.method) stddev,
(select count(stddevadc) from tall t2 where  stddevadc is not null  and t2.[ROI Label]=tall.[ROI Label] and t2.[ROI END Label]=tall.[ROI END Label] and t2.method=tall.method) count
into effectsize2_stddevadc
From tall where stddevadc is not null
drop table effectsize2_stddevadc


select distinct [roi label],[roi end label],[method],es es,count from (
select *,(mean_male-mean_female)/stddev es From effectsize2_stddevadc where count>450
) as x
order by es desc

select *,(mean_male-mean_female)/stddev From effectsize2_stddevadc where [roi label]='ctx-rh-middletemporal' and [roi end label]='wm-rh-middletemporal' and method='roi_end'

select avg(stddevadc) from (
select distinct [roi label],[roi end label],[method], abs((mean_male-mean_female)/stddev) stddevadc,count 
From effectsize2_stddevadc 
where count>450  
) as x



---Effect size mean stddev FA

select distinct [ROI Label],[roi end label],method,gender,
(select avg(stddevfa) from tall tm where gender='Male' and stddevfa is not null and tm.[ROI Label]=tall.[ROI Label] and tm.[ROI END Label]=tall.[ROI END Label] and tm.method=tall.method) mean_male,
(select avg(stddevfa) from tall t2 where gender='Female' and stddevfa is not null and t2.[ROI Label]=tall.[ROI Label] and t2.[ROI END Label]=tall.[ROI END Label] and t2.method=tall.method) mean_female,
(select stdev(stddevfa) from tall t2 where  stddevfa is not null  and t2.[ROI Label]=tall.[ROI Label] and t2.[ROI END Label]=tall.[ROI END Label] and t2.method=tall.method) stddev,
(select count(stddevfa) from tall t2 where  stddevfa is not null  and t2.[ROI Label]=tall.[ROI Label] and t2.[ROI END Label]=tall.[ROI END Label] and t2.method=tall.method) count
into effectsize2_stddevfa
From tall where stddevfa is not null

--drop table effectsize2_stddevfa

select distinct [roi label],[roi end label],method,es,count from (
select *,(mean_male-mean_female)/stddev es From effectsize2_stddevfa where count>450
) as x order by es desc

 where [roi label]='ctx-rh-middletemporal' and [roi end label]='wm-rh-middletemporal' and method='roi_end'
