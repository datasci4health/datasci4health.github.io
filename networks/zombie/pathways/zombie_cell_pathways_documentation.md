# Zombie Cell Pathways: Dataset Design and Rationale

## 1. Purpose

This document records the design rationale for a fictional, educational
graph representing three pathways inside a zombie cell:

-   **Feed** --- acquisition and processing of nutrients.
-   **Duplication** --- replication/propagation of the zombie cell.
-   **Movement** --- control of locomotion.

The network is deliberately synthetic. Protein-like identifiers, pathway
relationships, and expression values are invented for teaching graph
analysis, pathway connectivity, redundancy, bottlenecks, and
differential expression. They should not be interpreted as real
biological entities or measurements.

## 2. Requirements and design decisions

The dataset was developed from the following user requirements and
subsequent refinements:

1.  Represent three fantasy pathways---feed, duplication, and
    movement---with approximately 7--10 proteins per pathway.
2.  Supply separate node and edge CSV tables.
3.  Node table fields initially included an identifier and pathway
    membership. If a protein belongs to multiple pathways, memberships
    are listed in one field separated by `/`.
4.  Edge table fields are `source`, `target`, and `pathway`.
5.  Replace sequential identifiers with varied, zombie-inspired
    protein-like acronyms.
6.  Add a node functional-role field. The requested terms were adapted
    to common pathway terminology:
    -   **receptor**: detects an extracellular or cellular cue and
        initiates signaling;
    -   **intermediate**: relays or processes the signal within a
        pathway;
    -   **effector**: executes or directly drives a downstream cellular
        response. "Signaling protein" is also common for intermediates,
        while "effector" is a more conventional term than "actuator" in
        this context.
7.  Add redundancy before and after a bottleneck in the feed pathway.
8.  Connect the three pathway subnetworks into one connected graph,
    while retaining pathway labels and shared-node membership.
9.  Add three expression columns: baseline expression, mutant
    expression, and their difference. The mutant is a fictional
    duplication-promoting mutation. Duplication-pathway expression is
    increased substantially; feed and movement receive small, mixed
    perturbations.

## 3. Node naming and attributes

Identifiers are playful, zombie-themed protein-like names rather than
biological protein names. Examples include `ZMR1`, `BITE1`, `SPAWN1`,
`REPLX`, `CRAWL3`, and `SHAMB5`.

The node table contains:

  Column                Meaning
  --------------------- ---------------------------------------------------
  `id`                  Unique protein-like node identifier
  `pathway`             One or more pathway memberships, separated by `/`
  `role`                `receptor`, `intermediate`, or `effector`
  `expression_normal`   Simulated baseline expression value
  `expression_mutant`   Simulated expression in the mutant
  `expression_diff`     `expression_mutant - expression_normal`

Expression values are arbitrary normalized units, not calibrated RNA-seq
values. The difference is signed: positive values indicate higher
expression in the mutant, negative values indicate lower expression.

## 4. Pathway structures

### 4.1 Feed pathway

The feed pathway has redundant alternatives on both sides of the
bottleneck `HGR1`.

``` text
              ZMR1
             /    \\
         BITE1    DIGZ2
             \\    /
              ROT3
                |
              HGR1       <- bottleneck
             /    \\
        FLESH2   CRAWL3
             \\    /
             DEVOUR3
                |
              CHEW4
```

**Rationale**

-   `ZMR1` is the receptor-like entry point.
-   Two upstream branches (`BITE1` and `DIGZ2`) converge at `ROT3`.
-   `HGR1` is the single required node between the upstream convergence
    and downstream branching. Every feed-path route from `ZMR1` to
    `CHEW4` passes through it.
-   After `HGR1`, two alternative routes (`FLESH2` and `CRAWL3`)
    converge at `DEVOUR3`, then proceed to `CHEW4`.
-   `CRAWL3` is shared with movement, creating an explicit connection
    between the pathways.

This structure supports analyses of path redundancy and node-removal
vulnerability. Removing `HGR1` disconnects the feed entry from its
downstream output, while removing either branch node alone leaves an
alternative route.

### 4.2 Duplication pathway

``` text
                 SPAWN1
                /      \\
          INFECT2      VIRAL3
             |  \\      /  |
             |   \\    /   |
             |    REPLX    |
             |      ^      |
             v      |      v
            MUT8 ---+     (routes)
             \\             /
              \\           /
               REPLX
                 |
               CLONE9
                 |
               BROOD7
```

Equivalent edge-level structure (the authoritative representation is
`edges.csv`):

``` text
SPAWN1 -> INFECT2 -> MUT8 -> REPLX -> CLONE9 -> BROOD7
    \\          \\       /
     -> VIRAL3 -> MUT8
     \\          \\----> REPLX
      -> VIRAL3 ------> REPLX
```

**Rationale**

-   `SPAWN1` is the receptor-like entry point.
-   `INFECT2` and `VIRAL3` provide parallel upstream routes.
-   `MUT8` receives input from both branches.
-   `REPLX` is the designated bottleneck: all directed routes from
    `SPAWN1` to the downstream output `BROOD7` pass through `REPLX`.
-   The graph also contains direct edges from `INFECT2`, `VIRAL3`, and
    `MUT8` to `REPLX`, creating additional redundant routes before the
    bottleneck.
-   `CLONE9` and `BROOD7` form a short downstream output cascade.

The duplicated connections are intentional: they make the duplication
pathway robust to loss of individual upstream intermediates, but not to
loss of `REPLX`.

### 4.3 Movement pathway

``` text
WALKR1 -> STAG2 -> CRAWL3 -> LURCH4 -> SHAMB5 -> CHASE6
```

**Rationale**

-   `WALKR1` is the receptor-like entry point.
-   `STAG2`, `CRAWL3`, `LURCH4`, and `SHAMB5` are intermediates.
-   `CHASE6` is the terminal effector.
-   `CRAWL3` is shared with the feed pathway, coupling movement and
    nutrient-processing activity.

## 5. Cross-pathway connectivity

The three pathway subnetworks are connected through shared nodes and
explicit cross-talk edges:

``` text
Duplication: INFECT2 ----crosstalk----> ROT3 :Feed
Feed:        HGR1 -> CRAWL3 <--------- Movement
Movement:    SHAMB5 ----crosstalk----> DEVOUR3 :Feed
```

The shared-node memberships are recorded in the node `pathway` field,
for example `feed/movement`. Cross-talk edges are labeled `crosstalk` in
the edge table to distinguish them from within-pathway edges.

This design allows the overall graph to be analyzed as one connected
network while retaining pathway-level structure. Note that the node
membership field describes participation, whereas an edge's pathway
field describes the relationship's assigned category; these are not
interchangeable.

## 6. Expression design

The expression table models two conditions:

-   **Normal**: baseline fictional zombie-cell state.
-   **Mutant**: a hypothetical mutation that preferentially activates
    the duplication program.

The intended pattern is:

  -----------------------------------------------------------------------
  Pathway                             Intended mutant-vs-normal pattern
  ----------------------------------- -----------------------------------
  Duplication                         Strong positive differential
                                      expression across its nodes

  Feed                                Small positive and negative
                                      fluctuations around baseline

  Movement                            Small positive and negative
                                      fluctuations around baseline
  -----------------------------------------------------------------------

The duplication pathway has larger increases, with `REPLX` assigned the
largest increase to emphasize the central bottleneck. Feed and movement
values vary modestly in both directions so that they do not appear
uniformly unchanged or systematically activated.

These values are hand-designed illustrative data. They do not arise from
a statistical model, biological experiment, or randomized sampling
process. The earlier description of the non-duplication variation as
"random" should therefore be understood as **random-like mixed
variation**, not reproducibly sampled random noise.

## 7. Expected analysis behavior

### Differential expression

-   Sorting nodes by `expression_diff` should bring duplication-pathway
    nodes to the top.
-   Feed and movement nodes should show comparatively small changes of
    either sign.
-   A pathway-level summary (for example, mean or median difference)
    should show duplication as the strongest positive shift.

### Centrality and bottlenecks

-   `HGR1` is a feed-pathway bottleneck: all feed routes from `ZMR1` to
    `CHEW4` pass through it.
-   `REPLX` is a duplication-pathway bottleneck: all routes from
    `SPAWN1` to `BROOD7` pass through it.
-   Depending on whether centrality is calculated on the full graph or
    on pathway-filtered subgraphs, cross-talk may alter rankings.
    Analyze both views when teaching pathway-specific versus
    whole-network centrality.

### Redundancy and robustness

-   Removing `BITE1` or `DIGZ2` individually should leave an upstream
    feed alternative.
-   Removing `FLESH2` or `CRAWL3` individually should leave a downstream
    feed alternative (though removing `CRAWL3` also affects movement).
-   Removing `INFECT2` or `VIRAL3` individually should leave alternative
    duplication routes.
-   Removing `HGR1` or `REPLX` should disrupt the corresponding
    designated pathway flow.

### Pathway overlap and cross-talk

-   Shared nodes support analysis of pathway membership overlap.
-   Cross-talk edges make the complete graph connected and enable
    signal-propagation exercises across pathway boundaries.
-   Filtering by pathway labels can recover pathway-specific
    subnetworks, while retaining shared nodes where appropriate.

## 8. Data interpretation and caveats

-   This is a fantasy teaching network, not a biological pathway
    database.
-   Protein-like identifiers do not correspond to known genes or
    proteins.
-   Expression values are arbitrary and should not be treated as fold
    changes, log counts, p-values, or statistically significant
    differential expression.
-   The graph is directed. An edge indicates a hypothetical directed
    interaction or influence, not necessarily a biochemical reaction.
-   The edge table's `crosstalk` label denotes cross-pathway links;
    within-pathway edges use `feed`, `duplication`, or `movement`.
-   The network is intentionally small and hand-crafted for
    interpretability. Its topology is designed to demonstrate concepts
    rather than reproduce biological complexity.

## 9. Files

The associated data files are:

-   `nodes_expression.csv` --- node identifiers, pathway memberships,
    roles, and expression values.
-   `edges.csv` --- directed source-target relationships and
    pathway/cross-talk labels.

For reproducible analysis, preserve the identifiers and use the CSV
tables as the authoritative graph specification. The diagrams in this
document are explanatory renderings of the intended topology.
