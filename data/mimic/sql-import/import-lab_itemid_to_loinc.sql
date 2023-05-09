DROP TABLE IF EXISTS lab_itemid_to_loinc;

CREATE TABLE lab_itemid_to_loinc (
  itemid MEDIUMINT NOT NULL,
  label VARCHAR(255),
  fluid VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  valueuom VARCHAR(255),
  loinc VARCHAR(255) NOT NULL,
  loinc_version VARCHAR(255) NOT NULL,
  notes TEXT
 )
 CHARACTER SET = UTF8MB4;
 
LOAD DATA LOCAL INFILE 'lab_itemid_to_loinc.csv' INTO TABLE lab_itemid_to_loinc
   FIELDS TERMINATED BY ',' ESCAPED BY '' OPTIONALLY ENCLOSED BY '"'
   LINES TERMINATED BY '\n'
   IGNORE 1 LINES
   (@itemid,@label,@fluid,@category,@valueuom,@loinc,@loinc_version,@notes)
 SET
   itemid = trim(@itemid),
   label = IF(@label='', NULL, trim(@label)),
   fluid = trim(@fluid),
   category = trim(@category),
   valueuom = IF(@valueuom='', NULL, trim(@valueuom)),
   loinc = trim(@loinc),
   loinc_version = trim(@loinc_version),
   notes = IF(@notes='', NULL, trim(@notes));
   
 alter table lab_itemid_to_loinc
  add index lab_itemid_to_loinc_idx01 (itemid),
  add index lab_itemid_to_loinc_idx02 (loinc, loinc_version);
   
