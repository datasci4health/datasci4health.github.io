# Human symptoms–disease network

Goh, K. il, Cusick, M. E., Valle, D., Childs, B., Vidal, M., & Barabási, A. L. (2007). The human disease network. Proceedings of the National Academy of Sciences of the United States of America, 104(21), 8685–8690. https://doi.org/10.1073/PNAS.0701361104

Zhou, X., Menche, J., Barabási, A.-L., & Sharma, A. (2014). Human symptoms–disease network. Nature Communications, 5(1), 4212. https://doi.org/10.1038/ncomms5212

## Class 2024-04-30 Network Science - Mapping and Transforming

* folder `mapping-transforming`

Orange workflow `converte-list-rows.ows` prepares files of three sources:
* `01-source-nature` - original from the articles on Nature
* `02-source-human-phenotype-ontology` - Human Phenotype Ontology (genes x diseases)
* `03-source-comparative-toxicogenomics-database` - Comparative Toxicogenomics Database (maps MeSH to OMIM)

Prepared files are saved at:

* `04-prepared` - files to be read and processed by Cypher

## Class 2024-05-02 Mapping and Workflow

* folder `mapping-transforming`

Relations between symptoms and diseases manually selected and stored in:
* `05-manually-selected` -  rationale stored at `symptom-disease(selected).xlsx`

Besides processing the simple example in Cypher, there two equivalent examples:

* `06-jupyter-networkx` - Jupyter example using NetworkX (files are also converted to Pajek for Orange)
* `07-orange-network` - Orange example using networks 

## Class 2024-05-09 Clusters and Communities

* folder `cluster-module`

* `01-preprocess` - data from symptoms and diseases are converted by Orange to a network disease-disease with different similarity thresholds (0.8 and 0.95)

This data is source to the other three projects:

* `02-cytoscape` - networks are imported to CytoScape, which infers communities
* `03-jupyter-networkx` - networks are imported, displayed and converted (to Pajek for Orange) at Jupyter with NetworkX
* `04-orange-cluster-network` - clusters and communities (network) are compared