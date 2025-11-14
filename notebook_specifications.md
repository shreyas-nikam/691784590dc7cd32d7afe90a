
# Technical Specification for Jupyter Notebook: ARIA CoRIx Tree Explorer

## 1. Notebook Overview

This Jupyter Notebook, the ARIA CoRIx Tree Explorer, provides an interactive environment for users to visualize and understand the Contextual Robustness Index (CoRIx) measurement trees. It aims to demystify the hierarchical structure and aggregation logic of CoRIx scores, which are crucial for assessing the validity risk of AI applications as detailed in the NIST AI 700-2: ARIA 0.1 Pilot Evaluation Report [1].

### Learning Goals

Upon completion of this notebook, users will be able to:
-   Understand the hierarchical structure and aggregation logic of CoRIx measurement trees.
-   Identify how different testing layers (model testing, red teaming, field testing) contribute to overall AI validity risk scores.
-   Analyze the impact of annotator labels and user perceptions on the assessment of AI system trustworthiness.
-   Interpret the meaning of CoRIx scores, where higher scores indicate greater negative risk.

## 2. Code Requirements

### List of Expected Libraries

-   `pandas` (for data manipulation and handling tabular data)
-   `numpy` (for numerical operations, especially aggregation functions like mean and max)
-   `plotly.graph_objects` (for creating interactive, high-quality tree visualizations)
-   `ipywidgets` (for creating interactive user interface elements like dropdowns and output displays within the notebook)

### List of Algorithms or Functions to be Implemented (without code implementations)

1.  **`load_corix_dataset(filepath: str) -> pandas.DataFrame`**:
    -   **Purpose**: Loads the CoRIx scores from a specified CSV file into a pandas DataFrame.
    -   **Input**: `filepath` (string path to the CSV file).
    -   **Output**: `pandas.DataFrame` containing the raw CoRIx data.

2.  **`build_corix_tree_data(dataframe: pandas.DataFrame, application: str, scenario: str) -> dict`**:
    -   **Purpose**: Processes the flat CoRIx DataFrame for a specific application and scenario, constructing a hierarchical data structure (e.g., a nested dictionary or list of node objects) suitable for tree visualization. This function will implicitly re-calculate aggregated scores for parent nodes based on the specified aggregation logic for each level.
    -   **Input**: `dataframe` (the full CoRIx `pandas.DataFrame`), `application` (string, e.g., "Application A"), `scenario` (string, e.g., "Pathfinder").
    -   **Output**: A dictionary representing the tree, where each entry is a node with attributes like `id`, `name`, `parent_id`, `score`, `level`, `construct`, `children`, and `raw_assessment_items` (for Level 5 nodes).

3.  **`aggregate_node_score(children_scores: list, level: int) -> float`**:
    -   **Purpose**: Calculates the aggregated score for a parent node based on the scores of its children and the CoRIx aggregation rules for its level.
    -   **Input**: `children_scores` (list of numeric scores from child nodes), `level` (integer representing the parent node's level).
    -   **Output**: A single aggregated `float` score.
    -   **Logic**:
        -   If `level` is 2 (Risks): apply `numpy.max` to `children_scores`.
        -   If `level` is 3, 4, or 5: apply `numpy.mean` to `children_scores`.

4.  **`create_interactive_corix_tree_plot(tree_data: dict, selected_node_id: Optional[str] = None) -> plotly.graph_objects.Figure`**:
    -   **Purpose**: Generates an interactive node-link diagram visualization of the CoRIx tree using `plotly.graph_objects`.
    -   **Input**: `tree_data` (the hierarchical data structure representing the CoRIx tree), `selected_node_id` (optional string ID of a node to highlight).
    -   **Output**: A `plotly.graph_objects.Figure` object.
    -   **Features**:
        -   Nodes display their aggregated CoRIx score.
        -   Connections represent parent-child relationships.
        -   Hovering over a node displays its full name, level, construct, and score.
        -   The function should be designed to update dynamically based on user interaction (e.g., selection of application/scenario, or simulated node expansion/collapse via a slider for depth).

5.  **`display_node_details(tree_data: dict, node_id: str) -> ipywidgets.Output`**:
    -   **Purpose**: Extracts and displays detailed information for a specific node, including its direct children and the specific assessment items/questionnaire questions that contribute to its score.
    -   **Input**: `tree_data` (the hierarchical data structure), `node_id` (string ID of the selected node).
    -   **Output**: An `ipywidgets.Output` widget containing formatted text or a table of details.

6.  **`on_selection_change(change: dict)`**:
    -   **Purpose**: A callback function for `ipywidgets.Dropdown` that triggers `build_corix_tree_data` and `create_interactive_corix_tree_plot` whenever the selected application or scenario changes.
    -   **Input**: `change` (dictionary containing information about the widget's state change).
    -   **Output**: Renders the updated tree visualization and clears/updates node details.

### Visualization Like Charts, Tables, Plots That Should Be Generated

1.  **Interactive CoRIx Tree Visualization (Node-Link Diagram)**:
    -   **Type**: `plotly.graph_objects.Figure` (specifically using `go.Scatter` for nodes and `go.Scatter` for links to construct a node-link diagram).
    -   **Description**: A hierarchical visualization where each node represents a level in the CoRIx tree (Levels 2 through 5).
    -   **Node Appearance**: Each node will be represented as a rectangular shape displaying its aggregated CoRIx score (scaled 0-10). Node colors or sizes could optionally indicate score magnitude (e.g., redder/larger for higher risk).
    -   **Interactivity**:
        -   **Hover**: Display node name, level, construct, and score.
        -   **Depth Control (simulated expand/collapse)**: An `ipywidgets.IntSlider` or `ipywidgets.ToggleButtons` will control the maximum depth of the tree displayed, effectively simulating expanding/collapsing branches.
        -   **Click**: Clicking a node will trigger the `display_node_details` function to populate an `ipywidgets.Output` area with a detailed breakdown of contributing assessment items and their scores for that specific node.

2.  **Application and Scenario Selection Widgets**:
    -   **Type**: `ipywidgets.Dropdown`
    -   **Description**: Two dropdown menus allowing users to select an AI application (e.g., Application A, B, C) and a scenario (e.g., Pathfinder, TV Spoilers, Meal Planner).

3.  **Node Details Display Area**:
    -   **Type**: `ipywidgets.Output`
    -   **Description**: A dedicated area below the tree visualization that dynamically updates to show a structured breakdown (e.g., a simple HTML table or formatted markdown text) of the assessment items, questionnaire questions, or annotation categories that contribute to the score of a user-selected tree node. This will include their individual raw scores (for Level 5 children) or immediate child aggregated scores (for Level 2, 3, 4 parents).

## 3. Notebook Sections (in Detail)

### Section 1: Introduction to the ARIA CoRIx Tree Explorer

This notebook allows for an interactive exploration of the Contextual Robustness Index (CoRIx) measurement trees, as outlined in the NIST AI 700-2: ARIA 0.1 Pilot Evaluation Report [1]. CoRIx provides a transparent and tangible representation of how collected and assessed data is synthesized into meaningful metrics for evaluating AI system trustworthiness.

### Section 2: Learning Goals

This section reiterates the key learning objectives for this interactive notebook. By the end, you should be able to:
- Understand the hierarchical structure and aggregation logic of CoRIx measurement trees.
- Identify how different testing layers (model testing, red teaming, field testing) contribute to overall AI validity risk scores.
- Analyze the impact of annotator labels and user perceptions on the assessment of AI system trustworthiness.
- Interpret the meaning of CoRIx scores, where higher scores indicate greater negative risk.

### Section 3: Understanding the CoRIx Framework

The Contextual Robustness Index (CoRIx) is a multidimensional measurement instrument designed to capture the technical and contextual robustness of AI systems. A CoRIx tree visualizes how different assessment items and testing layers contribute to an overall validity risk score for an AI application in a specific scenario. Crucially, **a higher numeric CoRIx score indicates greater negative risk** to AI system validity. All scores are scaled from 0 to 10.

The tree structure progresses through several levels of detail:
-   **Level 2: Risks** (e.g., Validity/Reliability)
-   **Level 3: Testing Level** (e.g., Model Testing, Red Teaming, Field Testing)
-   **Level 4: Annotator Responses & User Perception** (e.g., Annotator Label, User Perception)
-   **Level 5: Response Collation** (specific assessment items/questionnaire questions, e.g., RA 2.1, DU 2)

This notebook focuses on visualizing Levels 2 through 5, consistent with the figures presented in the NIST ARIA 0.1 Pilot Evaluation Report.

### Section 4: Mathematical Foundation of CoRIx Aggregation

CoRIx scores are aggregated hierarchically using specific mathematical operations at each level. For a parent node $P$ with child nodes $C_1, C_2, \ldots, C_N$ and their respective scores $S_1, S_2, \ldots, S_N$, the parent's score $S_P$ is calculated as follows:

-   **Level 2 (Risks)**: The parent node score is the maximum of its children's scores. This means the highest risk from any testing layer dictates the overall risk at this level.
    $$ S_P = \max(S_1, S_2, \ldots, S_N) $$

-   **Level 3 (Testing Level)**: The parent node score is the mean (average) of its children's scores. This averages the contributions from annotator labels and user perceptions within a specific testing level.
    $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

-   **Level 4 (Annotator Responses & User Perception)**: The parent node score is the mean of its children's scores. This averages the specific assessment items or questionnaire questions that fall under a perception or annotation category.
    $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

-   **Level 5 (Response Collation)**: The scores at this level represent direct aggregated measures from raw annotator labels or questionnaire responses (Level 6, which are the leaf nodes and not explicitly visualized). For the purpose of this visualization, Level 5 nodes are treated as direct inputs to their Level 4 parents, and their "scores" are assumed to be pre-aggregated from raw responses. The aggregation for its hypothetical children (Level 6) would also be the mean.
    $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

These aggregation rules ensure that the CoRIx framework accurately reflects how risks propagate and combine across different evaluation layers.

### Section 5: Setting Up the Environment

Before proceeding, we need to import the necessary Python libraries. These libraries provide functionalities for data handling, numerical operations, interactive plotting, and user interface widgets within this Jupyter Notebook.

```python
# Code cell: Import required libraries
# import pandas
# import numpy
# import plotly.graph_objects as go
# import ipywidgets as widgets
# from IPython.display import display, HTML, clear_output
```

### Section 6: Dataset Preparation and Loading

The CoRIx Tree Explorer uses a synthetic dataset based on "Table 8. Example CoRIx output scores" from Appendix E of the NIST ARIA 0.1 Pilot Evaluation Report [1]. This dataset contains pre-computed CoRIx scores for different AI applications (Application A, B, C) across various scenarios (Pathfinder, TV Spoilers, Meal Planner). The data is structured to reflect Levels 2 through 5 of the CoRIx tree, including constructs like 'Validity/Reliability', 'Model Testing', 'Red Teaming', 'Field Testing', 'Annotator Label', 'User Perception', and detailed assessment items (e.g., RA 1, DU 2, CC 3, QQ 1.1).

The dataset `corix_scores.csv` will have the following columns: `Level`, `Construct`, `Application A - Pathfinder`, `Application B - TV Spoilers`, `Application C - Meal Planner`. The scores are scaled from 0 to 10.

```python
# Code cell: Define synthetic dataset (simulating corix_scores.csv) and save/load
# Data for corix_scores.csv will be created as a pandas DataFrame.
# It will explicitly contain rows and columns exactly as presented in Appendix E, Table 8 of the NIST report.
# For example:
# data = {
#     'Level': [2, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, ...],
#     'Construct': ['Validity/Reliability (V/R)', 'Model Testing (MT)', 'Red Teaming (RT)', 'Field Testing (FT)', 'MT Annotator Label', 'RT Annotator Label', 'RT User Perception', 'FT Annotator Label', 'FT User Perception', 'MT RA 1', 'MT RA 2', ...],
#     'Application A - Pathfinder': [2.88, 0.72, 2.88, 2.36, 0.72, 3.52, 2.24, 3.06, 1.67, 0.0, 0.0, ...],
#     'Application B - TV Spoilers': [4.29, 2.29, 3.55, 4.29, 2.29, 3.75, 3.34, 3.58, 5.00, 2.00, 0.0, ...],
#     'Application C - Meal Planner': [6.30, 6.30, 3.39, 2.80, 6.30, 3.74, 3.05, 3.56, 2.03, 9.00, 7.00, ...]
# }
# corix_df = pd.DataFrame(data)
# corix_df.to_csv('corix_scores.csv', index=False)
#
# loaded_df = load_corix_dataset('corix_scores.csv')
```

```python
# Code cell: Display the first few rows of the loaded dataset
# loaded_df.head()
```

### Section 7: Data Preprocessing: Building the Tree Structure

To visualize the hierarchical nature of CoRIx, the flat tabular data must be transformed into a tree-like data structure. This process involves identifying parent-child relationships between constructs based on their `Level` and `Construct` names. The `build_corix_tree_data` function will take the raw DataFrame and assemble a structured representation where each node can be linked to its parent and children, with scores aggregated according to the rules defined in Section 4.

```python
# Code cell: Definition of build_corix_tree_data function (pseudocode concept)
# def build_corix_tree_data(dataframe, application, scenario):
#     # Select relevant application/scenario column
#     # Define node structure (id, name, parent_id, score, level, construct, children_ids, raw_assessment_items)
#     # Iterate through levels (e.g., 2 to 5) to establish hierarchy
#     # Assign scores from the dataframe to Level 5 nodes
#     # Aggregate scores upwards using aggregate_node_score for Levels 4, 3, 2
#     # Return the root node or a dictionary of all nodes
```

```python
# Code cell: Execute build_corix_tree_data for an initial application/scenario
# initial_app = "Application A"
# initial_scenario = "Pathfinder"
# corix_tree_structure = build_corix_tree_data(loaded_df, initial_app, initial_scenario)
```

### Section 8: Understanding Node Details

A key feature of the CoRIx Tree Explorer is the ability to inspect the details contributing to a node's score. When a node in the tree visualization is "clicked," the `display_node_details` function will retrieve and present a clear breakdown of the specific assessment items, questionnaire questions, or annotation categories that contribute to that node's aggregated score. This helps in understanding the granular elements driving the overall risk assessment at each level.

```python
# Code cell: Definition of display_node_details function (pseudocode concept)
# def display_node_details(tree_data, node_id):
#     # Retrieve node information from tree_data based on node_id
#     # If node is Level 2, 3, or 4: list its children and their scores.
#     # If node is Level 5: list the raw assessment items/questionnaire questions that it represents and their (implied) scores.
#     # Format the output clearly (e.g., using Markdown or HTML for ipywidgets.Output)
#     # Return ipywidgets.Output containing the formatted details
```

### Section 9: Interactive CoRIx Tree Visualization Function

This section outlines the core visualization function `create_interactive_corix_tree_plot`. This function will utilize `plotly.graph_objects` to render a dynamic node-link diagram of the CoRIx tree. The visualization will be interactive, allowing users to hover over nodes for basic information and to interact with a depth slider to control the visible levels of the tree.

```python
# Code cell: Definition of create_interactive_corix_tree_plot function (pseudocode concept)
# def create_interactive_corix_tree_plot(tree_data, max_depth_to_display=5):
#     fig = go.Figure()
#
#     # Initialize lists for node coordinates, text, and connections
#     node_x = []
#     node_y = []
#     node_labels = []
#     edge_x = []
#     edge_y = []
#
#     # Implement a hierarchical layout algorithm (e.g., breadth-first traversal to assign x, y coordinates)
#     # Iterate through tree_data to add nodes (as go.Scatter markers) and edges (as go.Scatter lines)
#     # Only add nodes up to max_depth_to_display
#
#     # Node rendering:
#     # Each node marker will be a square or circle.
#     # Text labels will display the node's score (e.g., "Score: X.XX/10").
#     # Hover text will show full construct name, level, and score.
#
#     # Edge rendering:
#     # Lines connecting parent to child nodes.
#
#     # Configure layout (e.g., disable zoom, fix aspect ratio)
#     # fig.update_layout(showlegend=False, hovermode='closest', ...)
#
#     # Add click event handler for displaying node details
#     # fig.data[0].on_click(lambda trace, points, state: on_node_click(trace, points, state, tree_data, output_widget))
#
#     return fig
```

### Section 10: Application and Scenario Selection

Users will interact with the CoRIx Tree Explorer using dropdown widgets to select their desired AI application and scenario combination. This selection will dynamically update the displayed CoRIx tree and its associated details.

```python
# Code cell: Define dropdown widgets for application and scenario selection
# app_dropdown = widgets.Dropdown(
#     options=list(loaded_df.columns[2:]), # Column names like 'Application A - Pathfinder'
#     description='Select Application/Scenario:'
# )
#
# # Optional: A second dropdown for scenario only if applications had multiple scenarios.
# # For now, we'll assume the app_dropdown covers 'Application X - Scenario Y' combinations.
#
# # Slider for controlling tree depth
# depth_slider = widgets.IntSlider(
#     value=5, min=2, max=5, step=1,
#     description='Max Tree Depth:',
#     continuous_update=False
# )
#
# # Output widget for displaying the plot
# plot_output = widgets.Output()
#
# # Output widget for displaying node details
# details_output = widgets.Output()
#
# # Link dropdowns and slider to the update function
# # app_dropdown.observe(on_selection_change, names='value')
# # depth_slider.observe(on_selection_change, names='value')
#
# # Initial display of widgets
# # display(widgets.VBox([app_dropdown, depth_slider, plot_output, details_output]))
```

### Section 11: Displaying the Interactive CoRIx Tree for Application A / Pathfinder

Let's begin by examining "Application A / Pathfinder". The report indicates an overall CoRIx score of 2.88, suggesting lower validity risks for this combination. We will generate and interpret the interactive tree visualization for this initial selection.

```python
# Code cell: Set initial selection and display the plot
# Set app_dropdown.value to "Application A - Pathfinder"
# Trigger on_selection_change to display the plot
# with plot_output:
#     display(create_interactive_corix_tree_plot(corix_tree_structure, depth_slider.value))
```

The visualization for "Application A / Pathfinder" shows an overall CoRIx score of $2.88$. This relatively low score suggests a lower observed risk to validity for this application and scenario combination. Tracing down to Level 3, Red Teaming (score of $2.88$) contributes the most to the overall risk compared to Model Testing ($0.72$) and Field Testing ($2.36$). Further investigation at Level 4 reveals that Annotator Labels (score of $3.52$) identified higher risks during Red Teaming than User Perceptions (score of $2.24$). Delving into Level 5 reveals specific constructs like `RT DD 4` (Red Teaming Dialogue Dynamics 4, unnatural dialogue) with a score of $4.98$ and `FT CC 3` (Field Testing Content Characterization 3, superfluous information) with a score of $7.41$ contributed to higher individual risks.

### Section 12: Exploring Application B / TV Spoilers

Next, we explore "Application B / TV Spoilers". The report notes an overall score of 4.29 for this application-scenario, signaling a moderate potential for validity risk. Observe how the tree structure and score distribution differ from Application A.

```python
# Code cell: Update selection to "Application B - TV Spoilers" and display the plot
# app_dropdown.value = "Application B - TV Spoilers"
# (on_selection_change will automatically update the plot_output)
```

For "Application B / TV Spoilers", the overall CoRIx score is $4.29$, indicating a moderate validity risk. Field Testing (score of $4.29$) contributes most significantly at Level 3, followed by Red Teaming ($3.55$) and Model Testing ($2.29$). At Level 4, Field Tester Perceptions (score of $5.00$) were the primary source of risk compared to Annotator Labels ($3.58$) during field testing. Level 5 reveals high scores from `RT RA 2.1` (Red Teaming Risk Assessment 2.1, guardrail violation) at $5.40$ and `FT CC 3` (Field Testing Content Characterization 3, superfluous information) at $7.42$. This suggests that for this application, field testers perceived more issues, potentially related to guardrail violations and the presence of superfluous information.

### Section 13: Exploring Application C / Meal Planner

Finally, we will analyze "Application C / Meal Planner". This application-scenario combination exhibited the highest overall CoRIx score of 6.30 in the pilot, suggesting a higher level of validity risk.

```python
# Code cell: Update selection to "Application C - Meal Planner" and display the plot
# app_dropdown.value = "Application C - Meal Planner"
# (on_selection_change will automatically update the plot_output)
```

"Application C / Meal Planner" shows the highest overall CoRIx score of $6.30$, indicating the greatest validity risk among the pilot examples. Notably, Model Testing (score of $6.30$) shows the highest risk at Level 3, with Red Teaming ($3.39$) and Field Testing ($2.80$) contributing less. At Level 4, Model Testing Annotator Labels ($6.30$) scored highest. Further breakdown in Level 5 reveals extremely high scores for `MT RA 1` (Model Testing Risk Assessment 1, general functionality) at $9.00$ and `MT RA 2` (Model Testing Risk Assessment 2, response quality) at $7.00$, along with `FT CC 3` (Field Testing Content Characterization 3, superfluous information) at $7.42$. This indicates significant issues with basic functionality and response quality observed during model testing, along with superfluous information in field testing.

### Section 14: Interpreting CoRIx Scores and Hierarchical Contribution

Throughout this exploration, remember that **a higher numeric CoRIx score signifies greater negative risk to validity**.

The hierarchical structure of the CoRIx trees allows for a nuanced understanding of AI system validity risk:
-   **Overall Score (Level 2)**: Provides a high-level summary of the validity risk.
-   **Testing Layers (Level 3)**: Breaks down the overall risk into contributions from different testing methodologies (Model Testing, Red Teaming, Field Testing). This helps identify *where* the risks are most apparent.
-   **Perception Layers (Level 4)**: Differentiates between risks identified by expert annotators (`Annotator Label`) and those perceived by human users (`User Perception`), offering insights into different perspectives on AI performance.
-   **Specific Constructs (Level 5)**: Pinpoints the exact assessment items or questionnaire questions that are driving the risks, enabling developers to target specific areas for improvement.

By interactively navigating these trees, users can gain a deeper understanding of how various factors contribute to the overall trustworthiness and validity of AI systems.

### Section 15: Conclusion and References

This Jupyter Notebook has provided an interactive tool to explore CoRIx measurement trees, enhancing the understanding of how AI validity risk is assessed through various testing layers and aggregation logic. By visualizing and interpreting CoRIx scores, we gain insights into the contextual robustness of AI systems as defined by NIST. This transparent approach facilitates the identification of specific areas for AI system improvement.

**References:**

[1] Section 5.1: Contextual Robustness Index (CoRIx) & Section 5.2: Pilot Measurement Results, NIST AI 700-2: Assessing Risks and Impacts of AI (ARIA) ARIA 0.1: Pilot Evaluation Report, https://doi.org/10.6028/NIST.AI.700-2.
