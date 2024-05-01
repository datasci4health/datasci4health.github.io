https://geneontology.org/sparql

~~~sparql
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX metago: <http://model.geneontology.org/>
PREFIX definition: <http://purl.obolibrary.org/obo/IAO_0000115>
PREFIX enabled_by: <http://purl.obolibrary.org/obo/RO_0002333>
PREFIX BP: <http://purl.obolibrary.org/obo/GO_0008150>
PREFIX MF: <http://purl.obolibrary.org/obo/GO_0003674>
PREFIX CC: <http://purl.obolibrary.org/obo/GO_0005575>

SELECT DISTINCT ?property ?hasValue
WHERE {
  obo:GO_0016055 ?property ?hasValue
}

SELECT DISTINCT ?hasValue
WHERE {
  obo:GO_0016055 rdfs:subClassOf ?hasValue
}

SELECT DISTINCT ?super ?labels
WHERE {
  obo:GO_0016055 rdfs:subClassOf ?super .
  ?super rdfs:label ?labels .
}
~~~