
## example
### fictional example (Claude)

#### GAT Builder
* **Input**: the integrated network (`nodes` and `edges`), the converted Ensembl mRNA sequences (`gene-seq`), and the converted miRWalk miR sequences (`mir-seq`).
* **Output**: Graph Attention Network (GAT).

~~~bash
python3 gat_pipeline.py --nodes example/nodes.csv --edges example/edges.csv --gene-seq example/gene_sequence.csv --mir-seq example/mir_sequence.csv --output-dir example/gat/ --encoder proteinbert --num-layers 3
~~~

## mapk
### mapk pathway with miR
* source: `knowledge-graphs/pathways/mapk`
  * `mapk-kg-mir-lm` variation, produced by `mapk-to-kg-mir-lm.ows`

#### Convert from miRWalk to expected format for GAT computation

~~~bash
python3 parse_mirwalk.py --input mapk/miRWalk_miRNA_Targets.csv  --output mapk/nodes-mapk-mir-sequence.csv
~~~

#### GAT Builder
* **Input**: the integrated network (`nodes` and `edges`), the converted Ensembl mRNA sequences (`gene-seq`), and the converted miRWalk miR sequences (`mir-seq`).
* **Output**: Graph Attention Network (GAT).

~~~bash
python3 gat_pipeline.py --nodes mapk/nodes-mapk-mir-lm.csv --edges mapk/edges-mapk-mir-lm.csv --gene-seq mapk/nodes-mapk-gene-sequence.csv --mir-seq mapk/nodes-mapk-mir-sequence.csv --output-dir mapk/gat/ --encoder proteinbert --num-layers 3
~~~

## thca
### Thyroid carcinoma (THCA) with miR
* source: `networks/microRNA`
  * `lima_pathway` variation, produced by `thca-mirna-mrna_limma_pathway.ows`

#### Convert Ensembl mRNA FASTA data to CSV for GAT computation

~~~bash
python3 fasta_to_csv.py --input thca/mart_export.fasta --output thca/nodes-mRNA-sequence.csv
~~~

#### Convert from miRWalk to expected format for GAT computation

~~~bash
python3 parse_mirwalk.py --input thca/mir-mimat-sequence_limma.csv --mir-col mimat_id --output thca/nodes-mIR-sequence.csv
~~~

#### GAT Builder
* **Input**: the integrated network (`nodes` and `edges`), the converted Ensembl mRNA sequences (`gene-seq`), and the converted miRWalk miR sequences (`mir-seq`).
* **Output**: Graph Attention Network (GAT).

~~~bash
python3 gat_pipeline.py --nodes thca/nodes-microRNA-mRNA-type-expression.csv --edges thca/edges-microRNA-mRNA-relation.csv --gene-seq thca/nodes-gene-sequence.csv --mir-seq thca/nodes-mIR-sequence.csv --output-dir thca/gat/ --encoder proteinbert --num-layers 3
~~~

## thca-mapk-only
### Thyroid carcinoma (THCA) with miR (only genes of mapk pathway)
* source: `networks/microRNA`
  * `lima_pathway_only` variation, produced by `thca-mirna-mrna_limma_pathway(filter-pathway).ows`

#### GAT Builder
* **Input**: the integrated network (`nodes` and `edges`), the converted Ensembl mRNA sequences (`gene-seq`), and the converted miRWalk miR sequences (`mir-seq`).
* **Output**: Graph Attention Network (GAT).

~~~bash
python3 gat_pipeline.py --nodes thca-mapk-only/nodes-microRNA-mRNA-type-expression.csv --edges thca-mapk-only/edges-microRNA-mRNA-relation.csv --gene-seq thca-mapk-only/nodes-gene-sequence.csv --mir-seq thca-mapk-only/nodes-mIR-sequence.csv --output-dir thca-mapk-only/gat/ --encoder proteinbert --num-layers 3
~~~
