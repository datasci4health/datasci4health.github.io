## Limpando a Base

Vamos agora limpar a base para iniciarmos um novo ciclo de queries. Inicialmente, devem ser removidas todas as arestas:

~~~cypher
MATCH (n1)-[e]->(n2)
DELETE e
~~~

Em seguida todos os nós:

~~~cypher
MATCH (n)
DELETE n
~~~

Note que removemos primeiro as arestas porque um nó não se deixará remover se tiver arestas a ele ligadas.

~~~cypher
MATCH (d1:Disease)-[r1:Related]->(:Gene)<-[r2:Related]-(d2:Disease)
WHERE d1.meshId > d2.meshId
MERGE (d1)-[gs:GeneSimilar]->(d2)
ON CREATE SET gs.weight = 1
ON MATCH SET gs.weight = gs.weight + 1
~~~

~~~cypher
MATCH (d1:Disease)-[gs:GeneSimilar]->(d2:Disease)
RETURN d1,gs,d2
~~~

~~~cypher
MATCH (d1:Disease)-[h1:Has]->(:Symptom)<-[h2:Has]-(d2:Disease)
WHERE d1.meshId > d2.meshId
MERGE (d1)-[ss:SymptomSimilar]->(d2)
ON CREATE SET ss.count = 1
ON CREATE SET ss.sumTfidf = (h1.tfidf + h2.tfidf) / 2
ON MATCH SET ss.count = ss.count + 1
ON MATCH SET ss.sumTfidf = ss.sumTfidf + (h1.tfidf + h2.tfidf) / 2
~~~

~~~cypher
MATCH (d1:Disease)-[ss:SymptomSimilar]->(d2:Disease)
SET ss.tfidf = ss.sumTfidf / ss.count
~~~

~~~cypher
MATCH (d1:Disease)-[ss:SymptomSimilar]->(d2:Disease)
RETURN d1,ss,d2
~~~

~~~cypher
MATCH (d1:Disease)-[ss:SymptomSimilar]->(d2:Disease)
RETURN d1.meshTerm,ss.tfidf,d2.meshTerm
~~~

~~~cypher
MATCH (d1:Disease)-[ss:SymptomSimilar]->(d2:Disease)
RETURN AVG(ss.tfidf)
~~~

~~~cypher
MATCH (d1:Disease)-[ss:SymptomSimilar]->(d2:Disease)
WHERE ss.tfidf > 10
RETURN d1,ss,d2
~~~