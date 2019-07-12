  select * from(
  SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_tractstorender_asymidx]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_tractstorender_asymidx] 
  where cnt>450
  order by cast(effectsize_tractstorender_asymidx as float) asc) as x order by effectsize_tractstorender_asymidx