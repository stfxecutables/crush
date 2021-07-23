  select * from(
  SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_meanfa_asymidx]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_meanfa_asymidx] 
  where cnt>450
  order by cast(effectsize_meanfa_asymidx as float) asc) as x order by effectsize_meanfa_asymidx