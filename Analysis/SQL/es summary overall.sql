select 'effectsize_linestorender', es,count(1) from (select case
	when  floor(abs(effectsize_linestorender)*100)>=80 then 'Large'
	when  floor(abs(effectsize_linestorender)*100)>=50 then 'Medium'
	when  floor(abs(effectsize_linestorender)*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize_linestorender] 
 where cnt>513 ) as x
 group by es
 ----------  linestorender_asymidx
select '[effectsize_linestorender_asymidx]', es,count(1) from (select case
	when  floor(abs([effectsize_linestorender_asymidx])*100)>=80 then 'Large'
	when  floor(abs([effectsize_linestorender_asymidx])*100)>=50 then 'Medium'
	when  floor(abs([effectsize_linestorender_asymidx])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize_linestorender_asymidx] 
 where cnt>513 ) as x
 group by es
 -------- mean adc
 select '[effectsize_meanadc]',es,count(1) from (select case
	when  floor(abs([effectsize_meanadc])*100)>=80 then 'Large'
	when  floor(abs([effectsize_meanadc])*100)>=50 then 'Medium'
	when  floor(abs([effectsize_meanadc])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize_meanadc] 
 where cnt>513 ) as x
 group by es
 ------ mean adc asymidx
  select '[effectsize_meanadc_asymidx]', es,count(1) from (select case
	when  floor(abs([effectsize_meanadc_asymidx])*100)>=80 then 'Large'
	when  floor(abs([effectsize_meanadc_asymidx])*100)>=50 then 'Medium'
	when  floor(abs([effectsize_meanadc_asymidx])*100)>=20 then 'Small'	
	else 'None'
	end es
 from [dbo].[effectsize_meanadc_asymidx] 
 where cnt>513 ) as x
 group by es
 ------ mean fa
  select '[effectsize_meanfa]',es,count(1) from (select case
	when  floor(abs([effectsize_meanfa])*100)>=80 then 'Large'
	when  floor(abs([effectsize_meanfa])*100)>=50 then 'Medium'
	when  floor(abs([effectsize_meanfa])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize_meanfa] 
 where cnt>513 ) as x
 group by es
------ mean fa asymidx
 -- select '[effectsize_meanfa_asymidx]',es,count(1) from (select case
	--when  floor(abs([effectsize_meanfa_asymidx])*100)>=80 then 'Large'
	--when  floor(abs([effectsize_meanfa_asymidx])*100)>=50 then 'Medium'
	--when  floor(abs([effectsize_meanfa_asymidx])*100)>=20 then 'Small'
	--else 'None'
	--end es
 --from [dbo].[effectsize_meanfa_asymidx]
 --where cnt>513 ) as x
 --group by es
   ------ [dbo].[[effectsize_stddevadc_asymidx]]
  select '[effectsize2_stddevfa_asymidx]',es,count(1) from (select case
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=80 then 'Large'
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=50 then 'Medium'
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize2_stddevfa_asymidx]
 where count>513 ) as x
 group by es    
------ number of tracts
  select '[effectsize_numtracts]',es,count(1) from (select case
	when  floor(abs([effectsize_numtracts])*100)>=80 then 'Large'
	when  floor(abs([effectsize_numtracts])*100)>=50 then 'Medium'
	when  floor(abs([effectsize_numtracts])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize_numtracts]
 where cnt>513 ) as x
 group by es
------ number of tracts ASYMMETRY
  select '[[effectsize_numtracts_asymidx]]',es,count(1) from (select case
	when  floor(abs([effectsize_numtracts_asymidx])*100)>=80 then 'Large'
	when  floor(abs([effectsize_numtracts_asymidx])*100)>=50 then 'Medium'
	when  floor(abs([effectsize_numtracts_asymidx])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize_numtracts_asymidx]
 where cnt>513 ) as x
 group by es    
 ------ [dbo].[effectsize_stddevadc]
  select 'effectsize_stddevadc',es,count(1) from (select case
	when  floor(abs([effectsize_meanstddevadc])*100)>=80 then 'Large'
	when  floor(abs([effectsize_meanstddevadc])*100)>=50 then 'Medium'
	when  floor(abs([effectsize_meanstddevadc])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize_stddevadc]
 where cnt>513 ) as x
 group by es    

 -- ------ [dbo].[[effectsize_stddevadc_asymidx]]
 -- select '[effectsize_stddevadc_asymidx]',es,count(1) from (select case
	--when  floor(abs([effectsize_stddevadc_asymidx])*100)>=80 then 'Large'
	--when  floor(abs([effectsize_stddevadc_asymidx])*100)>=50 then 'Medium'
	--when  floor(abs([effectsize_stddevadc_asymidx])*100)>=20 then 'Small'
	--else 'None'
	--end es
 --from [dbo].[effectsize_stddevadc_asymidx]
 --where cnt>513 ) as x
 --group by es    
   ------ [dbo].[[effectsize_stddevadc_asymidx]]
  select '[effectsize2_stddevadc]',es,count(1) from (select case
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=80 then 'Large'
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=50 then 'Medium'
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize2_stddevadc]
 where count>513 ) as x
 group by es    

   ------ [dbo].[[effectsize_stddevadc_asymidx]]
  select '[effectsize2_stddevfa]',es,count(1) from (select case
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=80 then 'Large'
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=50 then 'Medium'
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize2_stddevfa]
 where count>513 ) as x
 group by es    


 --  ------effectsize_stddevfa-asymidx
 -- select '[[effectsize_stddevfa-asymidx]]',es,count(1) from (select case
	--when  floor(abs([effectsize_meanstddevfa_asymidx])*100)>=80 then 'Large'
	--when  floor(abs([effectsize_meanstddevfa_asymidx])*100)>=50 then 'Medium'
	--when  floor(abs([effectsize_meanstddevfa_asymidx])*100)>=20 then 'Small'
	--else 'None'
	--end es
 --from [dbo].[effectsize_stddevfa_asymidx]
 --where cnt>513 ) as x
 --group by es    
    ------[effectsize_tractstorender]
  select '[effectsize_tractstorender]',es,count(1) from (select case
	when  floor(abs([effectsize_tractstorender])*100)>=80 then 'Large'
	when  floor(abs([effectsize_tractstorender])*100)>=50 then 'Medium'
	when  floor(abs([effectsize_tractstorender])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize_tractstorender]
 where cnt>513 ) as x
 group by es    
     ------[[effectsize_tractstorender_asymidx]]
  select '[effectsize_tractstorender_asymidx]',es,count(1) from (select case
	when  floor(abs([effectsize_tractstorender_asymidx])*100)>=80 then 'Large'
	when  floor(abs([effectsize_tractstorender_asymidx])*100)>=50 then 'Medium'
	when  floor(abs([effectsize_tractstorender_asymidx])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize_tractstorender_asymidx]
 where cnt>513 ) as x
 group by es  

 
  ------ [dbo].[[effectsize_stddevadc_asymidx]]
  select '[effectsize2_stddevadc]',es,count(1) from (select case
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=80 then 'Large'
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=50 then 'Medium'
	when  floor(abs(([mean_male]-[mean_female])/[stddev])*100)>=20 then 'Small'
	else 'None'
	end es
 from [dbo].[effectsize2_stddevadc]
 where count>513 ) as x
 group by es    