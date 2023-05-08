## Preparing to Import

~~~sql
show variables like "local_infile";
set global local_infile = true;
show variables like "secure_file_priv";
~~~

## Preparing to Export
~~~
/etc/mysql/my.cnf
~/.my.cnf
~~~

~~~
[mysqld]
secure-file-priv=""
~~~

~~~sql
select * from d_icd_diagnoses where long_title like '%neutropenia%';
~~~

~~~
28800 |  9 | Neutropenia, unspecified
28809 |  9 | Other neutropenia
D70   | 10 | Neutropenia   
D708  | 10 | Other neutropenia
D709  | 10 | Neutropenia, unspecified
~~~

~~~sql
select * from d_labitems where label like '%neutrop%';
~~~

## 

~~~sql
select * from lab_itemid_to_loinc where label like '%neutrop%';
~~~

~~~sql
select d.*, l.valueuom, l.loinc, l.loinc_version from d_labitems d left join lab_itemid_to_loinc l on d.itemid = l.itemid where d.label like '%neutrop%' order by d.itemid;
~~~

~~~
|  51256 | Neutrophils               | Blood | Hematology | %        | 770-8 | 2.71          |
|  52075 | Absolute Neutrophil Count | Blood | Hematology | NULL     |       | 2.71          |
~~~

~~~sql
drop view if exists neutro_adm;
create view neutro_adm as select distinct subject_id, hadm_id from diagnoses_icd where ((icd_code='28800' or icd_code='28809') and icd_version=9) or ((icd_code='D708' or icd_code='D709') and icd_version=10) order by subject_id, hadm_id;
~~~

~~~sql
select count(distinct hadm_id) from neutro_adm;
count: 3013
~~~

~~~sql
select count(distinct subject_id) from neutro_adm;
count: 2133
~~~

~~~sql
drop view if exists neutro_lab;
create view neutro_lab as select distinct subject_id, hadm_id from labevents where itemid = 52075 and value < 0.5 and subject_id is not null and hadm_id is not null order by subject_id, hadm_id;
~~~

~~~sql
select count(distinct hadm_id) from neutro_lab;
count: 1962
~~~

~~~sql
select count(distinct subject_id) from neutro_lab;
count: 1178
~~~

~~~sql
drop view if exists neutro_all;
create view neutro_all as select * from neutro_adm union select * from neutro_lab order by subject_id, hadm_id;
~~~

~~~sql
select count(distinct hadm_id) from neutro_all;
count: 4249
~~~

~~~sql
select count(distinct subject_id) from neutro_all;
count: 2691
~~~

~~~sql
drop table if exists neutro_admissions;

create table neutro_admissions as select n.*, a.admittime, a.dischtime, a.deathtime, a.admission_type, a.marital_status, a.race from neutro_all n, admissions a where n.subject_id = a.subject_id and n.hadm_id = a.hadm_id;

alter table neutro_admissions
  add index neutro_admissions_idx01 (subject_id,hadm_id),
  add index neutro_admissions_idx02 (admittime, dischtime, deathtime),
  add index neutro_admissions_idx03 (admission_type),
  add unique index neutro_admissions_idx04 (hadm_id);
~~~

~~~sql
drop table if exists neutro_diagnoses;

create table neutro_diagnoses as select d.*, i.long_title from diagnoses_icd d, neutro_admissions n, d_icd_diagnoses i where d.subject_id = n.subject_id and d.hadm_id = n.hadm_id and d.icd_code = i.icd_code and d.icd_version = i.icd_version;

alter table neutro_diagnoses 
  add index neutro_diagnoses_idx01 (subject_id, hadm_id),
  add index neutro_diagnoses_idx02 (icd_code, icd_version, seq_num);
~~~

~~~sql
select distinct long_title from neutro_diagnoses where long_title like '%malignant%neoplasm%';
~~~

~~~sql
select count(distinct hadm_id) from neutro_diagnoses where long_title like '%malignant%neoplasm%';
count: 1492
~~~

~~~sql
select count(distinct subject_id) from neutro_diagnoses where long_title like '%malignant%neoplasm%';
count: 1151
~~~

~~~sql
select count(distinct labevent_id, itemid) from labevents l, neutro_diagnoses n where l.subject_id = n.subject_id and l.hadm_id = n.hadm_id;
~~~

~~~sql
drop table if exists neutro_labevents;

create table neutro_labevents as select l.* from labevents l, neutro_admissions n where l.subject_id = n.subject_id and l.hadm_id = n.hadm_id;
~~~

## Replacing null by interrogation (Orange compatibility)

~~~sql
# update neutro_labevents set value = '?' where value is null or value = '___';
# update neutro_labevents set valueuom = '?' where valueuom is null or valueuom = '___';
~~~

~~~sql
alter table neutro_labevents
add valuenum_str varchar(255);

update neutro_labevents
set valuenum_str = cast(valuenum as char);

update neutro_labevents
set valuenum_str = '?' where valuenum_str is null;
~~~

~~~sql
select 'hadm_id', 'specimen_id', 'itemid', 'charttime', 'value', 'valuenum', 'valueuom'
union all
select hadm_id, specimen_id, itemid, charttime, value, valuenum_str, valueuom
from neutro_labevents
into outfile 'neutro_labevents_min.csv'
fields optionally enclosed by '"' 
terminated by ',' 
lines terminated by '\n';
~~~

~~~sql
select 'subject_id', 'hadm_id', 'labevent_id', 'specimen_id', 'itemid', 'charttime', 'value', 'valuenum', 'valueuom', 'ref_range_lower', 'ref_range_upper', 'flag', 'priority', 'comments'
union all
select subject_id, hadm_id, labevent_id, specimen_id, itemid, charttime, value, valuenum_str, valueuom, ref_range_lower, ref_range_upper, flag, priority, comments
from neutro_labevents
into outfile 'neutro_labevents.csv'
fields optionally enclosed by '"' 
terminated by ',' 
lines terminated by '\n';
~~~

cd /etc/mysql
cp my.cnf /import

edit my.cnf
remove secure-file-priv=/var/lib/mysql-files

cd /etc/mysql
cp /import/my.cnf .