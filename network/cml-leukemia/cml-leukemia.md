MATCH (p1:Protein)-[r:Related]->(p2:Protein)
RETURN p1, r, p2

MATCH (p1:Protein)-[r:Related]->(p2:Protein)
WHERE r.database > 0 or r.experimental > 0
RETURN p1, r, p2

MATCH (p1:Protein)-[r:Related]->(p2:Protein)
WHERE r.database > 0 and r.experimental > 0
RETURN p1, r, p2

MATCH (p1:Protein)-[r:Related]->(p2:Protein)
WHERE r.database > 0 and r.experimental > 0
CREATE (p1)-[i:Interacts {weight: (r.database + r.experimental) / 2}]->(p2)

MATCH (p1:Protein)-[i:Interacts]->(p2:Protein)
RETURN p1, i, p2

MATCH (p1:Protein)-[i:Interacts]->(p2:Protein)
RETURN p1.name, i.weight, p2.name