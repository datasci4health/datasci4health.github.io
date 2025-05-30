# SPARQL endpoints

* Gene Ontology: https://geneontology.org/sparql

* UniProt (better): https://sparql.uniprot.org/sparql

# PRICKLE2 - Prickle-like protein 2 (UniProtKB:Q7Z3G6)

* URI: http://purl.uniprot.org/uniprot/Q7Z3G6

## All subjects related to the protein

~~~sparql
PREFIX up: <http://purl.uniprot.org/uniprot/>

SELECT DISTINCT ?subject ?property
WHERE {
  ?subject ?property up:Q7Z3G6 .
}
~~~

## All properties and objects related to the protein

~~~sparql
PREFIX up: <http://purl.uniprot.org/uniprot/>

SELECT DISTINCT ?property ?object
WHERE {
  up:Q7Z3G6 ?property ?object .
}
~~~

## All proteins URI with the label "Prickle-like protein 2"

~~~sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?protein ?label
WHERE {
  ?protein rdfs:label "Prickle-like protein 2" .
}
~~~

## All objects classified with the protein

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up:      <http://purl.uniprot.org/uniprot/>
PREFIX up_core: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?object ?label
WHERE {
  up:Q7Z3G6 up_core:classifiedWith ?object .
  ?object rdfs:label ?label .
}
~~~

~~~csv
object, label
http://purl.obolibrary.org/obo/GO_0005737,"cytoplasm"
http://purl.obolibrary.org/obo/GO_0031965,"nuclear membrane"
http://purl.obolibrary.org/obo/GO_0008270,"zinc ion binding"
http://purl.obolibrary.org/obo/GO_0060071,"Wnt signaling pathway, planar cell polarity pathway"
~~~

## Organism related to this protein

~~~sparql
PREFIX up:      <http://purl.uniprot.org/uniprot/>
PREFIX up_core: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?taxon ?scientific_name
WHERE {
  up:Q7Z3G6 up_core:organism ?taxon .
  ?taxon up_core:scientificName ?scientific_name .
}
~~~

## Gene related to this protein

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up:      <http://purl.uniprot.org/uniprot/>
PREFIX up_core: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?gene ?label
WHERE {
  up:Q7Z3G6 up_core:encodedBy ?gene .
  ?gene rdfs:label ?label .
}
~~~

# Wnt signaling pathway (GO:0016055)

* URI: https://amigo.geneontology.org/amigo/term/GO:0016055

## All superclasses of the pathway 

~~~sparql
PREFIX obo:  <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?super ?labels
WHERE {
  obo:GO_0016055 rdfs:subClassOf ?super .
  ?super rdfs:label ?labels .
}
~~~

## All subclasses of the pathway

~~~sparql
PREFIX obo:  <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sub ?label
WHERE {
  ?sub rdfs:subClassOf obo:GO_0016055 .
  ?sub rdfs:label ?label .
}
~~~

## All properties and objects related to the pathway

~~~sparql
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?property ?object
WHERE {
  obo:GO_0016055 ?property ?object .
}
~~~

## All subjects and properties related to the pathway

~~~sparql
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?subject ?property
WHERE {
   ?subject ?property obo:GO_0016055 .
}
~~~

## All subjects (URI and label) classified with the pathway

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo:     <http://purl.obolibrary.org/obo/>
PREFIX up_core: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?uri ?label
WHERE {
  ?uri up_core:classifiedWith obo:GO_0016055 .
  ?uri rdfs:label ?label .
}
~~~

## All proteins (URI and label) classified with the pathway

~~~sparql
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo:     <http://purl.obolibrary.org/obo/>
PREFIX up_core: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?protein ?label
WHERE {
  ?protein up_core:classifiedWith obo:GO_0016055 .
  ?protein rdf:type up_core:Protein .
  ?protein rdfs:label ?label .
}
~~~

## All proteins classified with the pathway and their organism with the scientific name

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up_core: <http://purl.uniprot.org/core/>
PREFIX obo:     <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?protein ?label ?organism ?scientific_name
WHERE {
  ?protein up_core:classifiedWith obo:GO_0016055 .
  ?protein rdf:type up_core:Protein .
  ?protein rdfs:label ?label .
  ?protein up_core:organism ?organism .
  ?organism up_core:scientificName ?scientific_name .
}
~~~

## All proteins classified with the pathway for the organism Homo sapiens (taxon:9606)

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up_core: <http://purl.uniprot.org/core/>
PREFIX obo:     <http://purl.obolibrary.org/obo/>
PREFIX taxon:   <http://purl.uniprot.org/taxonomy/>

SELECT DISTINCT ?protein ?label
WHERE {
  ?protein up_core:classifiedWith obo:GO_0016055 .
  ?protein rdf:type up_core:Protein .
  ?protein rdfs:label ?label .
  ?protein up_core:organism taxon:9606 .
}
~~~

## All proteins classified with the pathway for the organism Mus musculus (taxon:10090)

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up_core: <http://purl.uniprot.org/core/>
PREFIX obo:     <http://purl.obolibrary.org/obo/>
PREFIX taxon:   <http://purl.uniprot.org/taxonomy/>

SELECT DISTINCT ?protein ?label
WHERE {
  ?protein up_core:classifiedWith obo:GO_0016055 .
  ?protein rdf:type up_core:Protein .
  ?protein rdfs:label ?label .
  ?protein up_core:organism taxon:10090 .
}
~~~

# Cluster Casein kinase I isoform delta - 100% (UniRef100_Q9DC28)

## All subjects and properties related to the cluster

~~~sparql
PREFIX up_ref: <http://purl.uniprot.org/uniref/>

SELECT DISTINCT ?subject ?property
WHERE {
  ?subject ?property up_ref:UniRef100_Q9DC28 .
}
~~~

## All properties and objects related to the cluster

~~~sparql
PREFIX up_ref: <http://purl.uniprot.org/uniref/>

SELECT DISTINCT ?property ?object
WHERE {
  up_ref:UniRef100_Q9DC28 ?property ?object .
}
~~~

## The UniParc which this cluster is member of

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up_core: <http://purl.uniprot.org/core/>
PREFIX up_ref:  <http://purl.uniprot.org/uniref/>

SELECT DISTINCT ?uniparc ?label
WHERE {
  up_ref:UniRef100_Q9DC28 up_core:member ?uniparc .
  ?uniparc rdfs:label ?label .
}
~~~

~~~
uniparc
UPI0000027B20
~~~

## All properties and objects related to the UniParc

~~~sparql
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up_core: <http://purl.uniprot.org/core/>
PREFIX up_arc:  <http://purl.uniprot.org/uniparc/>

SELECT DISTINCT ?protein ?organism ?scientific_name
WHERE {
  up_arc:UPI0000027B20 up_core:sequenceFor ?protein .
  ?protein rdf:type up_core:Protein .
  ?protein up_core:organism ?organism .
  ?organism up_core:scientificName ?scientific_name .
}
~~~

# Wnt signaling pathway, planar cell polarity pathway (GO:0060071)

## All proteins classified with the pathway

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up_core: <http://purl.uniprot.org/core/>
PREFIX obo:     <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?protein ?label
WHERE {
  ?protein up_core:classifiedWith obo:GO_0060071 .
  ?protein rdf:type up_core:Protein .
  ?protein rdfs:label ?label .
}
~~~

## All proteins classified with the pathway and their organism

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up_core: <http://purl.uniprot.org/core/>
PREFIX obo:     <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?protein ?label ?organism
WHERE {
  ?protein up_core:classifiedWith obo:GO_0060071 .
  ?protein rdf:type up_core:Protein .
  ?protein rdfs:label ?label .
  ?protein up_core:organism ?organism .
}
~~~

## All proteins classified with the pathway and their organism with the scientific name

~~~sparql
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up_core: <http://purl.uniprot.org/core/>
PREFIX obo:     <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?protein ?label ?organism ?scientific_name
WHERE {
  ?protein up_core:classifiedWith obo:GO_0060071 .
  ?protein rdf:type up_core:Protein .
  ?protein rdfs:label ?label .
  ?protein up_core:organism ?organism .
  ?organism up_core:scientificName ?scientific_name .
}
~~~
