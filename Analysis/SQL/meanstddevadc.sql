  select * from(
  SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_meanstddevadc]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_stddevadc] 
  where cnt>450
  order by cast(effectsize_meanstddevadc as float) asc) as x order by effectsize_meanstddevadc