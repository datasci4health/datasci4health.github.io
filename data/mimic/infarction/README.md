# SQL sequence to prepare the tables

## ICD codes related to myocardial infarction

~~~sql
select * from d_icd_diagnoses where long_title like '%myocardial infarction%';

create view myocardial_infarction_codes as select * from d_icd_diagnoses where long_title like '%myocardial infarction%';

select * from myocardial_infarction_codes;

select count(*) from diagnoses_icd d, myocardial_infarction_codes m where d.icd_code=m.icd_code;
>> 31.829

-- Distribution of Infarction Codes
select s.icd_version, s.icd_code, d.long_title, count(*) from selected_mi_cases s, d_icd_diagnoses d where s.icd_code = d.icd_code group by s.icd_version, s.icd_code, d.long_title;

-- Distribution of Infarction Codes with ST Elevation
select s.icd_version, s.icd_code, d.long_title, count(*) from selected_mi_cases s, d_icd_diagnoses d where d.icd_code >= 'I210' and d.icd_code <= 'I213' and s.icd_code = d.icd_code group by s.icd_version, s.icd_code, d.long_title;

create view selected_mi_cases as select d.* from diagnoses_icd d, myocardial_infarction_codes m where d.icd_code=m.icd_code;

select * from selected_mi_cases limit 5;

select d.text from selected_mi_cases s, notes_discharge d where s.hadm_id=d.hadm_id limit 5;

select s.*,
       d.note_id,
       d.note_type,
       d.note_seq,
       d.charttime,
       d.storetime,
       REPLACE(d.text, '\n', '\\n') as text
from selected_mi_cases s, notes_discharge d where s.hadm_id=d.hadm_id limit 1;

select 'subject_id', 'hadm_id', 'seq_num', 'icd_code', 'icd_version', 'note_id', 'note_type', 'note_seq', 'charttime', 'storetime', 'text'
union all
select s.*,
       d.note_id,
       d.note_type,
       d.note_seq,
       d.charttime,
       d.storetime,
       REPLACE(d.text, '\n', '\\n') as text
from selected_mi_cases s, notes_discharge d where s.hadm_id=d.hadm_id
into outfile 'infarction_notes.csv'
fields optionally enclosed by '"' 
terminated by ',' 
lines terminated by '\n';


DROP TABLE IF EXISTS notes_infarction_subcluster;
CREATE TABLE notes_infarction_subcluster
(
  subject_id INT NOT NULL,
  hadm_id INT NOT NULL,
  seq_num TINYINT NOT NULL,
  icd_code VARCHAR(255) NOT NULL,
  icd_version TINYINT NOT NULL,
  note_id VARCHAR(25) NOT NULL,
  note_type VARCHAR(2) NOT NULL,
  note_seq SMALLINT NOT NULL,
  charttime DATETIME NOT NULL,
  storetime DATETIME,
  text TEXT NOT NULL
)
  CHARACTER SET = UTF8MB4;

icd_code,note_id,text,subject_id,hadm_id,seq_num,icd_version,note_type,note_seq,charttime,storetime

LOAD DATA LOCAL INFILE 'infarction_notes_cluster1_subcluster8.csv' INTO TABLE notes_infarction_subcluster
   FIELDS TERMINATED BY ',' ESCAPED BY '' OPTIONALLY ENCLOSED BY '"'
   LINES TERMINATED BY '\n'
   IGNORE 1 LINES
   (@icd_code,@note_id,@text,@subject_id,@hadm_id,@seq_num,@icd_version,@note_type,@note_seq,@charttime,@storetime)
 SET
   subject_id = trim(@subject_id),
   hadm_id = trim(@hadm_id),
   seq_num = trim(@seq_num),
   icd_code = trim(@icd_code),
   icd_version = trim(@icd_version),
   note_id = trim(@note_id),
   note_type = trim(@note_type),
   note_seq = trim(@note_seq),
   charttime = trim(@charttime),
   storetime = IF(@storetime='', NULL, trim(@storetime)),
   text = trim(@text);

select count(*) from diagnoses_icd d where d.icd_code='I219';
>> 13

select h.* from hcpcsevents h, notes_infarction_subcluster n where h.hadm_id = n.hadm_id limit 20;



select * from diagnoses_icd d where d.icd_code='I219';

select * from hcpcsevents where hadm_id = '20242490';

select * from hcpcsevents h, selected_mi_cases s where h.hadm_id = s.hadm_id;
~~~