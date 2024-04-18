import numpy as np
from Orange.data import Table, Domain, ContinuousVariable, StringVariable

gene = []
logfc = []

for inst in in_data:
    if "///" not in inst["Gene.ID"]:
        gene.append([inst.metas[0], inst.metas[1]])
        logfc.append([inst["logFC"]])
    else:
        id_list = inst.metas[0].split("///")
        symbol_list = inst.metas[1].split("///")
        for s in range(0, len(id_list)):
            gene.append([id_list[s], symbol_list[s]])
            logfc.append([inst["logFC"]])
        
print("generated")

out_data = Table.from_numpy(in_data.domain, np.array(logfc), metas=np.array(gene))