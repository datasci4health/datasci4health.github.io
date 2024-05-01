# Orange Script

Creating your own domain with metas:

~~~python
domain = Domain([], [ContinuousVariable("logFC")],
                metas=[StringVariable("Gene.ID"),
                       StringVariable("Gene.symbol")])
~~~

New table cropping /// fields:

~~~python
import numpy as np
from Orange.data import Table, Domain, ContinuousVariable, StringVariable

gene = []
logfc = []

for inst in in_data:
    if len(inst["Gene.symbol"].value) > 0:
        gene_symbol = inst["Gene.symbol"].value
        gene_id = inst["Gene.ID"].value
        if "///" in gene_symbol:
            gene_symbol = gene_symbol.split("///")[0]
            gene_id = gene_id.split("///")[0]
        gene.append([inst["ID"].value, gene_symbol, inst["Gene.title"].value, gene_id])
        logfc.append([inst["adj.P.Val"], inst["P.Value"], inst["t"], inst["B"], inst["logFC"]])
        
print("generated")

out_data = Table.from_numpy(in_data.domain, np.array(logfc), metas=np.array(gene))
~~~

