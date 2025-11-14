id: 691784590dc7cd32d7afe90a_documentation
summary: Assessing Risks and Impacts of AI Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Navigating AI Validity Risk: The CoRIx Tree Explorer with Streamlit

## 1. Introduction to the CoRIx Tree Explorer
Duration: 0:10:00

Welcome to the CoRIx Tree Explorer Codelab! This guide will walk you through a powerful Streamlit application designed to visualize and understand the Contextual Robustness Index (CoRIx) measurement trees. CoRIx scores are a crucial metric for assessing the validity risk of AI applications, as detailed in the NIST AI 700-2: ARIA 0.1 Pilot Evaluation Report [1].

<aside class="positive">
This codelab will provide a <b>comprehensive guide</b> for developers, enabling them to grasp the application's core functionalities, underlying concepts, and implementation details. By the end, you'll have a clear understanding of how to build interactive data visualizations for complex hierarchical data using Streamlit and Plotly.
</aside>

### Why is this application important?
In the rapidly evolving landscape of AI, assessing the trustworthiness and validity of AI systems is paramount. The CoRIx framework, proposed by NIST, offers a structured approach to this assessment. This application makes that framework tangible and interactive, allowing stakeholders to:
*   **Demystify complex AI risk assessments**: Understand how individual tests and perceptions aggregate into an overall risk score.
*   **Pinpoint areas of concern**: Identify which parts of an AI system (e.g., model testing, red teaming, field testing) or which specific issues (e.g., specific questionnaire items) contribute most to validity risk.
*   **Facilitate informed decision-making**: Empower developers, testers, and policymakers to make data-driven decisions for AI system improvement and responsible deployment.

### Learning Goals
Upon completing this codelab, you will be able to:
*   Understand the hierarchical structure and aggregation logic of CoRIx measurement trees.
*   Identify how different testing layers (model testing, red teaming, field testing) contribute to overall AI validity risk scores.
*   Analyze the impact of annotator labels and user perceptions on the assessment of AI system trustworthiness.
*   Interpret the meaning of CoRIx scores, where higher scores indicate greater negative risk.
*   Grasp the implementation details of building an interactive Streamlit application with Plotly visualizations.

### Concepts Explained
This codelab covers several key concepts:
*   **CoRIx Framework**: The Contextual Robustness Index as a measure of AI validity risk.
*   **Hierarchical Data Visualization**: Representing complex nested data structures (like a tree) interactively.
*   **Data Aggregation**: Mathematical rules (max, mean) for combining scores across different levels of a hierarchy.
*   **Streamlit Application Development**: Building multi-page interactive web applications with Python.
*   **Plotly Graphing**: Creating dynamic and interactive visualizations for data exploration.
*   **Session State Management**: Using Streamlit's `st.session_state` for persistent user interactions.

### Application Architecture and Flow
The application is structured into a main `app.py` file and three modular pages within the `application_pages` directory. This modular design enhances maintainability and scalability.

<aside class="positive">
<h4>Flow of the CoRIx Tree Explorer Application:</h4>
<p>
This application follows a multi-page Streamlit architecture. The `app.py` acts as the central orchestrator, managing navigation and routing user requests to specific functionalities implemented in separate Python files.
</p>
<p>
<b>1. User Starts App</b> (`streamlit run app.py`)<br>
    ↓<br>
<b>2. `app.py` (Main Orchestrator)</b><br>
    - Sets page configuration (title, layout).<br>
    - Displays sidebar logo and main application title.<br>
    - Manages sidebar navigation (`st.sidebar.selectbox`).<br>
    - Based on user's sidebar selection, imports and executes the relevant page function.<br>
    ↓<br>
<b>3. Navigation Choices:</b><br>
    - <b>"Data Overview"</b><br>
        ↓<br>
        <b>`application_pages/page1.py` (Data Overview Page)</b><br>
        - Introduces the synthetic dataset derived from NIST ARIA 0.1.<br>
        - Ensures `corix_scores.csv` exists (creates it if missing for demonstration purposes).<br>
        - Loads `corix_scores.csv` using `st.cache_data` for efficient data handling.<br>
        - Displays the raw data as a `st.dataframe` for user inspection.<br>
    - <b>"CoRIx Tree Explorer"</b><br>
        ↓<br>
        <b>`application_pages/page2.py` (Interactive Tree Explorer Page - Core Functionality)</b><br>
        - Explains the CoRIx methodology, tree levels, and mathematical aggregation rules.<br>
        - Ensures `corix_scores.csv` exists and loads the dataset.<br>
        - <b>`build_corix_tree_data` (Data Transformation)</b>:<br>
            - Takes the raw DataFrame, selected application, and scenario.<br>
            - Constructs a hierarchical dictionary (`tree_data`) representing the CoRIx tree.<br>
            - Recursively calculates and aggregates scores for each node based on level-specific rules (maximum for Level 2, mean for Levels 3, 4, and 5).<br>
        - <b>User Controls (Sidebar)</b>:<br>
            - `st.selectbox` allows selecting different Application/Scenario combinations.<br>
            - `st.slider` enables control over the maximum tree depth to display.<br>
        - <b>`create_interactive_corix_tree_plot` (Visualization)</b>:<br>
            - Utilizes Plotly (`plotly.graph_objects`) to render an interactive node-link diagram of the CoRIx tree.<br>
            - Dynamically positions nodes, sets colors (highlighting selected nodes), and displays scores.<br>
        - <b>`plotly_events` (Interactivity)</b>:<br>
            - Captures click events on tree nodes, updating `st.session_state.selected_node_id`.<br>
        - <b>`display_node_details` (Detail View)</b>:<br>
            - Triggered by node clicks or initial selection.<br>
            - Displays granular information for the selected node, including its children's scores or contributing raw assessment items.<br>
    - <b>"Interpretation and Conclusion"</b><br>
        ↓<br>
        <b>`application_pages/page3.py` (Guided Interpretation Page)</b><br>
        - Provides pre-written, detailed interpretations for specific application/scenario combinations.<br>
        - Recaps the general interpretation of CoRIx scores and the value of hierarchical contributions.<br>
        - Concludes the application with references.
</p>
</aside>

## 2. Setting Up the Environment
Duration: 0:05:00

Before running the application, you need to set up your Python environment and create the necessary files.

### 2.1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2.2. Create Project Directory
Create a new directory for your project and navigate into it.

```bash
mkdir corix_explorer
cd corix_explorer
mkdir application_pages
```

### 2.3. Install Dependencies
Install the required Python libraries using `pip`.

```bash
pip install streamlit pandas numpy plotly streamlit_plotly_events
```

### 2.4. Create Application Files
Now, create the Python files with the provided code.

#### `app.py`
Create a file named `app.py` in the `corix_explorer` directory and paste the following content:

```python
import streamlit as st
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
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

# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Data Overview", "CoRIx Tree Explorer", "Interpretation and Conclusion"])

if page == "Data Overview":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "CoRIx Tree Explorer":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Interpretation and Conclusion":
    from application_pages.page3 import run_page3
    run_page3()
# Your code ends
```

#### `application_pages/page1.py`
Create a file named `page1.py` inside the `application_pages` directory and paste the following content:

```python
import streamlit as st
import pandas as pd
import os

def run_page1():
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

#### `application_pages/page2.py`
Create a file named `page2.py` inside the `application_pages` directory and paste the following content:

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os # For os.PathLike in load_corix_dataset
from streamlit_plotly_events import plotly_events

# Helper function to load data - needs to be accessible across pages
@st.cache_data
def load_corix_dataset(filepath):
    if not isinstance(filepath, (str, os.PathLike)):
        raise TypeError(f"filepath must be a string or a path-like object, got {type(filepath).__name__}")
    df = pd.read_csv(filepath)
    return df

# Ensure the corix_scores.csv file exists for the app to run
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


def run_page2():
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

    CoRIx scores are aggregated hierarchically using specific mathematical operations at each level. For a parent node $P$ with child nodes $C_1, C_2, \ldots, C_N$ and their respective scores $S_1, S_2, \ldots, S_N$, the parent's score $S_P$ is calculated as follows:

    -   **Level 2 (Risks)**: The parent node score is the maximum of its children's scores. This means the highest risk from any testing layer dictates the overall risk at this level.
        $$ S_P = \max(S_1, S_2, \ldots, S_N) $$

    -   **Level 3 (Testing Level)**: The parent node score is the mean (average) of its children's scores. This averages the contributions from annotator labels and user perceptions within a specific testing level.
        $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

    -   **Level 4 (Annotator Responses & User Perception)**: The parent node score is the mean of its children's scores. This averages the specific assessment items or questionnaire questions that fall under a perception or annotation category.
        $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

    -   **Level 5 (Response Collation)**: The scores at this level represent direct aggregated measures from raw annotator labels or questionnaire responses (Level 6, which are the leaf nodes and not explicitly visualized). For the purpose of this visualization, Level 5 nodes are treated as direct inputs to their Level 4 parents, and their "scores" are assumed to be pre-aggregated from raw responses. The aggregation for its hypothetical children (Level 6) would also be the mean.
        $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

    These aggregation rules ensure that the CoRIx framework accurately reflects how risks propagate and combine across different evaluation layers, providing a robust measure for AI system validity risk.
    """)

    st.subheader("Section 6: Data Preprocessing: Building the Tree Structure and Aggregation Logic")
    st.markdown("""
    To visualize the hierarchical nature of CoRIx, the flat tabular data must be transformed into a tree-like data structure. This process involves identifying parent-child relationships between constructs based on their `Level` and `Construct` names. The `build_corix_tree_data` function will take the raw DataFrame and assemble a structured representation where each node can be linked to its parent and children, with scores aggregated according to the rules defined in Section 4.

    ### Formulae for CoRIx Aggregation (Recap)

    -   **Level 2 (Risks)**: The parent node score is the maximum of its children's scores.
        $$ S_P = \max(S_1, S_2, \ldots, S_N) $$

    -   **Levels 3, 4, 5**: The parent node score is the mean (average) of its children's scores.
        $$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$

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
                # Remove duplicates from raw_assessment_items based on item_id
                node['raw_assessment_items'] = list({frozenset(d.items()) for d in node['raw_assessment_items']})
                node['raw_assessment_items'] = [dict(item) for item in node['raw_assessment_items']]
                node['raw_assessment_items'].sort(key=lambda x: x['item_id'])

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
                st.markdown(f" **Node Details for: {node['name']}** (ID: `{node_id}`) ")
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

#### `application_pages/page3.py`
Create a file named `page3.py` inside the `application_pages` directory and paste the following content:

```python
import streamlit as st

def run_page3():
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

    st.subheader("Section 14: Conclusion and References")
    st.markdown("""
    This Streamlit application has provided an interactive tool to explore CoRIx measurement trees, enhancing the understanding of how AI validity risk is assessed through various testing layers and aggregation logic. By visualizing and interpreting CoRIx scores, we gain insights into the contextual robustness of AI systems as defined by NIST. This transparent approach facilitates the identification of specific areas for AI system improvement.

    **References:**

    [1] Section 5.1: Contextual Robustness Index (CoRIx) & Section 5.2: Pilot Measurement Results, NIST AI 700-2: Assessing Risks and Impacts of AI (ARIA) ARIA 0.1: Pilot Evaluation Report, https://doi.org/10.6028/NIST.AI.700-2.
    """)
```

### 2.5. Run the Application
Navigate back to the `corix_explorer` directory (if you're in `application_pages`) and run the Streamlit application:

```bash
cd .. # if you were in application_pages
streamlit run app.py
```

Your browser should automatically open to the Streamlit application.

## 3. Data Overview (Page 1)
Duration: 0:08:00

This step focuses on the `Data Overview` page, implemented in `application_pages/page1.py`. This page provides context about the dataset used for CoRIx tree visualization.

### 3.1. Purpose of `page1.py`
The `page1.py` script is responsible for:
*   Introducing the synthetic CoRIx dataset.
*   Explaining its structure and origin (NIST ARIA 0.1 report).
*   Ensuring the `corix_scores.csv` file exists, creating it with synthetic data if it doesn't.
*   Loading the dataset efficiently using Streamlit's caching mechanism.
*   Displaying a preview of the raw data.

### 3.2. Understanding the CoRIx Dataset
The application uses a synthetic dataset structured to represent CoRIx scores across different levels and constructs for various AI applications and scenarios.

*   **`corix_scores.csv`**: This CSV file serves as the raw input data.
*   **Columns**:
    *   `Level`: Indicates the hierarchical level of the construct (2, 3, 4, or 5).
    *   `Construct`: The name of the specific item or category within the CoRIx framework.
    *   `Application X - Scenario Y`: Columns representing the CoRIx scores (scaled 0-10) for different AI application and scenario combinations. For example, `Application A - Pathfinder`.

### 3.3. Data Loading and Caching
The `load_corix_dataset` function is decorated with `@st.cache_data`.

```python
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
```

<aside class="positive">
The `@st.cache_data` decorator is a powerful Streamlit feature. It caches the output of a function, preventing re-execution on subsequent runs (e.g., when a user interacts with a widget) if the input parameters haven't changed. This significantly improves application performance, especially for data loading or heavy computation.
</aside>

### 3.4. Data Generation Logic
For demonstration purposes, if `corix_scores.csv` does not exist, the application programmatically creates it using a predefined dictionary `data` and saves it. This ensures the application is self-contained and runnable without manual data file setup.

```python
    if not os.path.exists('corix_scores.csv'):
        data = {
            # ... (data dictionary) ...
        }
        corix_df = pd.DataFrame(data)
        corix_df.to_csv('corix_scores.csv', index=False)
```

### 3.5. Displaying Raw Data
The `st.dataframe(loaded_df.head())` command displays the first few rows of the loaded DataFrame. This provides a quick visual check of the raw input data.

**Interpretation:** Observe the `Level` and `Construct` columns, which define the hierarchy, and the score columns for different applications. Notice that scores are already pre-computed for various levels, but the application's core logic will re-aggregate and structure this data into a tree.

## 4. Understanding the CoRIx Framework and Methodology (Page 2 - Theory)
Duration: 0:15:00

Switch to the "CoRIx Tree Explorer" page in the sidebar. This page, primarily driven by `application_pages/page2.py`, is the heart of the application. It starts by explaining the theoretical underpinnings of the CoRIx framework and its aggregation logic.

### 4.1. The Contextual Robustness Index (CoRIx)
CoRIx is a multi-dimensional metric designed to quantify the technical and contextual robustness of AI systems. It provides a validity risk score, where a **higher numeric CoRIx score indicates greater negative risk** to AI system validity. All scores are normalized from 0 to 10.

### 4.2. CoRIx Tree Structure
The CoRIx framework organizes assessment into a hierarchical tree with several levels:
*   **Level 2: Risks**: The highest level visualized, typically representing overall risks like `Validity/Reliability (V/R)`.
*   **Level 3: Testing Level**: Breaks down risks by evaluation methodology: `Model Testing (MT)`, `Red Teaming (RT)`, `Field Testing (FT)`.
*   **Level 4: Annotator Responses & User Perception**: Further refines risks based on who identified them: `Annotator Label` (expert evaluators) or `User Perception` (end-users).
*   **Level 5: Response Collation**: Represents specific assessment items or questionnaire questions (e.g., `RA 2.1`, `DD 2`) that directly feed into Level 4 scores. These are the most granular nodes explicitly visualized.

### 4.3. Mathematical Foundation of CoRIx Aggregation
The CoRIx framework uses specific aggregation rules to combine scores from child nodes to their parent nodes.

#### Level 2 (Risks) Aggregation
At Level 2, the parent node's score (e.g., `Validity/Reliability (V/R)`) is the **maximum** of its children's scores. This means the overall risk is determined by the *highest* risk identified across any of the testing layers below it.

$$ S_P = \max(S_1, S_2, \ldots, S_N) $$
Where $S_P$ is the parent's score and $S_i$ are the scores of its child nodes (e.g., Model Testing, Red Teaming, Field Testing).

#### Levels 3, 4, and 5 Aggregation
For Levels 3, 4, and 5, the parent node's score is the **mean (average)** of its children's scores. This approach averages contributions from various sub-components, providing a balanced aggregation.

$$ S_P = \frac{1}{N} \sum_{i=1}^{N} S_i $$
Where $S_P$ is the parent's score, $N$ is the number of child nodes, and $S_i$ are the scores of the child nodes. For example, the `Model Testing (MT)` score (Level 3) would be the average of `MT Annotator Label` and `MT User Perception` scores (Level 4, if `MT User Perception` existed). Similarly, `MT Annotator Label` (Level 4) would be the average of its Level 5 assessment items. Level 5 nodes are typically direct inputs, and their scores are assumed to be pre-aggregated from raw (Level 6) responses; if they had children, their aggregation would also be the mean.

<aside class="negative">
It is crucial to understand these aggregation rules, as they dictate how risks propagate through the CoRIx tree. Misinterpreting these rules can lead to incorrect conclusions about AI system validity risk.
</aside>

## 5. Data Preprocessing and Tree Building (Page 2 - Implementation)
Duration: 0:15:00

This step dives into the `build_corix_tree_data` function, which transforms the flat tabular data into a hierarchical structure suitable for visualization. This is a crucial data engineering step.

### 5.1. The `aggregate_node_score` Function
This helper function encapsulates the aggregation logic based on the CoRIx level.

```python
def aggregate_node_score(children_scores, level):
    if level == 2:
        return np.max(children_scores)
    elif level in [3, 4, 5]:
        return np.mean(children_scores)
    else:
        return np.nan
```
*   If the `level` is 2, it returns the maximum score among children.
*   For levels 3, 4, and 5, it returns the mean of the children's scores.

### 5.2. The `build_corix_tree_data` Function
This function is responsible for parsing the `corix_scores.csv` DataFrame and constructing a dictionary representation of the CoRIx tree.

```python
@st.cache_data
def build_corix_tree_data(dataframe, application, scenario):
    # ... (input validation and DataFrame filtering) ...

    # Parent-child mapping for building the hierarchy
    parent_map = {
        'Model Testing (MT)': 'Validity/Reliability (V/R)',
        'MT Annotator Label': 'Model Testing (MT)',
        # ... (many more mappings) ...
    }

    all_nodes = {}
    for _, row in df_filtered.iterrows():
        # Create initial node objects from DataFrame rows
        # ... (node creation logic) ...
        all_nodes[construct] = node
    
    # Establish parent-child relationships
    # Identify the root node 'Validity/Reliability (V/R)'
    # ... (relationship building) ...

    # Recursive function to calculate and aggregate scores from bottom-up
    def calculate_and_aggregate_scores(node):
        if not node['children']: # Base case: leaf node (Level 5)
            return node['score'] if node['level'] == 5 else 0.0

        children_scores = []
        for child in node['children']:
            child_score = calculate_and_aggregate_scores(child) # Recursive call
            children_scores.append(child_score)
        
        # Collect raw assessment items for parent nodes (for display)
        if node['level'] < 5:
            for child in node['children']:
                node['raw_assessment_items'].extend(child['raw_assessment_items'])
            # Remove duplicates and sort
            # ... (deduplication and sorting logic) ...

        # Aggregate current node's score using aggregate_node_score
        node['score'] = aggregate_node_score(children_scores, node['level'])
        return node['score']

    if root_node_obj:
        calculate_and_aggregate_scores(root_node_obj) # Start aggregation from the root
    
    return all_nodes
```

<aside class="positive">
The `build_corix_tree_data` function employs a <b>recursive approach</b> to calculate aggregated scores. It starts from the lowest level (Level 5) nodes, retrieves their scores, and then recursively passes these scores up the hierarchy. Each parent node then aggregates its children's scores based on the rules defined in `aggregate_node_score`. This ensures that all scores in the tree accurately reflect the CoRIx aggregation logic.
</aside>

**Key aspects of `build_corix_tree_data`:**
1.  **Input Filtering**: Takes the raw DataFrame, application, and scenario, then filters to the relevant score column.
2.  **`parent_map`**: A crucial dictionary that explicitly defines the parent-child relationships between construct names. This is necessary because the raw data doesn't explicitly link parents to children beyond their `Level`.
3.  **Node Initialization**: Iterates through the filtered DataFrame to create initial node objects, storing them in `all_nodes`.
4.  **Relationship Building**: Uses `parent_map` to assign `parent_id` and populate the `children` list for each node. It also identifies the `root_node_obj` ('Validity/Reliability (V/R)').
5.  **Recursive Aggregation (`calculate_and_aggregate_scores`)**:
    *   This nested function traverses the tree from the bottom up.
    *   **Base Case**: If a node has no children (a Level 5 leaf node in this visualization), its score is returned directly.
    *   **Recursive Step**: For parent nodes, it recursively calls itself for each child, collects their aggregated scores, and then applies `aggregate_node_score` to determine its own score.
    *   **`raw_assessment_items`**: This list is populated for parent nodes by extending it with raw assessment items from its children, which is useful for displaying details.

**Interpretation:** After running `build_corix_tree_data`, `current_tree_data` will be a dictionary where keys are construct IDs and values are node objects. Each node object contains its ID, name, parent ID, children, level, and the calculated aggregated score. This structured data is ready for visualization.

## 6. Node Details Display (Page 2 - Functionality)
Duration: 0:08:00

Understanding the detailed contributions to a CoRIx score is vital. The `display_node_details` function provides this granularity.

### 6.1. Purpose of `display_node_details`
This function is designed to be called when a user clicks on a node in the interactive tree. Its responsibilities include:
*   Clearing previous details.
*   Retrieving the specific node's data from the `tree_data` dictionary.
*   Displaying the node's level, construct name, and its aggregated score.
*   Crucially, it either lists the scores of its direct children (for Level 2, 3, 4 nodes) or the specific raw assessment items/questionnaire questions that contributed to its own score (for Level 5 nodes).

```python
def display_node_details(tree_data, node_id, placeholder):
    with placeholder:
        st.empty() # Clear previous content
        if node_id not in tree_data:
            st.write(f"Node with ID '{node_id}' not found.")
            return

        node = tree_data[node_id]

        st.markdown(f" **Node Details for: {node['name']}** (ID: `{node_id}`) ")
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
```

### 6.2. How it Works
1.  **`placeholder`**: The function takes a Streamlit `placeholder` object. This allows dynamically updating a specific section of the UI without redrawing the entire application. `st.empty()` ensures old content is removed.
2.  **Node Retrieval**: It looks up the `node_id` in the `tree_data` dictionary to get the full node object.
3.  **Conditional Display**:
    *   If the node is at Level 2, 3, or 4, it iterates through `node['children']` and displays their names, IDs, and scores. This helps understand how immediate sub-components contribute.
    *   If the node is at Level 5, it iterates through `node['raw_assessment_items']` (which were collected during the recursive aggregation in `build_corix_tree_data`) and displays their IDs, questions, and scores. This provides the most granular breakdown.

**Interpretation:** This functionality is key to the application's goal of transparency. By clicking on any node, users can immediately see the breakdown of what constitutes that node's score, allowing them to trace risks back to their root causes within the CoRIx hierarchy.

## 7. Interactive Tree Visualization (Page 2 - Implementation)
Duration: 0:20:00

The core visualization for the CoRIx Tree Explorer is powered by Plotly, rendered as an interactive node-link diagram.

### 7.1. Purpose of `create_interactive_corix_tree_plot`
This function, implemented using `plotly.graph_objects`, generates the visual representation of the CoRIx tree. It handles:
*   Creating a `go.Figure` object.
*   Positioning nodes and drawing edges between them.
*   Customizing node appearance (color, size, text, hover information).
*   Filtering nodes based on a `max_depth_to_display` setting.
*   Highlighting a `selected_node_id`.

```python
def create_interactive_corix_tree_plot(tree_data, max_depth_to_display=5, selected_node_id=None):
    # ... (initialization and validation) ...

    node_x, node_y, node_hover_text, node_display_text, node_colors, node_sizes, node_custom_data = [], [], [], [], [], [], []
    edge_x, edge_y = [], []
    
    nodes_map = tree_data
    root_node_id = 'Validity/Reliability (V/R)'

    pos = {} # Stores (x,y) coordinates for each node
    queue = [(root_node_id, 0)] # For BFS traversal to determine layout
    visited_nodes = set([root_node_id])
    level_to_x_coords = {} # Helps in centering nodes per level

    while queue:
        current_node_id, current_depth_layout = queue.pop(0)
        node_info = nodes_map[current_node_id]
        actual_level = node_info.get('level', 0)

        if actual_level > max_depth_to_display:
            continue

        y_coord = -actual_level * 100 # Vertical positioning based on level
        
        # Horizontal positioning within a level
        if actual_level not in level_to_x_coords:
            level_to_x_coords[actual_level] = []
        current_x_offset = len(level_to_x_coords[actual_level]) * 150
        x_coord = current_x_offset
        level_to_x_coords[actual_level].append(x_coord)
        pos[current_node_id] = (x_coord, y_coord)

        # Collect data for Plotly Scatter trace
        node_x.append(x_coord)
        node_y.append(y_coord)
        node_hover_text.append(...) # Detailed info on hover
        node_display_text.append(...) # Text displayed on node
        node_custom_data.append(node_info.get('id')) # Data for click events
        
        is_selected = (current_node_id == selected_node_id)
        node_colors.append('red' if is_selected else '#66b3ff')
        node_sizes.append(25 if is_selected else 20)

        # Add children to queue for traversal if within max_depth
        for child_node_obj in node_info.get('children', []):
            child_id = child_node_obj['id']
            child_level = child_node_obj.get('level', actual_level + 1)
            if child_id in nodes_map and child_id not in visited_nodes and child_level <= max_depth_to_display:
                queue.append((child_id, child_level))
                visited_nodes.add(child_id)
                
    # Logic to horizontally center nodes at each level for better aesthetics
    max_overall_width = max(...) 
    centered_node_x = []
    for i, node_id in enumerate(node_custom_data):
        # ... (centering calculation) ...
        centered_node_x.append(original_x + offset)
        pos[node_id] = (original_x + offset, pos[node_id][1])

    # Create edges based on parent-child relationships and calculated positions
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
    
    # Add traces to the Plotly figure
    if len(tree_data) > 1 and edge_x:
        fig.add_trace(go.Scatter(...)) # Edges trace

    if centered_node_x:
        fig.add_trace(go.Scatter(...)) # Nodes trace

    fig.update_layout(...) # Layout settings (title, axes, background)
    return fig
```

### 7.2. How it Works
1.  **Graph Representation**: The function starts by collecting data for nodes (`node_x`, `node_y`, `node_hover_text`, etc.) and edges (`edge_x`, `edge_y`).
2.  **Breadth-First Search (BFS) for Layout**:
    *   A BFS approach (using a `queue`) is used to traverse the `tree_data` starting from the `root_node_id` (`Validity/Reliability (V/R)`).
    *   **Vertical Positioning (`y_coord`)**: Nodes are placed vertically based on their `actual_level` (e.g., Level 2 at `y=-200`, Level 3 at `y=-300`, etc.).
    *   **Horizontal Positioning (`x_coord`)**: Within each level, nodes are initially placed sequentially. `level_to_x_coords` helps manage this.
    *   **Filtering by Depth**: Nodes beyond `max_depth_to_display` are skipped.
    *   **`pos` Dictionary**: Stores the calculated (x, y) coordinates for each node.
3.  **Node Customization**:
    *   `node_hover_text`: Provides rich information when the user hovers over a node.
    *   `node_display_text`: The text shown directly on the node (name and score).
    *   `node_custom_data`: Crucially, this stores the `node['id']`, which is later used by `plotly_events` to identify which node was clicked.
    *   **Highlighting**: If `current_node_id` matches `selected_node_id`, the node's color becomes red and its size increases, providing visual feedback.
4.  **Centering Nodes**: After initial positioning, an additional loop calculates offsets to horizontally center the entire tree, and each level within itself, improving readability.
5.  **Plotly Traces**:
    *   **Edges**: A `go.Scatter` trace with `mode='lines'` draws the connections between parent and child nodes.
    *   **Nodes**: Another `go.Scatter` trace with `mode='markers+text'` renders the nodes as circles with text labels.
6.  **Layout**: `fig.update_layout` customizes the plot's title, disables grid lines and axis labels for a cleaner look, and sets fixed ranges.

**Interpretation:** This function converts the structured `tree_data` into a compelling visual interface. The interactive nature (hover, click, depth control) allows users to explore the complex CoRIx hierarchy intuitively, making it easier to identify high-risk areas and their contributing factors.

## 8. Application Control and Interactivity (Page 2 - Controls)
Duration: 0:10:00

This section integrates user interface controls (dropdowns, sliders) with the data processing and visualization functions, enabling dynamic interaction with the CoRIx Tree Explorer.

### 8.1. Streamlit Widgets for Control
The application provides two main interactive controls in the sidebar:

1.  **Application/Scenario Selection (`st.selectbox`)**:
    ```python
    selected_app_scenario = st.selectbox(
        'Select Application/Scenario:',
        options=app_dropdown_options,
        key='selected_app_scenario',
        index=app_dropdown_options.index(st.session_state.selected_app_scenario) if st.session_state.selected_app_scenario in app_dropdown_options else 0
    )
    ```
    This dropdown allows users to choose which `Application - Scenario` combination they want to visualize. `st.session_state` is used to persist the selected value across reruns.

2.  **Max Tree Depth Slider (`st.slider`)**:
    ```python
    max_depth = st.slider(
        'Max Tree Depth:',
        min_value=2, max_value=5, value=st.session_state.max_tree_depth, step=1,
        key='max_tree_depth'
    )
    ```
    This slider lets users control how many levels of the CoRIx tree are displayed, allowing them to simplify complex trees or drill down into details. The `key` also uses `st.session_state`.

### 8.2. Data Flow and Redrawing
1.  **Extracting Selection**: The selected application and scenario names are extracted from the `selected_app_scenario` string.
2.  **Building Tree Data**: The `build_corix_tree_data` function is called with the selected application and scenario to generate the `current_tree_data`.
3.  **Plot Generation**: The `create_interactive_corix_tree_plot` function is then called with `current_tree_data`, `max_depth`, and the `selected_node_id` (from `st.session_state`) to render the Plotly figure.

### 8.3. Handling Click Events (`plotly_events`)
The `streamlit_plotly_events` library bridges the interactivity between Plotly figures and Streamlit.

```python
clicked_points = plotly_events(fig, click_event=True, key="corix_tree_plot")

if clicked_points:
    clicked_node_id = clicked_points[0]['customdata']
    if st.session_state.selected_node_id != clicked_node_id:
        st.session_state.selected_node_id = clicked_node_id
        details_placeholder.empty() # Clear previous details immediately
        display_node_details(current_tree_data, st.session_state.selected_node_id, details_placeholder)
elif st.session_state.selected_node_id:
    display_node_details(current_tree_data, st.session_state.selected_node_id, details_placeholder)
else:
    details_placeholder.info("Click on a node in the tree to see its details.")
```
*   `plotly_events(fig, click_event=True)` listens for clicks on the `fig` (Plotly figure).
*   If a `clicked_points` list is returned (meaning a node was clicked), it extracts the `customdata` (which contains the `node_id`) of the clicked node.
*   It updates `st.session_state.selected_node_id` to the newly clicked node's ID.
*   The `details_placeholder` (created using `st.empty()`) is cleared, and `display_node_details` is called to show the new node's information.
*   If no new node is clicked but a node was previously selected, its details are re-displayed to maintain context during reruns.
*   If no node is selected, an informational message prompts the user to interact with the tree.

**Interpretation:** This interactive setup allows users to dynamically control which CoRIx tree they view and to drill down into the specifics of any node. The use of `st.session_state` ensures a smooth and consistent user experience, making the application highly responsive to user input.

## 9. Exploring Application A / Pathfinder (Page 3 - Use Case 1)
Duration: 0:05:00

Navigate to the "Interpretation and Conclusion" page in the sidebar. This page, powered by `application_pages/page3.py`, provides pre-analyzed insights for the different application scenarios.

### 9.1. Guided Exploration
The first section guides you through the interpretation of "Application A / Pathfinder".

**Task**: In the "CoRIx Tree Explorer" page, select "Application A - Pathfinder" from the sidebar dropdown. Keep the Max Tree Depth slider at 5. Observe the tree and then click on various nodes to see their details.

**Interpretation:**
The visualization for "Application A / Pathfinder" shows an overall CoRIx score of $2.88$. This relatively low score suggests a lower observed risk to validity for this application and scenario combination. Tracing down to Level 3, Red Teaming (score of $2.88$) contributes the most to the overall risk compared to Model Testing ($0.72$) and Field Testing ($2.36$). Further investigation at Level 4 reveals that Annotator Labels (score of $3.52$) identified higher risks during Red Teaming than User Perceptions (score of $2.24$). Delving into Level 5 reveals specific constructs like `RT DD 4` (Red Teaming Dialogue Dynamics 4, unnatural dialogue) with a score of $4.98$ and `FT CC 3` (Field Testing Content Characterization 3, superfluous information) with a score of $7.41$ contributed to higher individual risks. This granular view allows us to pinpoint specific areas of concern.

## 10. Exploring Application B / TV Spoilers (Page 3 - Use Case 2)
Duration: 0:05:00

Next, we explore "Application B / TV Spoilers", which shows a moderate validity risk.

**Task**: In the "CoRIx Tree Explorer" page, select "Application B - TV Spoilers" from the sidebar dropdown. Keep the Max Tree Depth slider at 5. Compare this tree structure and scores with "Application A - Pathfinder".

**Interpretation:**
For "Application B / TV Spoilers", the overall CoRIx score is $4.29$, indicating a moderate validity risk. Field Testing (score of $4.29$) contributes most significantly at Level 3, followed by Red Teaming ($3.55$) and Model Testing ($2.29$). At Level 4, Field Tester Perceptions (score of $5.00$) were the primary source of risk compared to Annotator Labels ($3.58$) during field testing. Level 5 reveals high scores from `RT RA 2.1` (Red Teaming Risk Assessment 2.1, guardrail violation) at $5.40$ and `FT CC 3` (Field Testing Content Characterization 3, superfluous information) at $7.42$. This suggests that for this application, field testers perceived more issues, potentially related to guardrail violations and the presence of superfluous information, offering targeted areas for improvement.

## 11. Exploring Application C / Meal Planner (Page 3 - Use Case 3)
Duration: 0:05:00

Finally, we will analyze "Application C / Meal Planner", which exhibits the highest overall CoRIx score among the examples.

**Task**: In the "CoRIx Tree Explorer" page, select "Application C - Meal Planner" from the sidebar dropdown. Keep the Max Tree Depth slider at 5. Observe how the tree structure highlights critical risk areas.

**Interpretation:**
"Application C / Meal Planner" shows the highest overall CoRIx score of $6.30$, indicating the greatest validity risk among the pilot examples. Notably, Model Testing (score of $6.30$) shows the highest risk at Level 3, with Red Teaming ($3.39$) and Field Testing ($2.80$) contributing less. At Level 4, Model Testing Annotator Labels ($6.30$) scored highest. Further breakdown in Level 5 reveals extremely high scores for `MT RA 1` (Model Testing Risk Assessment 1, general functionality) at $9.00$ and `MT RA 2` (Model Testing Risk Assessment 2, response quality) at $7.00$, along with `FT CC 3` (Field Testing Content Characterization 3, superfluous information) at $7.42$. This indicates significant issues with basic functionality and response quality observed during model testing, along with superfluous information in field testing. These findings provide clear guidance for developers to address fundamental AI system shortcomings.

## 12. Interpreting CoRIx Scores and Hierarchical Contribution (Page 3 - Recap)
Duration: 0:05:00

This section summarizes the key takeaways regarding CoRIx score interpretation and the benefits of its hierarchical structure.

### 12.1. Meaning of CoRIx Scores
Always remember that **a higher numeric CoRIx score signifies greater negative risk to validity**. The scores are on a scale of 0 to 10.

### 12.2. Value of Hierarchical Structure
The tree structure of CoRIx provides a multi-faceted view of AI validity risk:
*   **Overall Score (Level 2)**: Provides a quick, high-level summary of the AI system's validity risk in a given context.
*   **Testing Layers (Level 3)**: Breaks down the overall risk by the methodology used to assess it (Model Testing, Red Teaming, Field Testing). This helps in identifying *where* the primary risks are being detected, allowing for targeted process improvements.
*   **Perception Layers (Level 4)**: Differentiates risks based on the source of feedback: expert annotators (`Annotator Label`) vs. human users (`User Perception`). This distinction can highlight discrepancies in how experts and end-users perceive an AI system's trustworthiness.
*   **Specific Constructs (Level 5)**: Pinpoints the exact granular assessment items or questionnaire questions that are driving the risks. This level provides actionable insights for developers to address specific issues within the AI system.

By interactively navigating these trees, users can gain a deeper understanding of how various factors contribute to the overall trustworthiness and validity of AI systems. This empowers stakeholders to make informed decisions about AI deployment and risk mitigation.

## 13. Conclusion and References
Duration: 0:03:00

Congratulations! You have successfully completed the CoRIx Tree Explorer Codelab.

This Streamlit application has provided an interactive tool to explore CoRIx measurement trees, enhancing the understanding of how AI validity risk is assessed through various testing layers and aggregation logic. By visualizing and interpreting CoRIx scores, we gain insights into the contextual robustness of AI systems as defined by NIST. This transparent approach facilitates the identification of specific areas for AI system improvement.

You've learned about:
*   The significance of CoRIx in AI risk assessment.
*   The hierarchical structure and aggregation rules of CoRIx trees.
*   How to develop a multi-page Streamlit application.
*   Techniques for transforming flat data into a hierarchical structure.
*   Creating interactive Plotly visualizations within Streamlit.
*   Managing application state for dynamic user experiences.

We hope this codelab has equipped you with valuable insights into AI validity risk assessment and the development of interactive data applications.

**References:**

[1] Section 5.1: Contextual Robustness Index (CoRIx) & Section 5.2: Pilot Measurement Results, NIST AI 700-2: Assessing Risks and Impacts of AI (ARIA) ARIA 0.1: Pilot Evaluation Report, https://doi.org/10.6028/NIST.AI.700-2.
