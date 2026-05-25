
## example
### fictional example (Claude)

~~~bash
python3 gat_pipeline.py --nodes example/nodes.csv --edges example/edges.csv --gene-seq example/gene_sequence.csv --mir-seq example/mir_sequence.csv --output-dir example/gat/ --encoder proteinbert --num-layers 3
~~~

## mapk
### mapk pathway with miR
* source: `knowledge-graphs/pathways/mapk`
  * `mapk-kg-mir-lm` variation, produced by `mapk-to-kg-mir-lm.ows`

#### Convert from miRWalk to expected input

~~~bash
python3 parse_mirwalk.py --input mapk/miRWalk_miRNA_Targets.csv  --output mapk/nodes-mapk-mir-sequence.csv
~~~

~~~bash
python3 gat_pipeline.py --nodes mapk/nodes-mapk-mir-lm.csv --edges mapk/edges-mapk-mir-lm.csv --gene-seq mapk/nodes-mapk-gene-sequence.csv --mir-seq mapk/nodes-mapk-mir-sequence.csv --output-dir mapk/gat/ --encoder proteinbert --num-layers 3
~~~

## thca
### Thyroid carcinoma (THCA) with miR
* source: `networks/microRNA`
  * `lima_pathway` variation, produced by `thca-mirna-mrna_limma_pathway.ows`

~~~bash
python3 fasta_to_csv.py --input thca/mart_export.fasta --output thca/nodes-mRNA-sequence.csv
~~~

~~~bash
python3 parse_mirwalk.py --input thca/miRWalk_miRNA_Targets_limma.csv  --output thca/nodes-mIR-sequence.csv
~~~

~~~bash
python3 gat_pipeline.py --nodes thca/nodes-microRNA-mRNA-type-expression.csv --edges thca/edges-microRNA-mRNA-relation.csv --gene-seq thca/nodes-gene-sequence.csv --mir-seq thca/nodes-mIR-sequence.csv --output-dir thca/gat/ --encoder proteinbert --num-layers 3
~~~
