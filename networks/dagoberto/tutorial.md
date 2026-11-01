# Network Visualizer: Usage Tutorial

Welcome to the Network Visualizer! This tool allows you to build, style, and analyze network graphs and scatter plots directly in your browser.

## 1. Getting Started

When you open the application (e.g., `network_viewer.html`), you will see a sidebar for **Data Setup** on the left and a main visual area on the right.

### Inputting Data
You have three ways to load your data (CSV, TSV, or TXT formats):
1.  **Type or Paste:** Copy data from Excel or a text editor and paste it directly into the text boxes.
2.  **Upload:** Click the "Choose File" button above any text box.
3.  **Drag and Drop:** Drag a file from your computer and drop it over the text box (the box will turn blue).

The system automatically detects whether you are using tabs or commas and converts it to standard CSV format.

## 2. Understanding the Data Boxes

### Box 1: Nodes Data (Required: `id`)
This box defines the entities in your network. 
*   **Must have** a column named `id` (or the first column will be treated as the ID).
*   Include categorical columns here (e.g., `type`, `category`) to control shapes and colors later.

### Box 2: Nodes Weights (Optional)
Use this box to separate your numerical data from your structural data. 
*   **Must have** an `id` column to match with Box 1.
*   Include numerical data here (e.g., `score`, `expression_level`, `x`, `y`).
*   *Note: The system automatically merges Box 1 and Box 2 internally based on the ID.*

### Box 3: Edges Data (Required: `source`, `target`)
This box defines the connections between your nodes.
*   **Must have** a `source` column and a `target` column (matching the IDs in your node data).
*   If you include an edge that mentions a node not listed in Box 1 or 2, the system will automatically create it for you!

## 3. Styling the Network

Once your data is loaded, use the dropdown menus below the text boxes to map your data to visual properties:

*   **Node Type Col (Shape/Color):** Select a categorical column. Different categories will get different shapes and colors.
*   **Node Numeric Color Col (Overrides):** Select a numerical column. This overrides the categorical color, applying a gradient scale (Red for negative values, Gray for zero, Blue for positive values).
*   **Edge Type Col (Line Style):** Select a categorical column. Different categories get different dashing styles (solid, dashed, dotted) and colors.
*   **Edge Thickness Col (Numeric):** Select a numerical column to scale the width of the connection lines.

## 4. Rendering and Interaction

Click the **Render Network** button. 
*   **Interact:** Zoom with your scroll wheel, click and drag the background to pan, and drag individual nodes to arrange them.
*   **View Chart:** If your merged node data has at least 3 columns (a label, an X value, and a Y value), click **Plot Nodes Chart** to see your data as a Cartesian scatter plot.

## 5. Saving and Loading

The application provides several ways to save your work:

*   **Save CSV:** The small green buttons save the current contents of a specific text box to a file.
*   **Save Positions (Spatial Configuration):** If you spent time dragging nodes into a perfect layout, click this button to save their exact X and Y coordinates. You can load this file later to snap them back into place.
*   **Save Full JSON:** This is the most powerful save feature. It bundles all your text boxes, your dropdown selections, and your node positions into one file.
*   **Load Full JSON:** Restores your entire workspace exactly as you left it.

### Sharing via URL
If you host a setup JSON file online, you can share a link that automatically loads it on startup by adding the `?setup=` parameter. 
Example: `http://your-site.com/network_viewer.html?setup=https://your-site.com/my-graph.json`

(Note: For advanced data preparation from unstructured datasets, refer to tools mentioned in the "DataSci4Health" guidelines).
