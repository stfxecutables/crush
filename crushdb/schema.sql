create table if not exists measurements (
    sample int,
    visit int,
    roi_start int,
    roi_end int,
    method varchar(7),
    measurement varchar(20),
    measured numeric(36,20),
unique(sample,visit,roi_start,roi_end,method,measurement)
);
