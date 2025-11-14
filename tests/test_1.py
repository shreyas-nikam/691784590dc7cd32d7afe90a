import pytest
import pandas as pd
import numpy as np

# Placeholder for your module import
# DO NOT REPLACE or REMOVE THIS BLOCK
try:
    from definition_c48236c77fa6403cb21e737295dd9906 import build_corix_tree_data, aggregate_node_score
except ImportError:
    # Fallback for testing if definition_c48236c77fa6403cb21e737295dd9906 is not fully implemented yet.
    # In a real scenario, this would mean the tests cannot run until the module
    # is correctly set up. For this exercise, we provide a mock `aggregate_node_score`
    # to allow `build_corix_tree_data` to be tested against its expected behavior.
    # The `build_corix_tree_data` function itself is assumed to be imported.

    def aggregate_node_score(children_scores: list, level: int) -> float:
        """
        Mock aggregation logic based on the notebook specification.
        This function would typically be implemented in `definition_c48236c77fa6403cb21e737295dd9906`.
        """
        if not children_scores:
            return 0.0 # Return 0.0 for empty children list, consistent with no risk.
        if level == 2: # Risks
            return np.max(children_scores)
        elif level in [3, 4, 5]: # Testing Level, Annotator Responses & User Perception, Response Collation
            return np.mean(children_scores)
        else:
            # For levels not specified, or if there's an issue, return 0.0 or raise an error.
            # Returning 0.0 for unknown levels is a safe default for a mock.
            return 0.0
    
# DO NOT REPLACE or REMOVE THE ABOVE BLOCK

@pytest.fixture
def complex_corix_dataframe():
    """
    A representative pandas DataFrame mimicking the CoRIx dataset structure
    as described in the notebook specification.
    Level 5 scores are provided as base, and higher level scores (NaNs)
    are expected to be calculated by `build_corix_tree_data`.
    """
    data = {
        'Level': [2, 3, 3, 4, 4, 5, 5, 5],
        'Construct': [
            'Validity/Reliability', # Level 2 (Root)
            'Model Testing',        # Level 3 child of V/R
            'Red Teaming',          # Level 3 child of V/R
            'MT Annotator Label',   # Level 4 child of Model Testing
            'RT Annotator Label',   # Level 4 child of Red Teaming
            'MT RA 1',              # Level 5 child of MT Annotator Label
            'MT RA 2',              # Level 5 child of MT Annotator Label
            'RT DD 4'               # Level 5 child of RT Annotator Label
        ],
        'Application A - Pathfinder': [np.nan, np.nan, np.nan, np.nan, np.nan, 1.0, 3.0, 5.0],
        'Application B - TV Spoilers': [np.nan, np.nan, np.nan, np.nan, np.nan, 2.0, 4.0, 6.0]
    }
    return pd.DataFrame(data)

def _create_expected_tree(df: pd.DataFrame, application: str, scenario: str) -> dict:
    """
    Helper function to generate the expected tree structure and scores,
    mirroring the hierarchical processing and aggregation logic that
    `build_corix_tree_data` is expected to implement.
    It uses the `aggregate_node_score` function (either real or mock).
    """
    app_scenario_col = f"{application} - {scenario}"
    
    # Filter the DataFrame for relevant columns and the specific application/scenario
    df_filtered = df[
        [col for col in df.columns if col in ['Level', 'Construct'] or col == app_scenario_col]
    ].copy()
    df_filtered.rename(columns={app_scenario_col: 'score'}, inplace=True)

    # Extract Level 5 (leaf) scores directly from the filtered dataframe
    score_mt_ra1 = df_filtered[df_filtered['Construct'] == 'MT RA 1']['score'].iloc[0]
    score_mt_ra2 = df_filtered[df_filtered['Construct'] == 'MT RA 2']['score'].iloc[0]
    score_rt_dd4 = df_filtered[df_filtered['Construct'] == 'RT DD 4']['score'].iloc[0]
    
    # Calculate scores upwards using the assumed aggregation logic (`aggregate_node_score`)
    # Level 4 aggregations (mean)
    score_mt_annotator_label = aggregate_node_score([score_mt_ra1, score_mt_ra2], 4) # (1.0 + 3.0) / 2 = 2.0
    score_rt_annotator_label = aggregate_node_score([score_rt_dd4], 4)             # (5.0) / 1 = 5.0

    # Level 3 aggregations (mean)
    score_model_testing = aggregate_node_score([score_mt_annotator_label], 3)    # (2.0) / 1 = 2.0
    score_red_teaming = aggregate_node_score([score_rt_annotator_label], 3)      # (5.0) / 1 = 5.0

    # Level 2 (Root) aggregation (max)
    score_validity_reliability = aggregate_node_score([score_model_testing, score_red_teaming], 2) # max(2.0, 5.0) = 5.0

    # Construct the expected hierarchical dictionary
    expected_tree = {
        'id': 'Validity/Reliability', 'name': 'Validity/Reliability', 'parent_id': None,
        'score': score_validity_reliability, 'level': 2, 'construct': 'Validity/Reliability',
        'children': [
            {
                'id': 'Model Testing', 'name': 'Model Testing', 'parent_id': 'Validity/Reliability',
                'score': score_model_testing, 'level': 3, 'construct': 'Model Testing',
                'children': [
                    {
                        'id': 'MT Annotator Label', 'name': 'MT Annotator Label', 'parent_id': 'Model Testing',
                        'score': score_mt_annotator_label, 'level': 4, 'construct': 'MT Annotator Label',
                        'children': [
                            {
                                'id': 'MT RA 1', 'name': 'MT RA 1', 'parent_id': 'MT Annotator Label',
                                'score': score_mt_ra1, 'level': 5, 'construct': 'MT RA 1', 'children': [],
                                'raw_assessment_items': ['MT RA 1']
                            },
                            {
                                'id': 'MT RA 2', 'name': 'MT RA 2', 'parent_id': 'MT Annotator Label',
                                'score': score_mt_ra2, 'level': 5, 'construct': 'MT RA 2', 'children': [],
                                'raw_assessment_items': ['MT RA 2']
                            }
                        ],
                        'raw_assessment_items': []
                    }
                ],
                'raw_assessment_items': []
            },
            {
                'id': 'Red Teaming', 'name': 'Red Teaming', 'parent_id': 'Validity/Reliability',
                'score': score_red_teaming, 'level': 3, 'construct': 'Red Teaming',
                'children': [
                    {
                        'id': 'RT Annotator Label', 'name': 'RT Annotator Label', 'parent_id': 'Red Teaming',
                        'score': score_rt_annotator_label, 'level': 4, 'construct': 'RT Annotator Label',
                        'children': [
                             {
                                'id': 'RT DD 4', 'name': 'RT DD 4', 'parent_id': 'RT Annotator Label',
                                'score': score_rt_dd4, 'level': 5, 'construct': 'RT DD 4', 'children': [],
                                'raw_assessment_items': ['RT DD 4']
                            }
                        ],
                        'raw_assessment_items': []
                    }
                ],
                'raw_assessment_items': []
            }
        ],
        'raw_assessment_items': []
    }
    return expected_tree

def _compare_trees(actual, expected):
    """
    Recursive helper function to compare two tree dictionaries,
    handling floating point comparisons and list order.
    """
    assert isinstance(actual, dict)
    assert isinstance(expected, dict)
    assert set(actual.keys()) == set(expected.keys())
    for key in expected.keys():
        if key == 'score':
            # Use pytest.approx for floating point comparisons
            assert pytest.approx(actual[key]) == expected[key], f"Score mismatch for node {actual.get('id', 'N/A')}"
        elif key == 'children':
            assert isinstance(actual[key], list)
            assert isinstance(expected[key], list)
            assert len(actual[key]) == len(expected[key]), f"Children count mismatch for node {actual.get('id', 'N/A')}"
            
            # Sort children by 'id' for consistent comparison order, assuming 'id' is unique
            actual_children_sorted = sorted(actual[key], key=lambda x: x['id'])
            expected_children_sorted = sorted(expected[key], key=lambda x: x['id'])
            for ac, ec in zip(actual_children_sorted, expected_children_sorted):
                _compare_trees(ac, ec)
        elif key == 'raw_assessment_items':
            assert actual[key] == expected[key], f"Raw assessment items mismatch for node {actual.get('id', 'N/A')}"
        else:
            assert actual[key] == expected[key], f"Attribute '{key}' mismatch for node {actual.get('id', 'N/A')}"


def test_build_corix_tree_data_basic_functionality(complex_corix_dataframe):
    """
    Test case 1: Verify the function correctly builds a hierarchical tree
    structure and aggregates scores for a valid input DataFrame and a known
    application/scenario.
    """
    application = "Application A"
    scenario = "Pathfinder"
    
    expected_tree = _create_expected_tree(complex_corix_dataframe, application, scenario)
    actual_tree = build_corix_tree_data(complex_corix_dataframe, application, scenario)
    
    _compare_trees(actual_tree, expected_tree)

def test_build_corix_tree_data_nonexistent_column(complex_corix_dataframe):
    """
    Test case 2: Verify that a KeyError is raised when the specified
    `application` and `scenario` combination does not form a column
    that exists in the input DataFrame.
    """
    application = "NonExistentApp"
    scenario = "NonExistentScenario"
    with pytest.raises(KeyError, match=f"column '{application} - {scenario}' not found"):
        build_corix_tree_data(complex_corix_dataframe, application, scenario)

def test_build_corix_tree_data_empty_dataframe():
    """
    Test case 3: Verify that passing an empty pandas DataFrame results in
    an empty dictionary, as there's no data to construct any part of the tree.
    """
    empty_df = pd.DataFrame(columns=['Level', 'Construct', 'Application A - Pathfinder'])
    application = "Application A"
    scenario = "Pathfinder"
    
    actual_tree = build_corix_tree_data(empty_df, application, scenario)
    assert actual_tree == {}

@pytest.mark.parametrize("missing_column", ['Level', 'Construct'])
def test_build_corix_tree_data_missing_required_columns(complex_corix_dataframe, missing_column):
    """
    Test case 4: Verify that a KeyError is raised if the input DataFrame
    is missing critical columns ('Level' or 'Construct') required for
    establishing the hierarchy.
    """
    df_missing_col = complex_corix_dataframe.drop(columns=[missing_column])
    application = "Application A"
    scenario = "Pathfinder"
    with pytest.raises(KeyError, match=missing_column):
        build_corix_tree_data(df_missing_col, application, scenario)

@pytest.mark.parametrize("invalid_df_input", [
    None,
    "not a dataframe",
    123,
    [1, 2, 3],
    pd.Series([1, 2, 3]) # A pandas Series is not a DataFrame
])
def test_build_corix_tree_data_invalid_dataframe_type(invalid_df_input):
    """
    Test case 5: Verify that a TypeError is raised when the `dataframe`
    argument is not a pandas DataFrame object.
    """
    application = "Application A"
    scenario = "Pathfinder"
    with pytest.raises(TypeError):
        build_corix_tree_data(invalid_df_input, application, scenario)