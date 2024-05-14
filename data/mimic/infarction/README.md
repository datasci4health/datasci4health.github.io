# SQL sequence to prepare the tables

## ICD codes related to myocardial infarction

~~~sql
select * from d_icd_diagnoses where long_title like '%myocardial infarction%';

create view myocardial_infarction_codes as select * from d_icd_diagnoses where long_title like '%myocardial infarction%';

select * from myocardial_infarction_codes;

select count(*) from diagnoses_icd d, myocardial_infarction_codes m where d.icd_code=m.icd_code;
>> 31.829

select count(*) from diagnoses_icd d where d.icd_code='I219';

create view selected_mi_cases as select * from diagnoses_icd d, myocardial_infarction_codes m where d.icd_code=m.icd_code limit 5;

select * from diagnoses_icd d where d.icd_code='I219';

select * from hcpcsevents where hadm_id = '20242490';

select * from hcpcsevents h, selected_mi_cases s where h.hadm_id = s.hadm_id;
~~~