
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
