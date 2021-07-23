  select * from(
  SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_meanfa]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_meanfa] 
  where cnt>450
  order by cast(effectsize_meanfa as float) asc) as x order by effectsize_meanfa