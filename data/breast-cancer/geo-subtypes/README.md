# Analysis Breast Cancer Subtypes

## Based on the Paper

Gruosso, T., Mieulet, V., Cardon, M., Bourachot, B., Kieffer, Y., Devun, F., Dubois, T., Dutreix, M., Vincent‐Salomon, A., Miller, K. M., & Mechta‐Grigoriou, F. (2016).  Chronic oxidative stress promotes H2 AX protein degradation and enhances chemosensitivity in breast cancer patients. EMBO Molecular Medicine, 8(5), 527–549. https://doi.org/10.15252/emmm.201505891

## Data Extracted from [GEO](https://www.ncbi.nlm.nih.gov/geo/)

### Accession GSE45827

* [Dataset](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE45827)

* [Analysis](https://www.ncbi.nlm.nih.gov/geo/geo2r/?acc=GSE45827)

## Sub-folders

* `geo-string-manual-pre-selected`
  * comparison of Normal vs Luminal A
  * differential expression pre-selected extracted from GEO: p-value 0.001 and logFC 3
  * network produced at [STRING](https://string-db.org): physical sub-network (Experiments and Databases)
* `workflow-full`
  * comparison of Normal vs Luminal A
  * full differential expression extracted from GEO
  * full network produced at STRING
  * data treated on Orange Datamining
     * p-value 0.001 and logFC 3
     * physical sub-network (Experiments and Databases)
* `soft`
  * SOFT file download from (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE45827)
  * notebook to explore SOFT format