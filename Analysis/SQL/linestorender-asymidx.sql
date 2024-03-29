/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_linestorender_asymidx]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_linestorender_asymidx] order by cast( effectsize_linestorender_asymidx as float) desc
  union
  select * from(
  SELECT TOP 5 [roistart]
      ,[roiend]
      ,[method]
      ,[effectsize_linestorender_asymidx]
      ,[Cnt]
  FROM [MSC].[dbo].[effectsize_linestorender_asymidx] 
  where cnt>450
  order by cast(effectsize_linestorender_asymidx as float) asc) as x order by effectsize_linestorender_asymidx