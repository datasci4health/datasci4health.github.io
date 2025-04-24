# Melanoma pathways in Cypher

(:Protein {name:"MEK"})-[:Activate]->(:Protein {name:"ERK"})

(:Compound {name:"PLX4072"})-[:Deactivate]->(:Protein {name:"BRAF"})-[:Activate]->(:Protein {name:"MEK"})

# Generic Graph

({name:"A"})-[:Activate]->({name:"B"})->[:Deactivate]->({name:"C"})->[:Activate]->({name:"D"})
