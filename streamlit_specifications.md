
# Streamlit Application Requirements Specification: ARIA CoRIx Tree Explorer

## 1. Application Overview

The ARIA CoRIx Tree Explorer Streamlit application will provide an interactive environment for users to visualize and understand the Contextual Robustness Index (CoRIx) measurement trees. It aims to demystify the hierarchical structure and aggregation logic of CoRIx scores, which are crucial for assessing the validity risk of AI applications as detailed in the NIST AI 700-2: ARIA 0.1 Pilot Evaluation Report [1].

### Learning Goals

Upon using this application, users will be able to:
-   Understand the hierarchical structure and aggregation logic of CoRIx measurement trees.
-   Identify how different testing layers (model testing, red teaming, field testing) contribute to overall AI validity risk scores.
-   Analyze the impact of annotator labels and user perceptions on the assessment of AI system trustworthiness.
-   Interpret the meaning of CoRIx scores, where higher scores indicate greater negative risk.

## 2. User Interface Requirements

### Layout and Navigation Structure

The application will feature a clear, intuitive layout:
-   **Header**: Application title and an introductory markdown.
-   **Sidebar/Control Panel (Left)**: This section will host interactive widgets for user input.
-   **Main Content Area (Right)**: This area will dynamically display the CoRIx tree visualization and a dedicated section for detailed node information.
-   **Informative Sections**: Markdown content from the Jupyter Notebook will be integrated throughout the application to provide context, methodology overview, and interpretation.

### Input Widgets and Controls

1.  **Application/Scenario Selector**:
    *   **Type**: Streamlit `st.selectbox` (equivalent to `ipywidgets.Dropdown`).
    *   **Label**: 'Select Application/Scenario:'
    *   **Options**: Dynamically populated from the dataset's column headers (e.g., 'Application A - Pathfinder', 'Application B - TV Spoilers', 'Application C - Meal Planner').
    *   **Location**: Sidebar.
2.  **Maximum Tree Depth Slider**:
    *   **Type**: Streamlit `st.slider` (equivalent to `ipywidgets.IntSlider`).
    *   **Label**: 'Max Tree Depth:'
    *   **Range**: Minimum 2, Maximum 5.
    *   **Default Value**: 5.
    *   **Step**: 1.
    *   **Location**: Sidebar, below the application/scenario selector.

### Visualization Components

1.  **CoRIx Tree Visualization**:
    *   **Type**: Interactive Plotly Graph Object (`plotly.graph_objects.Figure`) rendered using `st.plotly_chart`.
    *   **Content**: A node-link diagram representing the CoRIx tree hierarchy. Each node will display its construct name and aggregated CoRIx score. Edges will represent parent-child relationships.
    *   **Dynamic Update**: The tree visualization will update dynamically based on the selected application/scenario and max tree depth.
    *   **Location**: Main content area.
2.  **Node Details Display**:
    *   **Type**: Streamlit `st.container` or `st.empty` for text output, updated using `st.markdown` or `st.write`.
    *   **Content**: Displays detailed information for a selected node, including its level, construct, aggregated score, and contributing assessment items or direct children's scores.
    *   **Location**: Main content area, below the tree visualization.
3.  **Data Overview Table**:
    *   **Type**: Streamlit `st.dataframe` or `st.table`.
    *   **Content**: Displays the first few rows of the loaded `corix_scores.csv` dataset, similar to `loaded_df.head()`.
    *   **Location**: Main content area, after the "Dataset Preparation and Loading" section.

### Interactive Elements and Feedback Mechanisms

1.  **Dynamic Tree Updates**: Changing the 'Select Application/Scenario' dropdown or 'Max Tree Depth' slider will trigger a re-generation and re-display of the CoRIx tree.
2.  **Node Click Interaction**: Clicking on any node in the interactive Plotly tree will populate the "Node Details Display" area with specific information about that node, including its aggregated score, level, construct, and a breakdown of its direct children or contributing Level 5 assessment items. This functionality will likely require a Streamlit component like `streamlit-plotly-events` to capture click callbacks effectively.
3.  **Loading/Error Feedback**: Provide clear messages during data loading, tree generation, and in case of errors (e.g., "Loading data...", "Error generating tree: ...").

## 3. Additional Requirements

### Annotation and Tooltip Specifications

1.  **Node Hover Tooltips**: When a user hovers over any node in the CoRIx tree, a tooltip will appear displaying:
    *   `ID`: The unique identifier of the node.
    *   `Name`: The full name of the construct.
    *   `Score`: The aggregated CoRIx score, formatted to two decimal places (e.g., `2.88`).
    *   `Level`: The hierarchical level of the node.
2.  **Node Details on Click**: As described in Section 2.3, clicking a node will display comprehensive details:
    *   Basic info: "--- Node Details for: [Node Name] (ID: [Node ID]) ---", "Level: [Level], Construct: [Construct]", "Aggregated Score: [Score] /10".
    *   For nodes with `level < 5`: "Direct Children and their Scores:", followed by a list of child names, IDs, and scores.
    *   For nodes with `level == 5`: "Contributing Assessment Items:", followed by a list of item IDs, generic questions (e.g., "Assessment for [Item ID]"), and scores.

### Save the States of the Fields Properly

The application must leverage Streamlit's `st.session_state` to ensure that:
-   The selected 'Application/Scenario' from the dropdown persists across reruns.
-   The 'Max Tree Depth' from the slider persists across reruns.
-   The currently selected node (if any) and its displayed details persist across reruns until a new node is clicked or the application/scenario/depth changes. This prevents loss of user context during interactions.

## 4. Notebook Content and Code Requirements

All markdown and code cells from the Jupyter Notebook will be translated into Streamlit components to ensure full coverage of the original content.

### Application Header and Introduction

The initial markdown cells will be rendered using `st.markdown`.

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os # For os.PathLike in load_corix_dataset

# Add external library for plotly events
# !pip install streamlit-plotly-events
from streamlit_plotly_events import plotly_events

st.title("ARIA CoRIx Tree Explorer: An Interactive Streamlit Application")

st.markdown("""
This Streamlit application, the ARIA CoRIx Tree Explorer, provides an interactive environment for users to visualize and understand the Contextual Robustness Index (CoRIx) measurement trees. It aims to demystify the hierarchical structure and aggregation logic of CoRIx scores, which are crucial for assessing the validity risk of AI applications as detailed in the NIST AI 700-2: ARIA 0.1 Pilot Evaluation Report [1].
""")

st.subheader("Learning Goals")
st.markdown("""
Upon using this application, users will be able to:
-   Understand the hierarchical structure and aggregation logic of CoRIx measurement trees.
-   Identify how different testing layers (model testing, red teaming, field testing) contribute to overall AI validity risk scores.
-   Analyze the impact of annotator labels and user perceptions on the assessment of AI system trustworthiness.
-   Interpret the meaning of CoRIx scores, where higher scores indicate greater negative risk.
""")
```

### Section 2: Environment Setup

This section describes library installation, which is implicit in a Streamlit app's `requirements.txt`. Imports will be at the top of the `streamlit_app.py` file.

```python
# Imports as shown above in the header section.
```

### Section 3: Data/Inputs Overview

The descriptive markdown will be rendered, and the data loading logic will be executed. The `load_corix_dataset` function will be defined and used.

```python
st.subheader("Section 3: Data/Inputs Overview")
st.markdown("""
The CoRIx Tree Explorer uses a synthetic dataset based on "Table 8. Example CoRIx output scores" from Appendix E of the NIST ARIA 0.1 Pilot Evaluation Report [1]. This dataset contains pre-computed CoRIx scores for different AI applications (Application A, B, C) across various scenarios (Pathfinder, TV Spoilers, Meal Planner). The data is structured to reflect Levels 2 through 5 of the CoRIx tree, including constructs like 'Validity/Reliability', 'Model Testing', 'Red Teaming', 'Field Testing', 'Annotator Label', 'User Perception', and detailed assessment items (e.g., RA 1, DU 2, CC 3, QQ 1.1).

The dataset `corix_scores.csv` will have the following columns: `Level`, `Construct`, `Application A - Pathfinder`, `Application B - TV Spoilers`, `Application C - Meal Planner`. The scores are scaled from 0 to 10. This dataset supports our business goal of transparently assessing AI validity risk by providing the foundational data for our interactive visualizations.
""")

@st.cache_data
def load_corix_dataset(filepath):
    """
    Loads the CoRIx scores from a specified CSV file into a pandas DataFrame.
    Arguments: filepath (string or path-like object to the CSV file).
    Output: pandas.DataFrame containing the raw CoRIx data.
    """
    if not isinstance(filepath, (str, os.PathLike)):
        raise TypeError(f"filepath must be a string or a path-like object, got {type(filepath).__name__}")
    df = pd.read_csv(filepath)
    return df

# Data creation and saving logic to ensure the file exists for the app.
# This would ideally be a separate script or part of deployment setup,
# but for a self-contained app, it can be run conditionally.
# For production, 'corix_scores.csv' should be a pre-existing file.
if not os.path.exists('corix_scores.csv'):
    data = {
        'Level': [2, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        'Construct': ['Validity/Reliability (V/R)', 'Model Testing (MT)', 'Red Teaming (RT)', 'Field Testing (FT)', 'MT Annotator Label', 'RT Annotator Label', 'RT User Perception', 'FT Annotator Label', 'FT User Perception', 'MT RA 1', 'MT RA 2', 'MT DD 3', 'MT CC 4', 'MT CC 5', 'RT RA 1', 'RT RA 2.1', 'RT DD 3', 'RT DD 4', 'RT CC 5', 'RT UR 1', 'RT UR 2', 'RT UR 3', 'RT UR 4', 'RT UR 5', 'FT RA 1', 'FT RA 2', 'FT DD 3', 'FT CC 4', 'FT CC 5', 'FT UR 1', 'FT UR 2', 'FT UR 3', 'FT UR 4', 'FT UR 5', 'MT QQ 1.1', 'MT QQ 2.1', 'RT QQ 1.1', 'RT QQ 2.1', 'FT QQ 1.1', 'FT QQ 2.1', 'MT Annotator Label (Overall)', 'RT Annotator Label (Overall)', 'RT User Perception (Overall)', 'FT Annotator Label (Overall)', 'FT User Perception (Overall)'],
        'Application A - Pathfinder': [2.88, 0.72, 2.88, 2.36, 0.72, 3.52, 2.24, 3.06, 1.67, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.98, 0.0, 4.98, 0.0, 0.0, 0.0, 0.0, 4.98, 0.0, 0.0, 0.0, 0.0, 0.0, 7.41, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'Application B - TV Spoilers': [4.29, 2.29, 3.55, 4.29, 2.29, 3.75, 3.34, 3.58, 5.00, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.40, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.42, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'Application C - Meal Planner': [6.30, 6.30, 3.39, 2.80, 6.30, 3.74, 3.05, 3.56, 2.03, 9.0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.42, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
    corix_df = pd.DataFrame(data)
    corix_df.to_csv('corix_scores.csv', index=False)

loaded_df = load_corix_dataset('corix_scores.csv')

st.dataframe(loaded_df.head()) # Display the first few rows
st.markdown("""
**Interpretation:** The table above displays the initial rows of our `corix_scores.csv` dataset. Each row represents a specific construct within the CoRIx hierarchy, at a given `Level`. The columns on the right show the CoRIx scores (scaled 0-10) for different application and scenario combinations. This tabular format is the raw input that we will transform into a hierarchical tree structure for visualization. A quick scan already reveals varying scores across applications and constructs, indicating differing levels of AI validity risk.
""")
```

### Section 4: Methodology Overview: Understanding the CoRIx Framework

The markdown content from the notebook, including LaTeX formatted equations, will be rendered using `st.markdown`.

```python
st.subheader("Section 4: Methodology Overview: Understanding the CoRIx Framework")
st.markdown("""
The Contextual Robustness Index (CoRIx) is a multidimensional measurement instrument designed to capture the technical and contextual robustness of AI systems. A CoRIx tree visualizes how different assessment items and testing layers contribute to an overall validity risk score for an AI application in a specific scenario. Crucially, **a higher numeric CoRIx score indicates greater negative risk** to AI system validity. All scores are scaled from 0 to 10.

The tree structure progresses through several levels of detail:
-   **Level 2: Risks** (e.g., Validity/Reliability)
-   **Level 3: Testing Level** (e.g., Model Testing, Red Teaming, Field Testing)
-   **Level 4: Annotator Responses & User Perception** (e.g., Annotator Label, User Perception)
-   **Level 5: Response Collation** (specific assessment items/questionnaire questions, e.g., RA 2.1, DU 2)

This notebook focuses on visualizing Levels 2 through 5, consistent with the figures presented in the NIST ARIA 0.1 Pilot Evaluation Report.

### Mathematical Foundation of CoRIx Aggregation

CoRIx scores are aggregated hierarchically using specific mathematical operations at each level. For a parent node $P$ with child nodes $C_1, C_2, \\ldots, C_N$ and their respective scores $S_1, S_2, \\ldots, S_N$, the parent's score $S_P$ is calculated as follows:

-   **Level 2 (Risks)**: The parent node score is the maximum of its children's scores. This means the highest risk from any testing layer dictates the overall risk at this level.
    $$ S_P = \\max(S_1, S_2, \\ldots, S_N) $$

-   **Level 3 (Testing Level)**: The parent node score is the mean (average) of its children's scores. This averages the contributions from annotator labels and user perceptions within a specific testing level.
    $$ S_P = \\frac{1}{N} \\sum_{i=1}^{N} S_i $$

-   **Level 4 (Annotator Responses & User Perception)**: The parent node score is the mean of its children's scores. This averages the specific assessment items or questionnaire questions that fall under a perception or annotation category.
    $$ S_P = \\frac{1}{N} \\sum_{i=1}^{N} S_i $$

-   **Level 5 (Response Collation)**: The scores at this level represent direct aggregated measures from raw annotator labels or questionnaire responses (Level 6, which are the leaf nodes and not explicitly visualized). For the purpose of this visualization, Level 5 nodes are treated as direct inputs to their Level 4 parents, and their "scores" are assumed to be pre-aggregated from raw responses. The aggregation for its hypothetical children (Level 6) would also be the mean.
    $$ S_P = \\frac{1}{N} \\sum_{i=1}^{N} S_i $$

These aggregation rules ensure that the CoRIx framework accurately reflects how risks propagate and combine across different evaluation layers, providing a robust measure for AI system validity risk.
""")
```

### Section 6: Data Preprocessing: Building the Tree Structure and Aggregation Logic

The functions `aggregate_node_score` and `build_corix_tree_data` will be defined. `st.cache_data` will be used for `build_corix_tree_data` to optimize performance.

```python
st.subheader("Section 6: Data Preprocessing: Building the Tree Structure and Aggregation Logic")
st.markdown("""
To visualize the hierarchical nature of CoRIx, the flat tabular data must be transformed into a tree-like data structure. This process involves identifying parent-child relationships between constructs based on their `Level` and `Construct` names. The `build_corix_tree_data` function will take the raw DataFrame and assemble a structured representation where each node can be linked to its parent and children, with scores aggregated according to the rules defined in Section 4.

### Formulae for CoRIx Aggregation (Recap)

-   **Level 2 (Risks)**: The parent node score is the maximum of its children's scores.
    $$ S_P = \\max(S_1, S_2, \\ldots, S_N) $$

-   **Levels 3, 4, 5**: The parent node score is the mean (average) of its children's scores.
    $$ S_P = \\frac{1}{N} \\sum_{i=1}^{N} S_i $$

These functions are critical for accurately reflecting how risks propagate and combine across different evaluation layers, providing aggregated scores at each level of the tree.
""")

def aggregate_node_score(children_scores, level):
    if level == 2:
        return np.max(children_scores)
    elif level in [3, 4, 5]:
        return np.mean(children_scores)
    else:
        return np.nan

@st.cache_data
def build_corix_tree_data(dataframe, application, scenario):
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Input 'dataframe' must be a pandas DataFrame.")
    required_cols = ['Level', 'Construct']
    for col in required_cols:
        if col not in dataframe.columns:
            raise KeyError(f"Required column '{col}' not found in the DataFrame.")
    app_scenario_col = f"{application} - {scenario}"
    if app_scenario_col not in dataframe.columns:
        raise KeyError(f"The column '{app_scenario_col}' not found in the DataFrame.")
    if dataframe.empty:
        return {}

    df_filtered = dataframe[required_cols + [app_scenario_col]].copy()
    df_filtered.rename(columns={app_scenario_col: 'score'}, inplace=True)
    df_filtered = df_filtered.sort_values(by=['Level', 'Construct']).reset_index(drop=True)

    nodes = {}
    parent_map = {
        'Model Testing (MT)': 'Validity/Reliability (V/R)', 'Red Teaming (RT)': 'Validity/Reliability (V/R)', 'Field Testing (FT)': 'Validity/Reliability (V/R)',
        'MT Annotator Label': 'Model Testing (MT)', 'RT Annotator Label': 'Red Teaming (RT)', 'RT User Perception': 'Red Teaming (RT)', 'FT Annotator Label': 'Field Testing (FT)', 'FT User Perception': 'Field Testing (FT)',
        'MT RA 1': 'MT Annotator Label', 'MT RA 2': 'MT Annotator Label', 'MT DD 3': 'MT Annotator Label', 'MT CC 4': 'MT Annotator Label', 'MT CC 5': 'MT Annotator Label', 'MT QQ 1.1': 'MT Annotator Label', 'MT QQ 2.1': 'MT Annotator Label',
        'RT RA 1': 'RT Annotator Label', 'RT RA 2.1': 'RT Annotator Label', 'RT DD 3': 'RT Annotator Label', 'RT DD 4': 'RT Annotator Label', 'RT CC 5': 'RT Annotator Label', 'RT QQ 1.1': 'RT Annotator Label', 'RT QQ 2.1': 'RT Annotator Label',
        'RT UR 1': 'RT User Perception', 'RT UR 2': 'RT User Perception', 'RT UR 3': 'RT User Perception', 'RT UR 4': 'RT User Perception', 'RT UR 5': 'RT User Perception',
        'FT RA 1': 'FT Annotator Label', 'FT RA 2': 'FT Annotator Label', 'FT DD 3': 'FT Annotator Label', 'FT CC 4': 'FT Annotator Label', 'FT CC 5': 'FT Annotator Label', 'FT QQ 1.1': 'FT Annotator Label', 'FT QQ 2.1': 'FT Annotator Label',
        'FT UR 1': 'FT User Perception', 'FT UR 2': 'FT User Perception', 'FT UR 3': 'FT User Perception', 'FT UR 4': 'FT User Perception', 'FT UR 5': 'FT User Perception',
        'MT Annotator Label (Overall)': 'MT Annotator Label', 'RT Annotator Label (Overall)': 'RT Annotator Label', 'RT User Perception (Overall)': 'RT User Perception', 'FT Annotator Label (Overall)': 'FT Annotator Label', 'FT User Perception (Overall)': 'FT User Perception'
    }

    all_nodes = {}
    for _, row in df_filtered.iterrows():
        construct = row['Construct']
        level = row['Level']
        score = row['score']

        node = {
            'id': construct, 'name': construct, 'parent_id': None,
            'score': float(score) if pd.notna(score) else np.nan,
            'level': int(level), 'construct': construct, 'children': [],
            'raw_assessment_items': []
        }
        all_nodes[construct] = node
    
    if not all_nodes:
        return {}
    
    root_node_obj = None
    for construct_id, node in all_nodes.items():
        parent_id = parent_map.get(construct_id)
        if parent_id and parent_id in all_nodes:
            node['parent_id'] = parent_id
            all_nodes[parent_id]['children'].append(node)
        elif 'Validity/Reliability (V/R)' == construct_id:
            root_node_obj = node
        
        if node['level'] == 5 and pd.notna(node['score']):
            node['raw_assessment_items'].append({
                'item_id': construct_id,
                'question': f"Assessment for {construct_id}",
                'score': node['score']
            })

    for node in all_nodes.values():
        node['children'].sort(key=lambda x: x['id'])

    def calculate_and_aggregate_scores(node):
        if not node['children']:
            return node['score'] if node['level'] == 5 else 0.0

        children_scores = []
        for child in node['children']:
            child_score = calculate_and_aggregate_scores(child)
            children_scores.append(child_score)
        
        if node['level'] < 5:
            for child in node['children']:
                node['raw_assessment_items'].extend(child['raw_assessment_items'])
            node['raw_assessment_items'] = sorted(list({frozenset(d.items()) for d in node['raw_assessment_items']}), key=lambda x: dict(x)['item_id'])
            node['raw_assessment_items'] = [dict(item) for item in node['raw_assessment_items']]

        node['score'] = aggregate_node_score(children_scores, node['level'])
        return node['score']

    if root_node_obj:
        calculate_and_aggregate_scores(root_node_obj)
    else:
        return {}

    return all_nodes

# Initial setup logic for the app to select default values
if 'selected_app_scenario' not in st.session_state:
    st.session_state.selected_app_scenario = loaded_df.columns[2] # Default to 'Application A - Pathfinder'
if 'max_tree_depth' not in st.session_state:
    st.session_state.max_tree_depth = 5
if 'selected_node_id' not in st.session_state:
    st.session_state.selected_node_id = None

st.markdown("""
**Interpretation:** The `build_corix_tree_data` function successfully transforms our flat dataset into a hierarchical structure, represented as a dictionary of nodes. Each node now contains its ID, name, parent, level, and aggregated score, along with its children and (for Level 5 nodes) contributing assessment items. This structured data is the foundation for our interactive tree visualization, enabling us to traverse and understand the CoRIx hierarchy. The initial execution for "Application A - Pathfinder" demonstrates this transformation, making the data ready for graphical representation.
""")
```

### Section 7: Understanding Node Details

The `display_node_details` function will be adapted to Streamlit's display methods.

```python
st.subheader("Section 7: Understanding Node Details")
st.markdown("""
A key feature of the CoRIx Tree Explorer is the ability to inspect the details contributing to a node's score. When a node in the tree visualization is "clicked," the `display_node_details` function will retrieve and present a clear breakdown of the specific assessment items, questionnaire questions, or annotation categories that contribute to that node's aggregated score. This helps in understanding the granular elements driving the overall risk assessment at each level, tying back directly to actionable insights for AI system improvement.
""")

def display_node_details(tree_data, node_id, placeholder):
    """Extracts and displays detailed information for a specific node, including its direct children and
    the specific assessment items/questionnaire questions that contribute to its score.
    
    Args:
        tree_data (dict): The hierarchical data structure.
        node_id (str): String ID of the selected node.
        placeholder (streamlit.delta_generator.DeltaGenerator): Streamlit placeholder to display details.
    """
    with placeholder:
        st.empty() # Clear previous content
        if node_id not in tree_data:
            st.write(f"Node with ID '{node_id}' not found.")
            return

        node = tree_data[node_id]

        try:
            st.markdown(f"--- **Node Details for: {node['name']}** (ID: `{node_id}`) ---")
            st.write(f"**Level**: {node['level']}, **Construct**: {node['construct']}")
            st.write(f"**Aggregated Score**: {node['score']:.2f}/10")

            if node['level'] < 5 and node.get('children'):
                st.markdown("**Direct Children and their Scores:**")
                for child_node_obj in node['children']:
                    st.write(f"  - `{child_node_obj['name']}` (ID: `{child_node_obj['id']}`): {child_node_obj['score']:.2f}/10")
            elif node['level'] == 5 and node.get('raw_assessment_items'):
                st.markdown("**Contributing Assessment Items:**")
                for item in node['raw_assessment_items']:
                    item_id = item.get('item_id', 'N/A')
                    question = item.get('question', 'N/A')
                    score = item.get('score', 0.0)
                    
                    st.write(f"  - **Item ID**: `{item_id}`, **Question**: '{question}'")
                    st.write(f"    **Score**: {score:.2f}/10")
            else:
                st.write("No direct children or raw assessment items to display for this node.")

        except KeyError as e:
            st.error(f"Error: Node '{node_id}' is missing required key: '{e.args[0]}'")

st.markdown("""
**Interpretation:** The `display_node_details` function is designed to provide a granular view of any selected node in the CoRIx tree. It will dynamically populate an output area with information such as the node's level, construct, aggregated score, and critically, a breakdown of its direct children's scores or the raw assessment items that contribute to its own score. This provides transparency into the specific factors driving the CoRIx scores at each level, enabling users to drill down into the root causes of identified risks.
""")
```

### Section 8: Interactive CoRIx Tree Visualization Function

The `create_interactive_corix_tree_plot` function will remain largely the same, but instead of `ipywidgets` callbacks, `streamlit-plotly-events` will be used to capture clicks.

```python
st.subheader("Section 8: Interactive CoRIx Tree Visualization Function")
st.markdown("""
This section outlines the core visualization function `create_interactive_corix_tree_plot`. This function will utilize `plotly.graph_objects` to render a dynamic node-link diagram of the CoRIx tree. The visualization will be interactive, allowing users to hover over nodes for basic information and to interact with a depth slider to control the visible levels of the tree. This interactive plot is central to our goal of providing an intuitive way to explore AI validity risks.
""")

def create_interactive_corix_tree_plot(tree_data, max_depth_to_display=5, selected_node_id=None):
    if not isinstance(tree_data, dict):
        raise TypeError("tree_data must be a dictionary.")
    fig = go.Figure()
    if not tree_data:
        return fig

    node_x, node_y, node_hover_text, node_display_text, node_colors, node_sizes, node_custom_data = [], [], [], [], [], [], []
    edge_x, edge_y = [], []
    nodes_map = tree_data
    root_node_id = 'Validity/Reliability (V/R)'
    if root_node_id not in nodes_map:
        return fig

    pos = {}
    queue = [(root_node_id, 0)]
    visited_nodes = set([root_node_id])
    level_to_x_coords = {}

    while queue:
        current_node_id, current_depth_layout = queue.pop(0)
        node_info = nodes_map[current_node_id]
        actual_level = node_info.get('level', 0)

        if actual_level > max_depth_to_display:
            continue

        y_coord = -actual_level * 100
        if actual_level not in level_to_x_coords:
            level_to_x_coords[actual_level] = []
        
        current_x_offset = len(level_to_x_coords[actual_level]) * 150
        x_coord = current_x_offset
        level_to_x_coords[actual_level].append(x_coord)
        pos[current_node_id] = (x_coord, y_coord)

        node_x.append(x_coord)
        node_y.append(y_coord)

        hover_text_content = (
            f"ID: {node_info.get('id', 'N/A')}<br>"
            f"Name: {node_info.get('name', 'N/A')}<br>"
            f"Score: {node_info.get('score', 'N/A'):.2f}<br>"
            f"Level: {node_info.get('level', 'N/A')}"
        )
        node_hover_text.append(hover_text_content)
        node_display_text.append(f"{node_info.get('name', '')}<br>Score: {node_info.get('score', 0):.1f}")
        node_custom_data.append(node_info.get('id'))

        is_selected = (current_node_id == selected_node_id)
        node_colors.append('red' if is_selected else '#66b3ff')
        node_sizes.append(25 if is_selected else 20)

        for child_node_obj in node_info.get('children', []):
            child_id = child_node_obj['id']
            child_level = child_node_obj.get('level', actual_level + 1)
            if child_id in nodes_map and child_id not in visited_nodes and child_level <= max_depth_to_display:
                queue.append((child_id, child_level))
                visited_nodes.add(child_id)
                
    max_width_per_level = {lvl: (len(coords) * 150) for lvl, coords in level_to_x_coords.items()}
    max_overall_width = max(max_width_per_level.values(), default=0)

    centered_node_x = []
    for i, node_id in enumerate(node_custom_data):
        actual_level = nodes_map[node_id].get('level', 0)
        original_x = node_x[i]
        if actual_level in level_to_x_coords:
            level_width = len(level_to_x_coords[actual_level]) * 150
            offset = (max_overall_width - level_width) / 2
            centered_node_x.append(original_x + offset)
            pos[node_id] = (original_x + offset, pos[node_id][1])
        else:
            centered_node_x.append(original_x)

    for node_id, node_info in tree_data.items():
        if node_id in pos:
            for child_node_obj in node_info.get('children', []):
                child_id = child_node_obj['id']
                child_level = child_node_obj.get('level', 0)
                if child_id in pos and child_level <= max_depth_to_display:
                    x0, y0 = pos[node_id]
                    x1, y1 = pos[child_id]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
    
    if len(tree_data) > 1 and edge_x:
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y, mode='lines', line=dict(width=1, color='#888'),
            hoverinfo='none', name='Edges'
        ))

    if centered_node_x:
        fig.add_trace(go.Scatter(
            x=centered_node_x, y=node_y, mode='markers+text',
            marker=dict(size=node_sizes, color=node_colors, line=dict(width=1, color='black')),
            text=node_display_text, textposition="bottom center",
            hoverinfo='text', hovertext=node_hover_text, customdata=node_custom_data,
            name='Nodes'
        ))

    fig.update_layout(
        title='Interactive CoRIx Tree Plot', showlegend=False, hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
        plot_bgcolor='white', height=600, width=1000
    )
    return fig

st.markdown("""
**Interpretation:** The `create_interactive_corix_tree_plot` function leverages Plotly to render a visually appealing and interactive node-link diagram. Each node represents a construct in the CoRIx tree, displaying its name and aggregated score. The color and size of a node can change upon selection, providing visual cues. Crucially, the function is designed to work with `max_depth_to_display`, allowing users to control the complexity of the tree shown. Hovering over a node reveals more detailed information, while a click will trigger the display of node-specific details, as described in the previous section. This visualization allows for intuitive exploration of the hierarchical contributions to AI validity risk.
""")
```

### Section 9: Application and Scenario Selection & Callbacks

This section will implement Streamlit widgets and `st.session_state` to manage selection and updates.

```python
st.subheader("Section 9: Application and Scenario Selection & Callbacks")
st.markdown("""
Users will interact with the CoRIx Tree Explorer using dropdown widgets to select their desired AI application and scenario combination. This selection will dynamically update the displayed CoRIx tree and its associated details. The core logic handles the interactivity, ensuring that user choices are immediately reflected in the visualization and detailed outputs.
""")

# Place widgets in the sidebar
with st.sidebar:
    st.header("Controls")
    app_dropdown_options = list(loaded_df.columns[2:])
    selected_app_scenario = st.selectbox(
        'Select Application/Scenario:',
        options=app_dropdown_options,
        key='selected_app_scenario',
        index=app_dropdown_options.index(st.session_state.selected_app_scenario) if st.session_state.selected_app_scenario in app_dropdown_options else 0
    )

    max_depth = st.slider(
        'Max Tree Depth:',
        min_value=2, max_value=5, value=st.session_state.max_tree_depth, step=1,
        key='max_tree_depth'
    )

# Extract application and scenario names
application_name, scenario_name = st.session_state.selected_app_scenario.split(" - ", 1)

# Build tree data
current_tree_data = build_corix_tree_data(loaded_df, application_name, scenario_name)

# Placeholder for node details
details_placeholder = st.empty()

# Create and display the plot
fig = create_interactive_corix_tree_plot(current_tree_data, max_depth_to_display=max_depth, selected_node_id=st.session_state.selected_node_id)
clicked_points = plotly_events(fig, click_event=True, key="corix_tree_plot")

# Handle click event
if clicked_points:
    clicked_node_id = clicked_points[0]['customdata']
    if st.session_state.selected_node_id != clicked_node_id:
        st.session_state.selected_node_id = clicked_node_id
        details_placeholder.empty() # Clear previous details immediately
        display_node_details(current_tree_data, st.session_state.selected_node_id, details_placeholder)
elif st.session_state.selected_node_id: # If a node was previously selected and no new click, re-display its details
    display_node_details(current_tree_data, st.session_state.selected_node_id, details_placeholder)
else: # If no node is selected, prompt the user
    details_placeholder.info("Click on a node in the tree to see its details.")


st.markdown("""
**Interpretation:** This section sets up the interactive controls for our CoRIx Tree Explorer. The dropdown allows users to select different AI application and scenario combinations, while the slider controls the maximum depth of the tree visualization. The interaction logic, integrated with Streamlit's state management, redraws the tree and updates node details whenever a selection is made or a node is clicked. This interactivity is key to enabling dynamic exploration and comparison of AI validity risks across various contexts, directly supporting the learning goals of this application.
""")
```

### Sections 10, 11, 12: Exploring Specific Applications

These sections provide guided examples. In the Streamlit app, these will be rendered as markdown explanations. The user will manually select the corresponding application/scenario from the dropdown to see the changes.

```python
st.subheader("Section 10: Displaying the Interactive CoRIx Tree for Application A / Pathfinder")
st.markdown("""
Let's begin by examining "Application A / Pathfinder". The report indicates an overall CoRIx score of $2.88$, suggesting lower validity risks for this combination. We will generate and interpret the interactive tree visualization for this initial selection. This demonstration highlights how the tool immediately surfaces AI validity risk insights.

**Interpretation:** The visualization for "Application A / Pathfinder" shows an overall CoRIx score of $2.88$. This relatively low score suggests a lower observed risk to validity for this application and scenario combination. Tracing down to Level 3, Red Teaming (score of $2.88$) contributes the most to the overall risk compared to Model Testing ($0.72$) and Field Testing ($2.36$). Further investigation at Level 4 reveals that Annotator Labels (score of $3.52$) identified higher risks during Red Teaming than User Perceptions (score of $2.24$). Delving into Level 5 reveals specific constructs like `RT DD 4` (Red Teaming Dialogue Dynamics 4, unnatural dialogue) with a score of $4.98$ and `FT CC 3` (Field Testing Content Characterization 3, superfluous information) with a score of $7.41$ contributed to higher individual risks. This granular view allows us to pinpoint specific areas of concern.
""")

st.subheader("Section 11: Exploring Application B / TV Spoilers")
st.markdown("""
Next, we explore "Application B / TV Spoilers". The report notes an overall score of $4.29$ for this application-scenario, signaling a moderate potential for validity risk. Observe how the tree structure and score distribution differ from Application A. This comparison helps in understanding varying risk profiles across different AI applications and scenarios.

**Interpretation:** For "Application B / TV Spoilers", the overall CoRIx score is $4.29$, indicating a moderate validity risk. Field Testing (score of $4.29$) contributes most significantly at Level 3, followed by Red Teaming ($3.55$) and Model Testing ($2.29$). At Level 4, Field Tester Perceptions (score of $5.00$) were the primary source of risk compared to Annotator Labels ($3.58$) during field testing. Level 5 reveals high scores from `RT RA 2.1` (Red Teaming Risk Assessment 2.1, guardrail violation) at $5.40$ and `FT CC 3` (Field Testing Content Characterization 3, superfluous information) at $7.42$. This suggests that for this application, field testers perceived more issues, potentially related to guardrail violations and the presence of superfluous information, offering targeted areas for improvement.
""")

st.subheader("Section 12: Exploring Application C / Meal Planner")
st.markdown("""
Finally, we will analyze "Application C / Meal Planner". This application-scenario combination exhibited the highest overall CoRIx score of $6.30$ in the pilot, suggesting a higher level of validity risk. This analysis demonstrates how the explorer can highlight critical risk areas, enabling proactive mitigation strategies.

**Interpretation:** "Application C / Meal Planner" shows the highest overall CoRIx score of $6.30$, indicating the greatest validity risk among the pilot examples. Notably, Model Testing (score of $6.30$) shows the highest risk at Level 3, with Red Teaming ($3.39$) and Field Testing ($2.80$) contributing less. At Level 4, Model Testing Annotator Labels ($6.30$) scored highest. Further breakdown in Level 5 reveals extremely high scores for `MT RA 1` (Model Testing Risk Assessment 1, general functionality) at $9.00$ and `MT RA 2` (Model Testing Risk Assessment 2, response quality) at $7.00$, along with `FT CC 3` (Field Testing Content Characterization 3, superfluous information) at $7.42$. This indicates significant issues with basic functionality and response quality observed during model testing, along with superfluous information in field testing. These findings provide clear guidance for developers to address fundamental AI system shortcomings.
""")
```

### Section 13: Interpreting CoRIx Scores and Hierarchical Contribution

```python
st.subheader("Section 13: Interpreting CoRIx Scores and Hierarchical Contribution")
st.markdown("""
Throughout this exploration, remember that **a higher numeric CoRIx score signifies greater negative risk to validity**.

The hierarchical structure of the CoRIx trees allows for a nuanced understanding of AI system validity risk:
-   **Overall Score (Level 2)**: Provides a high-level summary of the validity risk.
-   **Testing Layers (Level 3)**: Breaks down the overall risk into contributions from different testing methodologies (Model Testing, Red Teaming, Field Testing). This helps identify *where* the risks are most apparent.
-   **Perception Layers (Level 4)**: Differentiates between risks identified by expert annotators (`Annotator Label`) and those perceived by human users (`User Perception`), offering insights into different perspectives on AI performance.
-   **Specific Constructs (Level 5)**: Pinpoints the exact assessment items or questionnaire questions that are driving the risks, enabling developers to target specific areas for improvement.

By interactively navigating these trees, users can gain a deeper understanding of how various factors contribute to the overall trustworthiness and validity of AI systems. This empowers stakeholders to make informed decisions about AI deployment and risk mitigation.
""")
```

### Section 14: Conclusion and References

```python
st.subheader("Section 14: Conclusion and References")
st.markdown("""
This Streamlit application has provided an interactive tool to explore CoRIx measurement trees, enhancing the understanding of how AI validity risk is assessed through various testing layers and aggregation logic. By visualizing and interpreting CoRIx scores, we gain insights into the contextual robustness of AI systems as defined by NIST. This transparent approach facilitates the identification of specific areas for AI system improvement.

**References:**

[1] Section 5.1: Contextual Robustness Index (CoRIx) & Section 5.2: Pilot Measurement Results, NIST AI 700-2: Assessing Risks and Impacts of AI (ARIA) ARIA 0.1: Pilot Evaluation Report, https://doi.org/10.6028/NIST.AI.700-2.
""")
```
