  select * from(
  SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_stddevadc_asymidx]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_stddevadc_asymidx] 
  where cnt>450
  order by cast(effectsize_stddevadc_asymidx as float) asc) as x order by effectsize_stddevadc_asymidx