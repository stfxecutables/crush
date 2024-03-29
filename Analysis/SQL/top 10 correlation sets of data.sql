select top 20 *  From top_Corr
 where qty>450 
 order by pearsonr desc

select * From correlations where intersection like '%TractsToRender%' and coeff is not null and coeff <1 order by pearsonr desc
select * From tall where roi='4012' and [ROI END]='4017' and method='roi_end'
select * From tall where [ROI Label]=

--select distinct roi,[roi label],[ROI END],[ROI END Label],method into distinct_interesctions from tall
--(1)
select age,stddevfa 
from tall 
where [roi label]='Right-Putamen' 
and [roi end label]='wm-rh-insula' 
and method='roi' 
and stddevfa is not null
--and age=15.0418550862506

--(2)
select age,meanfa 
from tall 
where [roi label]='Brain-Stem' 
and [roi end label]='wm-rh-caudalmiddlefrontal' 
and method='roi' 
and meanfa is not null


--(3)
select age,meanfa 
from tall 
where [roi label]='Left-Putamen' 
and [roi end label]='Brain-Stem' 
and method='roi' 
and meanfa is not null


--(4)
select age,stddevFA 
from tall 
where [roi label]='ctx-lh-superiortemporal' 
and [roi end label]='wm-lh-bankssts' 
and method='roi' 
and stddevFA is not null
 
--(5)
select age,meanFA 
from tall 
where [roi label]='Brain-Stem' 
and [roi end label]='ctx-lh-postcentral' 
and method='roi' 
and meanFA is not null
 
 --(6)
select age,meanFA 
from tall 
where [roi label]='Left-Putamen' 
and [roi end label]='Left-Pallidum' 
and method='roi' 
and meanFA is not null

 --(7)
select age,stddevFA 
from tall 
where [roi label]='wm-lh-bankssts' 
and [roi end label]='wm-lh-superiortemporal' 
and method='roi' 
and stddevFA is not null
	

 --(8)
select age,stddevFA 
from tall 
where [roi label]='ctx-lh-caudalmiddlefrontal' 
and [roi end label]='ctx-lh-parsopercularis' 
and method='roi' 
and stddevFA is not null

--(9)
select age,meanfa 
from tall 
where [roi label]='Brain-Stem' 
and [roi end label]='wm-lh-insula' 
and method='roi' 
and meanfa is not null 