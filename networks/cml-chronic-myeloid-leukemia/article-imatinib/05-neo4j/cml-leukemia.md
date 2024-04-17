MATCH (p1)-[i]->(p2)
DELETE i

MATCH (p)
DELETE p


MATCH (p1:ProteinSTRING)-[i:InteractSTRING]->(p2:ProteinSTRING)
RETURN p1, i, p2

MATCH (p1:ProteinGEO)
RETURN p1

MATCH (p1:ProteinSTRING)
MATCH (p2:ProteinGEO)
WHERE p1.name = p2.name
RETURN COUNT(p1)

MATCH (p1:ProteinSTRING)
MATCH (p2:ProteinGEO)
WHERE p1.name = p2.name
SET p1.logfc = p2.logfc

MATCH (p:ProteinSTRING)
WHERE p.logfc <> 0
RETURN p.name, p.logfc

MATCH (p1:ProteinSTRING)-[:InteractSTRING]->(p2:ProteinSTRING)
RETURN p1.name, p2.name


MATCH (p1:Protein)-[r:Related]->(p2:Protein)
RETURN p1, r, p2

MATCH (p1:Protein)-[r:Related]->(p2:Protein)
WHERE r.database > 0 or r.experimental > 0
RETURN p1, r, p2

MATCH (p1:Protein)-[r:Related]->(p2:Protein)
WHERE r.database > 0 and r.experimental > 0
RETURN p1, r, p2

MATCH (p1:Protein)-[r:Related]->(p2:Protein)
WHERE (r.database + r.experimental) / 2 > 0.5
RETURN p1, r, p2

MATCH (p1:Protein)-[r:Related]->(p2:Protein)
WHERE r.database > 0 or r.experimental > 0
CREATE (p1)-[i:Interacts {weight: (r.database + r.experimental) / 2}]->(p2)

MATCH (p1:Protein)-[i:Interacts]->(p2:Protein)
RETURN p1, i, p2

MATCH (p1:Protein)-[i:Interacts]->(p2:Protein)
RETURN p1.name, i.weight, p2.name


MATCH (p1:Protein)
MATCH (p2:ProteinGEO)
WHERE p1.name = p2.name
RETURN AVG(ABS(p2.logfc))


MATCH (p1:ProteinGS)-[r:RelatedGS]->(p2:ProteinGS)
WHERE r.database > 0 or r.experimental > 0
CREATE (p1)-[i:InteractsGS {weight: (r.database + r.experimental) / 2}]->(p2)

MATCH (p1:ProteinGS)-[i:InteractsGS]->(p2:ProteinGS)
RETURN p1, i, p2

MATCH (p1:ProteinGS)
MATCH (p2:ProteinGEO)
WHERE p1.name = p2.name
RETURN COUNT(p1)

MATCH (p1:ProteinGS)
MATCH (p2:ProteinGEO)
WHERE p1.name = p2.name
RETURN AVG(ABS(p2.logfc))

MATCH (p1:ProteinGS)
MATCH (p2:ProteinGEO)
WHERE p1.name = p2.name
SET p1.logfc = p2.logfc

MATCH (p1:ProteinGS)-[i:InteractsGS*0..1]->(p2:ProteinGS)
RETURN p1, i, p2

MATCH (p1:ProteinGS)-[i:InteractsGS]->(p2:ProteinGS)
WHERE p1.logfc <> 0
RETURN p1, i, p2

MATCH (p1:ProteinGS)-[i:InteractsGS*0..1]->(p2:ProteinGS)
WHERE p1.logfc <> 0 AND p2.logfc <> 0
RETURN p1, i, p2

MATCH (p:ProteinGS)
WHERE p.logfc <> 0
RETURN p.name, p.logfc

MATCH (p1:ProteinGS)-[i:InteractsGS*0..1]->(p2:ProteinGS)
WHERE p1.logfc <> 0 AND p2.logfc <> 0
RETURN p1.name, p2.name