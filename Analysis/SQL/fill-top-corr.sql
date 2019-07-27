begin

declare @stmt varchar(512)
declare @stmt2 nvarchar(512)
declare @roi varchar(10)
declare @roiend varchar(10)
declare @method varchar(10)
declare @measure varchar(30)
declare @pearsonr float
declare @p_value float

declare cur_i cursor for
select substring(roi,0,charindex('-',roi,0)) ROI,
 substring(roi,charindex('-',roi,0)+1,   charindex('-',roi,charindex('-',roi,0)+1) - charindex('-',roi,0)-1) ROIEND,
 --charindex('-',roi,charindex('-',roi,0)+1),charindex('-',roi,charindex('-',roi,charindex('-',roi,0)+1)+1),
 substring(roi,charindex('-',roi,charindex('-',roi,0)+1)+1,charindex('-',roi,charindex('-',roi,charindex('-',roi,0)+1)+1)-charindex('-',roi,charindex('-',roi,0)+1)-1) method,
 substring(roi,charindex('-',roi,charindex('-',roi,charindex('-',roi,0)+1)+1)+1,
 len(roi)-charindex('-',roi,charindex('-',roi,charindex('-',roi,0)+1)+1)+1
 ) MEASURE,
 pearsonr,p_value
from (
--select 'sss-ccc-mmm-fff-f2' roi
select top 5000 intersection roi,coeff,pearsonr,p_value from correlations where pearsonr is not null and pearsonr<=0.99999 order by pearsonr desc
--select top 50 intersection roi from correlations -- 'sss-ccc-mmm-fff-f2' roi
) as x

delete from top_corr
open cur_i;

	
fetch next from cur_i into @roi,@roiend,@method,@measure,@pearsonr,@p_value

while @@FETCH_STATUS=0
 BEGIN  
	set @stmt = 'insert into top_corr select '+''''+@roi+'-'+@roiend+'-'+@method+'-'+@measure+''',count(1),'+str(@pearsonr,20,18)+','+str(@p_value,20,18)+' from tall where roi='+''''+right('000'+@roi,4)+''''+' and [roi end]='+''''+right('000'+@roiend,4)+''''+' and method='+''''+@method+''' and ['+@measure+'] is not null'
	set @stmt2= cast(@stmt as nvarchar(512))
	print @stmt2
	execute sp_executesql @stmt2
	fetch next from cur_i into @roi,@roiend,@method,@measure,@pearsonr,@p_value
 END
close cur_i
deallocate cur_i
end


--select top 50000 intersection roi from correlations where pearsonr is not null order by pearsonr desc-- 'sss-ccc-mmm-fff-f2' roi

--select right('000'+'7',4)

--alter table top_corr add pearsonr numeric(20,17)
--alter table top_corr add p_value numeric(20,17)

select * From top_corr where qty>20 order by pearsonr desc

--select top 5000 intersection roi,coeff,pearsonr,p_value from correlations where pearsonr is not null and pearsonr<0.99999 order by pearsonr desc
