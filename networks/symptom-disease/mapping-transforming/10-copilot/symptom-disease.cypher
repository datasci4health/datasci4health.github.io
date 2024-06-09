// Cypher Code

// The name of the command to create a node is CREATE

// The complete statement to create a node is CREATE (n:Label {property1: value1, property2: value2, ...})

// Create a node of a Disease type and a name "Diabetes Mellitus"
CREATE (d:Disease {name: "Diabetes Mellitus"})

// Create a node of a Symptom type and a name "Obesity"
CREATE (s:Symptom {name: "Obesity"})

// Connect the previous two nodes with a Has relationship
MATCH (d:Disease {name: "Diabetes Mellitus"}), (s:Symptom {name: "Obesity"})
CREATE (d)-[:Has]->(s)

// Improved code
MATCH (d:Disease {name: "Diabetes Mellitus"})
MATCH (s:Symptom {name: "Obesity"})
CREATE (d)-[:Has]->(s)

// Query the database to see the results
MATCH (d:Disease)-[r:Has]->(s:Symptom)
RETURN d, r, s

// CSV Table of Diseases
MeSH Disease ID,MeSH Disease Term,OMIM Disease ID
MESH:D015464,"Leukemia, Myelogenous, Chronic, BCR-ABL Positive",OMIM:608232
MESH:D018860,Sneddon Syndrome,OMIM:182410
MESH:C535729,Dyschromatosis symmetrica hereditaria 1,OMIM:127400
MESH:C535607,Aicardi-Goutieres syndrome,OMIM:615010

// Load the CSV table from the given URL
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/datasci4health/datasci4health.github.io/master/networks/symptom-disease/mapping-transforming/04-prepared/diseases.csv' AS row
// Create a node for each row in the CSV table
CREATE (:Disease {
  MeSH_Disease_ID: row.`MeSH Disease ID`,
  MeSH_Disease_Term: row.`MeSH Disease Term`,
  OMIM_Disease_ID: row.`OMIM Disease ID`
})

// Query the database to see the resulting graph of the last table
MATCH (d:Disease)
RETURN d

