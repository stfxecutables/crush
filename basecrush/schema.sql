create table if not exists measurements (
    sample int,
    visit varchar(10),
    roi_start int,
    roi_end int,
    method varchar(7),
    measurement varchar(40),
    measured numeric(36,20),
    modified timestamp,
unique(sample,visit,roi_start,roi_end,method,measurement)
);


CREATE FUNCTION modified() RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
BEGIN  
  NEW.modified := current_timestamp;  
  RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_modified
  BEFORE INSERT OR UPDATE ON measurements
  FOR EACH ROW
  EXECUTE PROCEDURE modified();


/*
CREATE or replace FUNCTION f_count_measures(in s int, in v int) 
RETURNS bigint as $$
    select count(1) from measurements where sample=$1 and visit=$2;
    $$ LANGUAGE sql;
*/