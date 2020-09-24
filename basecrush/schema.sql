create table if not exists measurements (
    sample int,
    visit varchar(10),
    roi_start int,
    roi_end int,
    method varchar(7),
    measurement varchar(20),
    measured numeric(36,20),
unique(sample,visit,roi_start,roi_end,method,measurement)
);
/*
CREATE or replace FUNCTION f_count_measures(in s int, in v int) 
RETURNS bigint as $$
    select count(1) from measurements where sample=$1 and visit=$2;
    $$ LANGUAGE sql;
*/