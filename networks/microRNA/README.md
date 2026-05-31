# microRNA-mRNA

## Data source from [The Cancer Genome Atlas Program (TCGA)](https://www.cancer.gov/ccg/research/genome-sequencing/tcga) adapted by [Firehose](https://gdac.broadinstitute.org/)

### [Thyroid carcinoma (THCA)](http://firebrowse.org/?cohort=THCA)

* Clinical Data
  * [Clinical_Pick_Tier1](http://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/THCA/20160128/gdac.broadinstitute.org_THCA.Clinical_Pick_Tier1.Level_4.2016012800.0.0.tar.gz)
  * folder: [firehose-clinical](firehose-clinical/)
* microRNA seq
  * [illuminahiseq_mirnaseq-miR_isoform_expression](http://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/THCA/20160128/gdac.broadinstitute.org_THCA.Merge_mirnaseq__illuminahiseq_mirnaseq__bcgsc_ca__Level_3__miR_isoform_expression__data.Level_3.2016012800.0.0.tar.gz)
  * folder: [firehose-microRNA](firehose-microRNA/)
* mRNA seq
  * [illuminahiseq_rnaseqv2-RSEM_genes_normalized](http://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/THCA/20160128/gdac.broadinstitute.org_THCA.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz)
  * folder: [firehose-mRNA](firehose-mRNA/)

## [miRWalk](http://mirwalk.umm.uni-heidelberg.de/)
* input/output folder: [miRWalk](miRWalk/)

## [miRBase](https://www.mirbase.org/)
* [FTP Site](https://www.mirbase.org/download/CURRENT/)
  * [miRNA.csv incorrectly labeled link as miRNA.xls](https://www.mirbase.org/download/miRNA.csv)
  * folder: [miRBase](miRBase/)

## Orange Workflows
* **THCA mRNA-miR network**: Departs from differentially expressed miR and adds mRNAs that are miR targets. Three networks are produced for CytoScape: miR-mRNA (bipartite), miR-miR (projection), and mRNA-mRNA (projection).
  * workflow: `thca-mirna-mrna.ows`
  * CytoScape output: [cytoscape/native folder](cytoscape/native/)
* **THCA mRNA-miR network (Limma)**: Same as the previous, computing differential expression with the Limma R Package.
  * workflow: `thca-mirna-mrna_limma.ows`
  * CytoScape output: [cytoscape/limma folder](cytoscape/limma/)
* **THCA mRNA-miR network (Limma) and MAPK pathway**: Departs from **THCA mRNA-miR network (Limma)**. The network links target genes (mRNAs) of differentially expressed miRs with all MAPK genes (mRNAs), producing an overview of the action of miRs on the pathway, in addition to external articulations. Produces miR sequences and mRNA IDs for Ensembl to generate sequences. Both sequences feed embedding algorithms and Graph Attention Network (GAT) computation.
  * workflow: `thca-mirna-mrna_limma_pathway.ows`
  * CytoScape output: [cytoscape/limma_pathway folder](cytoscape/limma_pathway/)
  * Ensembl output: [ensembl](ensembl/)
  * GAT output: [gat](gat/)
* **THCA mRNA-miR network (Limma) and MAPK - filter pathway only**: Takes the output (nodes and edges) of the `thca-mirna-mrna_limma_pathway.ows` workflow and filters only genes (mRNAs) that are part of the pathway and those miRs that regulate them.
  * workflow: `thca-mirna-mrna_limma_pathway(filter-pathway).ows`
  * CytoScape output: [cytoscape/limma_pathway_only folder](cytoscape/limma_pathway_only/)


## CytoScape
  * input/output folder: [cytoscape](cytoscape/)
