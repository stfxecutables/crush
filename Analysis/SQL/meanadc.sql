  select * from(
  SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_meanadc]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_meanadc] 
  where cnt>450
  order by cast(effectsize_meanadc as float) asc) as x order by effectsize_meanadc