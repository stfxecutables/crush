  select * from(
  SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_meanadc_asymidx]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_meanadc_asymidx] 
  where cnt>450
  order by cast(effectsize_meanadc_asymidx as float) asc) as x order by effectsize_meanadc_asymidx