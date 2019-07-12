  select * from(
  SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_tractstorender]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_tractstorender] 
  where cnt>450
  order by cast(effectsize_tractstorender as float) asc) as x order by effectsize_tractstorender