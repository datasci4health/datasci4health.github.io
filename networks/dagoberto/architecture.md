# Network Visualizer: Architecture and Rationale

## 1. Conception and Purpose
The Network Visualizer was conceived to address the common need in data science, bioinformatics, and complex systems analysis for a lightweight, universally accessible tool to visualize graph data. Often, researchers and analysts have node and edge lists in CSV or TSV formats and need a rapid way to see the topology, map categorical data to visual properties (colors, shapes), and plot cartesian coordinates without installing heavy desktop software (like Cytoscape or Gephi) or setting up backend servers.

The application is designed to be a **purely client-side, zero-install web application**. It runs entirely in the browser, ensuring data privacy (no data is uploaded to a server) and immediate usability.

## 2. System Architecture
The application follows a monolithic, single-file architectural pattern (HTML, CSS, and JavaScript bundled together) to maximize portability. It relies on three primary external libraries delivered via Content Delivery Networks (CDNs):

*   **PapaParse:** Handles the robust parsing of raw CSV/TSV text into structured JavaScript objects. It automatically detects delimiters, ensuring seamless support for both comma-separated and tab-separated values.
*   **Cytoscape.js:** The core graph theory and rendering engine. It manages the network layout (using the force-directed `cose` algorithm or absolute `preset` positions), node/edge styling, interactivity (zooming, panning, dragging), and image exportation.
*   **Chart.js:** Provides the Cartesian charting capabilities, allowing users to switch contexts and view their node data (with X/Y coordinates) as a standard scatter plot.

### 2.1. Data Management and State
The application manages state primarily through the DOM (Document Object Model). Textareas serve as the primary data stores for:
1.  **Nodes Data:** Structural and categorical information (e.g., ID, type, labels).
2.  **Nodes Weights:** Optional numerical attributes (e.g., scores, coordinates).
3.  **Edges Data:** Topological connections (source, target) and edge attributes (type, strength).

A critical architectural decision was implementing a **Data Merging Engine**. To support the separation of structural data and numerical weights, the system performs a dynamic "Outer Join" based on node IDs before rendering. This unified dataset is then used to populate mapping dropdowns and feed the visualizers.

### 2.2. Rendering Pipelines
The application features two distinct rendering pipelines, controlled by a view-toggling mechanism:

1.  **Network Pipeline:**
    *   Reads the merged node data and edge data.
    *   Applies dynamic, data-driven styling using Cytoscape mappers.
    *   Generates a discrete color palette for categorical data.
    *   Computes a divergent color scale (Red to Gray to Blue) for normalized numerical node weights.
    *   Computes a continuous thickness scale for edge weights.
    *   Handles implicit node generation (if an edge references a node not explicitly listed in the nodes data, it is created automatically).

2.  **Chart Pipeline:**
    *   Reads the merged node data.
    *   Requires at least three columns (Label, X, Y).
    *   Groups data by a selected categorical column to assign distinct colors.
    *   Renders a scatter plot using Chart.js.

### 2.3. Persistence and Export
The architecture includes robust import/export modules:
*   **CSV/TSV Export:** Saves individual data boxes to local files.
*   **Spatial Configuration:** Extracts the current `(x, y)` positions of all nodes from the Cytoscape canvas and exports them as a CSV, allowing users to save manual layout adjustments.
*   **Full JSON Setup:** Bundles all current data, dropdown selections, and spatial coordinates into a single JSON object.
*   **URL Hydration:** Supports passing a `?setup=` URL parameter to automatically fetch and load a JSON configuration on startup, enabling easy sharing of specific visualizations.

## 3. Rationale for Key Technical Decisions
*   **Client-Side Only:** Eliminates server costs, reduces latency, and guarantees data privacy.
*   **Single File Delivery:** Ensures the tool can be shared simply by sending a file or hosting on a basic static server (like GitHub Pages).
*   **Implicit Node Generation:** Enhances robustness. In many real-world scenarios (like those detailed in "DataSci4Health"), researchers often only have edge lists. This feature ensures the app doesn't break and visualizes the topology regardless.
*   **Divergent Color Scales for Weights:** Provides immediate visual intuition for positive/negative numerical data (common in biological networks like gene expression or correlation matrices).
