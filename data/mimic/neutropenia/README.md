# Summary of Tables

* `neutro_admissions.csv` - joins admission records of two neutropenia-related contexts:
  * admissions of patients diagnosed with neutropenia
  * admissions of patients whose lab exam indicates neutropenia
* `neutro_diagnoses.csv` - diagnostics of the selected admissions
* `neutro_labevents` all lab exams of the selected admissions, exported in two versions due to its size:
  * `neutro_labevents_min.csv` - set of minimal fields for the proposed analysis
  * `neutro_labevents.csv` - includes a broader set of fields that could be useful in the analysis
* `neutro_itemid_loinc.csv` - codes of items and respective LOINC with descriptions for the selected exams

These files are organized in two ZIPs:
* `neutropenia_min.zip` - all tables with neutro_labevents_min for neutro_labevents
* `neutropenia_full.zip` - all tables with neutro_labevents for neutro_labevents

# SQL sequence to prepare the tables

## Filtering admissions of patients diagnosed with Neutropenia (`neutro_adm`)

### ICD codes related to neutropenia

~~~sql
select * from d_icd_diagnoses where long_title like '%neutropenia%';
~~~

~~~
+----------+-------------+--------------------------------+
| icd_code | icd_version | long_title                     |
+----------+-------------+--------------------------------+
| 28800    |           9 | Neutropenia, unspecified       |
| 28801    |           9 | Congenital neutropenia         |
| 28802    |           9 | Cyclic neutropenia             |
| 28803    |           9 | Drug induced neutropenia       |
| 28804    |           9 | Neutropenia due to infection   |
| 28809    |           9 | Other neutropenia              |
| 7767     |           9 | Transient neonatal neutropenia |
| D70      |          10 | Neutropenia                    |
| D703     |          10 | Neutropenia due to infection   |
| D704     |          10 | Cyclic neutropenia             |
| D708     |          10 | Other neutropenia              |
| D709     |          10 | Neutropenia, unspecified       |
| P615     |          10 | Transient neonatal neutropenia |
+----------+-------------+--------------------------------+
~~~

Selecting those neutropenias that do not have a predefined documented cause:

~~~
+----------+-------------+--------------------------------+
| icd_code | icd_version | long_title                     |
+----------+-------------+--------------------------------+
| 28800    |           9 | Neutropenia, unspecified       |
| 28809    |           9 | Other neutropenia              |
| D70      |          10 | Neutropenia                    |
| D708     |          10 | Other neutropenia              |
| D709     |          10 | Neutropenia, unspecified       |
+----------+-------------+--------------------------------+
~~~

There are no diagnoses with the generic code D70:
~~~sql
select count(*) from diagnoses_icd where icd_code='D70';
count: 0
~~~

So the selection filters the other four (version 9: `28800` and `28809`; version 10: `D708` and `D709`):

~~~sql
drop view if exists neutro_adm;

create view neutro_adm as
select distinct subject_id, hadm_id
from diagnoses_icd
where ((icd_code='28800' or icd_code='28809') and icd_version=9) or ((icd_code='D708' or icd_code='D709') and icd_version=10) order by subject_id, hadm_id;
~~~

Number of admissions in this table:

~~~sql
select count(distinct hadm_id) from neutro_adm;
count: 3,013
~~~

Number of subjects in this table:

~~~sql
select count(distinct subject_id) from neutro_adm;
count: 2,133
~~~

## Filtering admissions of patients whose lab exam indicates Neutropenia (`neutro_lab`)

### All lab exams that have neutrophils-like words in the description

#### Table `lab_itemid_to_loinc`

The table d_labitems_to_loinc comes from the CSV published here: https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iv/concepts/concept_map/d_labitems_to_loinc.csv

Join between d_labitems and  d_labitems_to_loinc to find neutrophils-like exams in both:

~~~sql
select d.*, l.valueuom, l.loinc, l.loinc_version from d_labitems d left join lab_itemid_to_loinc l on d.itemid = l.itemid where d.label like '%neutrop%' order by d.itemid;
~~~

~~~
+--------+--------------------------------------+---------------------+------------+----------+-------+---------------+
| itemid | label                                | fluid               | category   | valueuom | loinc | loinc_version |
+--------+--------------------------------------+---------------------+------------+----------+-------+---------------+
|  50872 | Anti-Neutrophil Cytoplasmic Antibody | Blood               | Chemistry  | N/A      |       | 2.71          |
|  51232 | Hypersegmented Neutrophils           | Blood               | Hematology | %        |       | 2.71          |
|  51256 | Neutrophils                          | Blood               | Hematology | %        | 770-8 | 2.71          |
|  52075 | Absolute Neutrophil Count            | Blood               | Hematology | NULL     |       | 2.71          |
|  52260 | Hypersegmented Neutrophils           | Cerebrospinal Fluid | Hematology | NULL     |       | 2.71          |
|  52261 | Hypersegmented Neutrophils #         | Cerebrospinal Fluid | Hematology | %        |       | 2.71          |
|  52299 | Hypersegmented Neutrophils           | Joint Fluid         | Hematology | NULL     |       | 2.71          |
|  52300 | Hypersegmented Neutrophils #         | Joint Fluid         | Hematology | %        |       | 2.71          |
|  52355 | Hypersegmented Neutrophils           | Other Body Fluid    | Hematology | NULL     |       | 2.71          |
|  52356 | Hypersegmented Neutrophils#          | Other Body Fluid    | Hematology | NULL     |       | 2.71          |
|  52382 | Hypersegmented  Neutrophils#         | Pleural             | Hematology | NULL     |       | 2.71          |
|  52383 | Hypersegmented Neutrophils           | Pleural             | Hematology | NULL     |       | 2.71          |
|  53133 | Absolute Neutrophil                  | Blood               | Chemistry  | NULL     | NULL  | NULL          |
+--------+--------------------------------------+---------------------+------------+----------+-------+---------------+
~~~

Among the three neutrophil count exams:

~~~
+--------+---------------------------+-------+------------+----------+-------+---------------+
| itemid | label                     | fluid | category   | valueuom | loinc | loinc_version |
+--------+---------------------------+-------+------------+----------+-------+---------------+
|  51256 | Neutrophils               | Blood | Hematology | %        | 770-8 | 2.71          |
|  52075 | Absolute Neutrophil Count | Blood | Hematology | NULL     |       | 2.71          |
|  53133 | Absolute Neutrophil       | Blood | Chemistry  | NULL     | NULL  | NULL          |
+--------+---------------------------+-------+------------+----------+-------+---------------+
~~~

We considered the `52075 - Absolute Neutrophil Count`. The `51256 - Neutrophils` exam presents results in percent (we are looking for the absolute count) and the `53133 - Absolute Neutrophil` does not have a LOINC counterpart and does not appear in the lab events table.

The exam type 52075 (Absolute Neutrophil Count) does not define a UOM (unit of measure). But all lab events specify the K/uL UOM -- i.e., 1,000 cells per microliter:

~~~sql
select valueuom, count(*) from labevents where itemid=52075 and valuenum is not null group by valueuom;
~~~

~~~
+----------+----------+
| valueuom | count(*) |
+----------+----------+
| K/uL     |   538690 |
+----------+----------+
~~~

Selecting admissions that have at least one neutrophil count exam (52075) with a value of fewer than 500 cells (0.5K cells) per microliter:

~~~sql
drop view if exists neutro_lab;

create view neutro_lab as
select distinct subject_id, hadm_id from labevents where itemid = 52075 and value < 0.5 and subject_id is not null and hadm_id is not null
order by subject_id, hadm_id;
~~~

Number of admissions in this table:

~~~sql
select count(distinct hadm_id) from neutro_lab;
count: 1,962
~~~

Number of subjects in this table:

~~~sql
select count(distinct subject_id) from neutro_lab;
count: 1,178
~~~

## Joining all neutropenia-related admissions (`neutro_admissions`)

This table joins the two previous tables:
* `neutro_adm` - contains all admissions of patients diagnosed with Neutropenia.
* `neutro_lab` - contains all admissions of patients whose lab exam indicates Neutropenia.

Combining the records of both tables in an intermediary table:

~~~sql
drop view if exists neutro_all;
create view neutro_all as select * from neutro_adm union select * from neutro_lab order by subject_id, hadm_id;
~~~

Number of admissions in this table:

~~~sql
select count(distinct hadm_id) from neutro_all;
count: 4,249
~~~

Number of subjects in this table:

~~~sql
select count(distinct subject_id) from neutro_all;
count: 2,691
~~~

Joining the subject and admission codes with the remaining admission data:

~~~sql
drop table if exists neutro_admissions;

create table neutro_admissions as
select n.*, a.admittime, a.dischtime, a.deathtime, a.admission_type, a.marital_status, a.race
from neutro_all n, admissions a
where n.subject_id = a.subject_id and n.hadm_id = a.hadm_id;

alter table neutro_admissions
  add index neutro_admissions_idx01 (subject_id,hadm_id),
  add index neutro_admissions_idx02 (admittime, dischtime, deathtime),
  add index neutro_admissions_idx03 (admission_type),
  add unique index neutro_admissions_idx04 (hadm_id);
~~~

Creating a string field (`deathtime_str`) counterpart for the `deathtime` field (as date fields do not accept characters like ?):

~~~sql
alter table neutro_admissions
add deathtime_str varchar(255);

update neutro_admissions
set deathtime_str = cast(deathtime as char);
~~~

Converting null fields in ?, as the Orange workflow uses ? to indicate missing values:

~~~sql
update neutro_admissions
set deathtime_str = '?' where deathtime_str is null;
~~~

Exporting the table to CSV:

~~~sql
select 'subject_id', 'hadm_id', 'admittime', 'dischtime', 'deathtime', 'admission_type', 'marital_status', 'race'
union all
select subject_id, hadm_id, admittime, dischtime, deathtime_str, admission_type, marital_status, race
from neutro_admissions
into outfile 'neutro_admissions.csv'
fields optionally enclosed by '"' 
terminated by ',' 
lines terminated by '\n';
~~~

## Diagnoses of the selected admissions (`neutro_diagnoses`)

Retrieving all diagnoses of the selected admissions besides those indicating Neutropenia:

~~~sql
drop table if exists neutro_diagnoses;

create table neutro_diagnoses as
select d.*, i.long_title
from diagnoses_icd d, neutro_admissions n, d_icd_diagnoses i
where d.subject_id = n.subject_id and d.hadm_id = n.hadm_id and d.icd_code = i.icd_code and d.icd_version = i.icd_version;

alter table neutro_diagnoses 
  add index neutro_diagnoses_idx01 (subject_id, hadm_id),
  add index neutro_diagnoses_idx02 (icd_code, icd_version, seq_num);
~~~

Exporting the table to CSV:

~~~sql
select 'subject_id', 'hadm_id', 'seq_num', 'icd_code', 'icd_version', 'long_title'
union all
select subject_id, hadm_id, seq_num, icd_code, icd_version, long_title
from neutro_diagnoses
into outfile 'neutro_diagnoses.csv'
fields optionally enclosed by '"' 
terminated by ',' 
lines terminated by '\n';
~~~

Types of cancer (`malignant neoplasm`):

~~~sql
select distinct long_title from neutro_diagnoses where long_title like '%malignant%neoplasm%';
~~~

~~~
+------------------------------------------------------------------------------------------------------------+
| long_title                                                                                                 |
+------------------------------------------------------------------------------------------------------------+
| Malignant neoplasm of head of pancreas                                                                     |
| Personal history of malignant neoplasm of breast                                                           |
| Secondary malignant neoplasm of bone                                                                       |
| Secondary malignant neoplasm of unspecified adrenal gland                                                  |
| Family history of malignant neoplasm of gastrointestinal tract                                             |
| Personal history of other malignant neoplasm of skin                                                       |
| Secondary malignant neoplasm of brain and spinal cord                                                      |
| Secondary malignant neoplasm of lung                                                                       |
| Secondary and unspecified malignant neoplasm of intrathoracic lymph nodes                                  |
| Personal history of malignant neoplasm of bladder                                                          |
| Malignant neoplasm of descending colon                                                                     |
| Malignant neoplasm of liver, secondary                                                                     |
| Secondary and unspecified malignant neoplasm of intra-abdominal lymph nodes                                |
| Family history of malignant neoplasm of prostate                                                           |
| Family history of malignant neoplasm of breast                                                             |
| Malignant neoplasm of pancreas, part unspecified                                                           |
| Other malignant neoplasm without specification of site                                                     |
| Personal history of malignant neoplasm of other sites                                                      |
| Malignant neoplasm of body of pancreas                                                                     |
| Secondary malignant neoplasm of retroperitoneum and peritoneum                                             |
| Family history of malignant neoplasm of other organs or systems                                            |
| Secondary malignant neoplasm of other specified sites                                                      |
| Malignant neoplasm of right ovary                                                                          |
| Personal history of malignant neoplasm of thyroid                                                          |
| Malignant neoplasm of other and unspecified sites of male breast                                           |
| Secondary malignant neoplasm of skin                                                                       |
| Family history of malignant neoplasm of trachea, bronchus and lung                                         |
| Family history of malignant neoplasm of digestive organs                                                   |
| Malignant neoplasm of unspecified site of right female breast                                              |
| Secondary malignant neoplasm of liver and intrahepatic bile duct                                           |
| Secondary malignant neoplasm of pleura                                                                     |
| Personal history of malignant neoplasm of other organs and systems                                         |
| Personal history of other malignant neoplasm of bronchus and lung                                          |
| Secondary malignant neoplasm of other digestive organs                                                     |
| Malignant neoplasm of unspecified part of unspecified bronchus or lung                                     |
| Personal history of malignant neoplasm of other parts of uterus                                            |
| Secondary malignant neoplasm of unspecified site                                                           |
| Malignant (primary) neoplasm, unspecified                                                                  |
| Family history of malignant neoplasm, unspecified                                                          |
| Personal history of malignant neoplasm of liver                                                            |
| Malignant neoplasm of rectum                                                                               |
| Personal history of malignant neoplasm of bronchus and lung                                                |
| Secondary malignant neoplasm of unspecified part of nervous system                                         |
| Secondary malignant neoplasm of left lung                                                                  |
| Secondary malignant neoplasm of right lung                                                                 |
| Malignant neoplasm of cervix uteri, unspecified                                                            |
| Malignant neoplasm of liver, primary                                                                       |
| Family history of malignant neoplasm of trachea, bronchus, and lung                                        |
| Personal history of malignant neoplasm of ovary                                                            |
| Malignant neoplasm of bronchus and lung, unspecified                                                       |
| Secondary malignant neoplasm of bone and bone marrow                                                       |
| Malignant neoplasm of upper-outer quadrant of right female breast                                          |
| Malignant neoplasm of prostate                                                                             |
| Malignant neoplasm of lower lobe, bronchus or lung                                                         |
| Secondary and unspecified malignant neoplasm of inguinal and lower limb lymph nodes                        |
| Personal history of other malignant neoplasm of rectum, rectosigmoid junction, and anus                    |
| Personal history of malignant neoplasm of testis                                                           |
| Malignant neoplasm of other specified sites of female breast                                               |
| Personal history of malignant neoplasm of kidney                                                           |
| Malignant neoplasm of unspecified site of left female breast                                               |
| Malignant neoplasm of other specified sites of pancreas                                                    |
| Personal history of malignant neoplasm of large intestine                                                  |
| Malignant neoplasm of rectosigmoid junction                                                                |
| Malignant neoplasm of anus, unspecified                                                                    |
| Family history of other malignant neoplasms of lymphoid, hematopoietic and related tissues                 |
| Malignant neoplasm of tonsil                                                                               |
| Malignant neoplasm of overlapping sites of cervix uteri                                                    |
| Family history of malignant neoplasm of other genital organs                                               |
| Malignant neoplasm of ovary                                                                                |
| Malignant neoplasm of nipple and areola, right female breast                                               |
| Personal history of malignant neoplasm of prostate                                                         |
| Personal history of other malignant neoplasm of large intestine                                            |
| Malignant neoplasm of thyroid gland                                                                        |
| Family history of unspecified malignant neoplasm                                                           |
| Malignant neoplasm of right main bronchus                                                                  |
| Secondary and unspecified malignant neoplasm of lymph nodes of head, face, and neck                        |
| Malignant neoplasm of hypopharynx, unspecified site                                                        |
| Personal history of malignant neoplasm of cervix uteri                                                     |
| Malignant neoplasm of upper lobe, bronchus or lung                                                         |
| Secondary malignant neoplasm of brain                                                                      |
| Malignant neoplasm of placenta                                                                             |
| Malignant neoplasm of left testis, unspecified whether descended or undescended                            |
| Secondary malignant neoplasm of cerebral meninges                                                          |
| Secondary malignant neoplasm of unspecified lung                                                           |
| Malignant neoplasm of cecum                                                                                |
| Malignant neoplasm of female genital organ, site unspecified                                               |
| Secondary malignant neoplasm of other digestive organs and spleen                                          |
| Malignant neoplasm of unspecified part of right bronchus or lung                                           |
| Malignant neoplasm of thymus                                                                               |
| Malignant neoplasm of unspecified site of unspecified female breast                                        |
| Personal history of other malignant neoplasm of kidney                                                     |
| Malignant neoplasm of other specified part of esophagus                                                    |
| Malignant neoplasm of esophagus, unspecified site                                                          |
| Secondary malignant neoplasm of other parts of nervous system                                              |
| Secondary malignant neoplasm of large intestine and rectum                                                 |
| Malignant neoplasm of upper third of esophagus                                                             |
| Personal history of malignant neoplasm of other sites of lip, oral cavity, and pharynx                     |
| Personal history of malignant neoplasm of unspecified site of lip, oral cavity, and pharynx                |
| Personal history of malignant neoplasm of bone                                                             |
| Malignant neoplasm of cardia                                                                               |
| Personal history of malignant neoplasm of other gastrointestinal tract                                     |
| Personal history of other malignant neoplasms of lymphoid, hematopoietic and related tissues               |
| Secondary and unspecified malignant neoplasm of lymph nodes of multiple sites                              |
| Malignant neoplasm of tail of pancreas                                                                     |
| Family history of malignant neoplasm of other respiratory and intrathoracic organs                         |
| Malignant neoplasm of ascending colon                                                                      |
| Malignant neoplasm of appendix                                                                             |
| Malignant neoplasm of upper lobe, left bronchus or lung                                                    |
| Malignant neoplasm of extrahepatic bile duct                                                               |
| Personal history of malignant neoplasm of other and unspecified oral cavity and pharynx                    |
| Secondary and unspecified malignant neoplasm of axilla and upper limb lymph nodes                          |
| Malignant neoplasm of central portion of female breast                                                     |
| Malignant neoplasm of trachea                                                                              |
| Secondary malignant neoplasm of bladder                                                                    |
| Malignant neoplasm of duodenum                                                                             |
| Malignant neoplasm of pancreas, unspecified                                                                |
| Malignant neoplasm of parietal lobe                                                                        |
| Malignant neoplasm of upper lobe, right bronchus or lung                                                   |
| Encounter for follow-up examination after completed treatment for conditions other than malignant neoplasm |
| Family history of malignant neoplasm of bladder                                                            |
| Malignant neoplasm of overlapping sites of left female breast                                              |
| Malignant neoplasm of stomach, unspecified site                                                            |
| Malignant neoplasm of bone and articular cartilage, unspecified                                            |
| Malignant neoplasm of fundus uteri                                                                         |
| Secondary malignant neoplasm of bone marrow                                                                |
| Rising PSA following treatment for malignant neoplasm of prostate                                          |
| Malignant neoplasm of descended right testis                                                               |
| Secondary and unspecified malignant neoplasm of intrapelvic lymph nodes                                    |
| Malignant neoplasm of colon, unspecified site                                                              |
| Secondary and unspecified malignant neoplasm of lymph nodes of axilla and upper limb                       |
| Malignant neoplasm of tonsil, unspecified                                                                  |
| Personal history of malignant neoplasm of ureter                                                           |
| Malignant neoplasm of main bronchus                                                                        |
| Malignant neoplasm of cerebrum, except lobes and ventricles                                                |
| Malignant neoplasm of pineal gland                                                                         |
| Malignant neoplasm of cerebral ventricle                                                                   |
| Malignant neoplasm of connective and soft tissue of trunk, unspecified                                     |
| Personal history of malignant neoplasm of rectum, rectosigmoid junction, and anus                          |
| Secondary malignant neoplasm of small intestine including duodenum                                         |
| Secondary malignant neoplasm of other urinary organs                                                       |
| Malignant neoplasm of other parts of bronchus or lung                                                      |
| Secondary malignant neoplasm of genital organs                                                             |
| Malignant neoplasm of upper-outer quadrant of female breast                                                |
| Malignant neoplasm of anterior mediastinum                                                                 |
| Malignant neoplasm of brain, unspecified                                                                   |
| Malignant neoplasm of larynx, unspecified                                                                  |
| Personal history of malignant neoplasm of pancreas                                                         |
| Malignant neoplasm associated with transplanted organ                                                      |
| Secondary and unspecified malignant neoplasm of lymph nodes of head, face and neck                         |
| Secondary and unspecified malignant neoplasm of lymph nodes, site unspecified                              |
| Secondary malignant neoplasm of adrenal gland                                                              |
| Malignant neoplasm of overlapping sites of rectum, anus and anal canal                                     |
| Malignant neoplasm of overlapping sites of bladder                                                         |
| Malignant neoplasm of lateral wall of bladder                                                              |
| Malignant neoplasm of corpus uteri, except isthmus                                                         |
| Personal history of malignant neoplasm of soft tissue                                                      |
| Malignant neoplasm of other specified sites of cervix                                                      |
| Personal history of malignant neoplasm of tongue                                                           |
| Family history of other specified malignant neoplasm                                                       |
| Malignant neoplasm of connective and other soft tissue of pelvis                                           |
| Malignant neoplasm of glottis                                                                              |
| Malignant neoplasm of subglottis                                                                           |
| Malignant neoplasm of peripheral nerves and autonomic nervous system, unspecified                          |
| Malignant neoplasm of sigmoid colon                                                                        |
| Personal history of other malignant neoplasm of stomach                                                    |
| Malignant neoplasm of breast (female), unspecified                                                         |
| Secondary and unspecified malignant neoplasm of lymph nodes of multiple regions                            |
| Family history of malignant neoplasm of testis                                                             |
| Family history of malignant neoplasm of kidney                                                             |
| Malignant neoplasm of greater curvature of stomach, unspecified                                            |
| Malignant neoplasm of overlapping sites of pancreas                                                        |
| Personal history of malignant neoplasm of other endocrine glands and related structures                    |
| Malignant neoplasm of oropharynx, unspecified site                                                         |
| Malignant neoplasm of intrahepatic bile ducts                                                              |
| Malignant neoplasm of endometrium                                                                          |
| Secondary malignant neoplasm of small intestine                                                            |
| Secondary malignant neoplasm of left ovary                                                                 |
| Secondary malignant neoplasm of right ovary                                                                |
| Malignant neoplasm of anus, unspecified site                                                               |
| Malignant neoplasm of unspecified site of right male breast                                                |
| Malignant neoplasm of nasopharynx, unspecified site                                                        |
| Malignant neoplasm of overlapping sites of hypopharynx                                                     |
| Secondary malignant neoplasm of other respiratory organs                                                   |
| Personal history of malignant neoplasm of larynx                                                           |
| Secondary and unspecified malignant neoplasm of lymph node, unspecified                                    |
| Malignant neoplasm of colon, unspecified                                                                   |
| Malignant neoplasm of left ovary                                                                           |
| Malignant neoplasm of pylorus                                                                              |
| Malignant neoplasm of pharynx, unspecified                                                                 |
| Malignant neoplasm of upper-outer quadrant of left female breast                                           |
| Malignant neoplasm of esophagus, unspecified                                                               |
| Malignant neoplasm of renal pelvis                                                                         |
| Malignant neoplasm of overlapping sites of right female breast                                             |
| Malignant neoplasm of right lower limb                                                                     |
| Malignant neoplasm of bladder, unspecified                                                                 |
| Secondary malignant neoplasm of kidney                                                                     |
| Malignant neoplasm of middle third of esophagus                                                            |
| Malignant neoplasm associated with transplant organ                                                        |
| Malignant neoplasm of pyloric antrum                                                                       |
| Malignant neoplasm of right kidney, except renal pelvis                                                    |
| Malignant neoplasm of lower-outer quadrant of left female breast                                           |
| Malignant neoplasm of upper-inner quadrant of left female breast                                           |
| Malignant mast cell neoplasm                                                                               |
| Secondary malignant neoplasm of ovary                                                                      |
| Malignant neoplasm of connective and soft tissue of abdomen                                                |
| Family history of malignant neoplasm of ovary                                                              |
| Malignant neoplasm of anal canal                                                                           |
| Malignant neoplasm of other sites of rectum, rectosigmoid junction, and anus                               |
| Malignant neoplasm of nipple and areola, left female breast                                                |
| Malignant neoplasm of oropharynx, unspecified                                                              |
| Malignant neoplasm of gallbladder                                                                          |
| Malignant neoplasm of lower lobe, left bronchus or lung                                                    |
| Secondary malignant neoplasm of left adrenal gland                                                         |
| Secondary malignant neoplasm of right adrenal gland                                                        |
| Malignant neoplasm of lower-outer quadrant of right female breast                                          |
| Family history of malignant neoplasm, bladder                                                              |
| Malignant neoplasm of other and unspecified testis                                                         |
| Malignant neoplasm of specified parts of peritoneum                                                        |
| Malignant neoplasm of peritoneum, unspecified                                                              |
| Malignant neoplasm of lower-inner quadrant of left female breast                                           |
| Secondary malignant neoplasm of mediastinum                                                                |
| Malignant neoplasm of unspecified main bronchus                                                            |
| Malignant neoplasm of uterus, part unspecified                                                             |
| Personal history of malignant neoplasm of other parts of nervous tissue                                    |
| Malignant neoplasm of kidney, except pelvis                                                                |
| Malignant neoplasm of upper-inner quadrant of right female breast                                          |
| Malignant neoplasm of lower third of esophagus                                                             |
| Malignant neoplasm of other parts of pancreas                                                              |
| Malignant neoplasm of right testis, unspecified whether descended or undescended                           |
| Malignant neoplasm of other accessory sinuses                                                              |
| Secondary and unspecified malignant neoplasm of lymph nodes of inguinal region and lower limb              |
| Malignant neoplasm of base of tongue                                                                       |
| Malignant neoplasm of stomach, unspecified                                                                 |
| Malignant neoplasm of middle lobe, bronchus or lung                                                        |
| Malignant neoplasm of pancreatic duct                                                                      |
| Malignant neoplasm of lower lobe, right bronchus or lung                                                   |
| Malignant neoplasm of scapula and long bones of upper limb                                                 |
| Malignant neoplasm of unspecified ovary                                                                    |
| Malignant neoplasm of unspecified fallopian tube                                                           |
| Malignant neoplasm of connective and soft tissue of left lower limb, including hip                         |
| Malignant neoplasm of tongue, unspecified                                                                  |
| Malignant neoplasm of long bones of left lower limb                                                        |
| Malignant neoplasm of left kidney, except renal pelvis                                                     |
| Malignant neoplasm of upper-inner quadrant of female breast                                                |
| Malignant neoplasm of long bones of right lower limb                                                       |
| Malignant neoplasm of long bones of lower limb                                                             |
| Malignant neoplasm of body of stomach                                                                      |
| Malignant neoplasm of bladder, part unspecified                                                            |
| Personal history of unspecified malignant neoplasm                                                         |
| Malignant neoplasm of connective and other soft tissue of head, face, and neck                             |
| Disseminated malignant neoplasm without specification of site                                              |
| Malignant neoplasm of liver, primary, unspecified as to type                                               |
| Malignant neoplasm of ampulla of vater                                                                     |
| Personal history of malignant neoplasm of brain                                                            |
| Malignant neoplasm of connective and other soft tissue of lower limb, including hip                        |
| Malignant neoplasm of adrenal gland                                                                        |
| Malignant neoplasm of temporal lobe                                                                        |
| Malignant neoplasm of retroperitoneum                                                                      |
| Malignant neoplasm of other parts of brain                                                                 |
| Malignant neoplasm of cerebral meninges                                                                    |
| Malignant neoplasm of left main bronchus                                                                   |
| Malignant neoplasm of overlapping sites of right bronchus and lung                                         |
| Malignant neoplasm of vagina                                                                               |
| Malignant neoplasm of other specified sites of stomach                                                     |
| Malignant neoplasm of extrahepatic bile ducts                                                              |
| Personal history of malignant neoplasm of esophagus                                                        |
| Malignant neoplasm of pyriform sinus                                                                       |
| Personal history of malignant neoplasm, unspecified                                                        |
| Personal history of other malignant neoplasm of small intestine                                            |
| Malignant neoplasm of biliary tract, part unspecified site                                                 |
| Unspecified malignant neoplasm of scalp and skin of neck                                                   |
| Malignant neoplasm of ileum                                                                                |
| Malignant neoplasm of scapula and long bones of right upper limb                                           |
| Malignant neoplasm of connective and soft tissue of right lower limb, including hip                        |
| Personal history of malignant neoplasm of stomach                                                          |
| Malignant neoplasm of other specified sites                                                                |
| Personal history of malignant neoplasm of other female genital organs                                      |
| Malignant neoplasm of head, face and neck                                                                  |
| Malignant neoplasm of overlapping sites of corpus uteri                                                    |
| Malignant neoplasm of lower-inner quadrant of female breast                                                |
| Malignant neoplasm of jejunum                                                                              |
| Malignant neoplasm of fallopian tube                                                                       |
| Malignant neoplasm of lower-outer quadrant of female breast                                                |
| Malignant neoplasm of cervical esophagus                                                                   |
| Malignant neoplasm of vertebral column                                                                     |
| Malignant neoplasm of frontal lobe                                                                         |
+------------------------------------------------------------------------------------------------------------+
count: 286
~~~

Number of admissions of patients with cancer, within a total of 4,249 admissions:

~~~sql
select count(distinct hadm_id)
from neutro_diagnoses
where long_title like '%malignant%neoplasm%';
count: 1,492
~~~

Number of patients with cancer, within a total of 2,691 patients:

~~~sql
select count(distinct subject_id)
from neutro_diagnoses
where long_title like '%malignant%neoplasm%';
count: 1,151
~~~

## Lab exams of the selected admissions (`neutro_labevents`)

Retrieving all lab exams of the selected admissions besides those indicating Neutropenia:

~~~sql
drop table if exists neutro_labevents;

create table neutro_labevents as
select l.* from labevents l, neutro_admissions n
where l.subject_id = n.subject_id and l.hadm_id = n.hadm_id;
~~~

## LOINC of the selected lab exams (`neutro_itemid_loinc`)

Codes of items and respective LOINC with descriptions for the selected exams.

Filtering those items present in the exams of the selected patients/admissions:

~~~sql
create view neutro_items as
select distinct itemid from neutro_labevents order by itemid;
~~~

Creating a lab item mapping table. Items are mapped to LOINC using the `lab_itemid_to_loinc` table. Columns mapped are indicated with the `_map` suffix as they showed inconsistencies (the priority in the `label` and `fluid` columns is those without `_map` suffix):

~~~sql
create table neutro_itemid_loinc as
select ni.itemid, dl.label, ll.label as label_map, dl.fluid,
ll.fluid as fluid_map, dl.category, ll.valueuom as valueuom_map,
ll.loinc as loinc_map, ll.loinc_version as loinc_version_map,
ll.notes as notes_map
from d_labitems dl, lab_itemid_to_loinc ll, neutro_items ni
where dl.itemid = ni.itemid and ll.itemid = ni.itemid;
~~~

Exporting:

~~~sql
select 'itemid', 'label', 'label_map', 'fluid', 'fluid_map', 'category',
'valueuom_map', 'loinc_map', 'loinc_version_map', 'notes_map'
union all
select itemid, label, label_map, fluid, fluid_map, category, valueuom_map,
loinc_map, loinc_version_map, notes_map
from neutro_itemid_loinc
into outfile 'neutro_itemid_loinc.csv'
fields optionally enclosed by '"' 
terminated by ',' 
lines terminated by '\n';
~~~

### Replacing null by interrogation (Orange compatibility)

Creating a string field (`valuenum_str`) counterpart for the `valuenum` field (as numeric fields do not accept characters like ?):

~~~sql
alter table neutro_labevents
add valuenum_str varchar(255);

update neutro_labevents
set valuenum_str = cast(valuenum as char);
~~~

Converting null fields in ?, as the Orange workflow uses ? to indicate missing values:

~~~sql
update neutro_labevents
set valuenum_str = '?' where valuenum_str is null;
~~~

Exporting the table in two versions due to its size:
* 'neutro_labevents_min.csv' - set of minimal fields for the proposed analysis:


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

* 'neutro_labevents.csv' - includes a broader set of fields that could be useful in the analysis:

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

# Preparing to Import/Export

## Preparing to Import

~~~sql
show variables like "local_infile";
set global local_infile = true;
~~~

## Preparing to Export

~~~
show variables like "secure_file_priv";
~~~

Create the following two files inside the docker:
~~~
/etc/mysql/my.cnf
~/.my.cnf
~~~

Content of both my.cnf files:
~~~
[mysqld]
secure-file-priv=""
~~~
