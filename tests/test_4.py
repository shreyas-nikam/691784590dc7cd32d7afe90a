import pytest
from unittest.mock import MagicMock, patch
import ipywidgets as widgets
from io import StringIO
import sys

# definition_367837c67003429eb6e04c9bf70fb255
from definition_367837c67003429eb6e04c9bf70fb255 import display_node_details
# </your_module>

# Sample tree_data for testing, based on the notebook specification and examples.
sample_tree_data = {
    "root": {
        "id": "root", "name": "Application A - Pathfinder", "parent_id": None,
        "score": 2.88, "level": 1, "construct": "Overall", "children": ["node_L2_VR"], "raw_assessment_items": []
    },
    "node_L2_VR": {
        "id": "node_L2_VR", "name": "Validity/Reliability (V/R)", "parent_id": "root",
        "score": 2.88, "level": 2, "construct": "Validity/Reliability",
        "children": ["node_L3_MT", "node_L3_RT", "node_L3_FT"], "raw_assessment_items": []
    },
    "node_L3_MT": {
        "id": "node_L3_MT", "name": "Model Testing (MT)", "parent_id": "node_L2_VR",
        "score": 0.72, "level": 3, "construct": "Model Testing",
        "children": ["node_L4_MTAL"], "raw_assessment_items": []
    },
    "node_L4_MTAL": {
        "id": "node_L4_MTAL", "name": "MT Annotator Label", "parent_id": "node_L3_MT",
        "score": 0.72, "level": 4, "construct": "Annotator Label",
        "children": ["node_L5_MTRA1", "node_L5_MTRA2"], "raw_assessment_items": []
    },
    "node_L5_MTRA1": {
        "id": "node_L5_MTRA1", "name": "MT RA 1", "parent_id": "node_L4_MTAL",
        "score": 0.0, "level": 5, "construct": "Response Collation",
        "children": [], "raw_assessment_items": [{"item_id": "raw_item_1", "score": 0.0, "question": "Question for RA 1"}]
    },
    "node_L5_MTRA2": {
        "id": "node_L5_MTRA2", "name": "MT RA 2", "parent_id": "node_L4_MTAL",
        "score": 0.0, "level": 5, "construct": "Response Collation",
        "children": [], "raw_assessment_items": [{"item_id": "raw_item_2", "score": 0.0, "question": "Question for RA 2"}]
    },
    "node_L3_RT": {
        "id": "node_L3_RT", "name": "Red Teaming (RT)", "parent_id": "node_L2_VR",
        "score": 2.88, "level": 3, "construct": "Red Teaming",
        "children": ["node_L4_RTAL", "node_L4_RTUP"], "raw_assessment_items": []
    },
    "node_L4_RTAL": {
        "id": "node_L4_RTAL", "name": "RT Annotator Label", "parent_id": "node_L3_RT",
        "score": 3.52, "level": 4, "construct": "Annotator Label",
        "children": ["node_L5_RTDD4"], "raw_assessment_items": []
    },
    "node_L5_RTDD4": {
        "id": "node_L5_RTDD4", "name": "RT DD 4", "parent_id": "node_L4_RTAL",
        "score": 4.98, "level": 5, "construct": "Response Collation",
        "children": [], "raw_assessment_items": [{"item_id": "raw_item_RTDD4", "score": 4.98, "question": "Is dialogue unnatural?"}]
    },
    "node_L4_RTUP": {
        "id": "node_L4_RTUP", "name": "RT User Perception", "parent_id": "node_L3_RT",
        "score": 2.24, "level": 4, "construct": "User Perception",
        "children": [], "raw_assessment_items": []
    },
    "node_L3_FT": {
        "id": "node_L3_FT", "name": "Field Testing (FT)", "parent_id": "node_L2_VR",
        "score": 2.36, "level": 3, "construct": "Field Testing",
        "children": ["node_L4_FTAL", "node_L4_FTUP"], "raw_assessment_items": []
    },
    "node_L4_FTAL": {
        "id": "node_L4_FTAL", "name": "FT Annotator Label", "parent_id": "node_L3_FT",
        "score": 3.06, "level": 4, "construct": "Annotator Label",
        "children": [], "raw_assessment_items": []
    },
    "node_L4_FTUP": {
        "id": "node_L4_FTUP", "name": "FT User Perception", "parent_id": "node_L3_FT",
        "score": 1.67, "level": 4, "construct": "User Perception",
        "children": ["node_L5_FTCC3"], "raw_assessment_items": []
    },
    "node_L5_FTCC3": {
        "id": "node_L5_FTCC3", "name": "FT CC 3", "parent_id": "node_L4_FTUP",
        "score": 7.41, "level": 5, "construct": "Response Collation",
        "children": [], "raw_assessment_items": [{"item_id": "raw_item_FTCC3", "score": 7.41, "question": "Is information superfluous?"}]
    },
    "node_L4_NoChildrenOrRaw": {
        "id": "node_L4_NoChildrenOrRaw", "name": "No Children or Raw Items", "parent_id": "node_L3_RT",
        "score": 1.0, "level": 4, "construct": "Placeholder", "children": [], "raw_assessment_items": []
    },
    "invalid_node_missing_level": {
        "id": "invalid_node_missing_level", "name": "Invalid Node", "parent_id": "root",
        "score": 5.0, "construct": "Invalid", "children": [], "raw_assessment_items": []
    }
}

# Fixture to mock ipywidgets.Output and capture its content
@pytest.fixture
def mock_output_widget(mocker):
    # This mock ensures that `widgets.Output()` returns a MagicMock instance
    # that also acts as a context manager.
    mock_out = MagicMock(spec=widgets.Output)
    # Configure the MagicMock to allow `with mock_out:` syntax
    mock_out.__enter__.return_value = mock_out
    mock_out.__exit__.return_value = None
    mocker.patch('ipywidgets.Output', return_value=mock_out)
    return mock_out

# Helper function to generate expected output content string
def get_expected_output_content(tree_data, node_id):
    node = tree_data[node_id]
    content = [
        f"--- Node Details for: {node['name']} (ID: {node_id}) ---",
        f"Level: {node['level']}, Construct: {node['construct']}",
        f"Aggregated Score: {node['score']:.2f}/10"
    ]

    if node['level'] < 5 and node['children']:
        content.append("\nDirect Children and their Scores:")
        for child_id in node['children']:
            child_node = tree_data.get(child_id)
            if child_node:
                content.append(f"  - {child_node['name']} (ID: {child_id}): {child_node['score']:.2f}/10")
            else:
                content.append(f"  - Child with ID '{child_id}' not found in tree_data.")
    elif node['level'] == 5 and node['raw_assessment_items']:
        content.append("\nContributing Assessment Items:")
        for item in node['raw_assessment_items']:
            content.append(f"  - Item ID: {item.get('item_id', 'N/A')}, Question: '{item.get('question', 'N/A')}'")
            content.append(f"    Score: {item.get('score', 'N/A'):.2f}/10")
    else:
        content.append("\nNo direct children or raw assessment items to display for this node.")
    return "\n".join(content) + "\n" # Add a final newline as print typically does

# Test Case 1: Display details for a Level 2 node (intermediate with children)
# Covers: Standard functionality for a parent node.
def test_display_node_details_level2_node(mock_output_widget, capsys):
    node_id = "node_L2_VR"
    result = display_node_details(sample_tree_data, node_id)
    assert isinstance(result, widgets.Output)
    captured = capsys.readouterr()
    expected_output = get_expected_output_content(sample_tree_data, node_id)
    assert captured.out == expected_output

# Test Case 2: Display details for a Level 5 node (leaf with raw assessment items)
# Covers: Leaf node specific logic, displaying raw assessment items.
def test_display_node_details_level5_node(mock_output_widget, capsys):
    node_id = "node_L5_RTDD4"
    result = display_node_details(sample_tree_data, node_id)
    assert isinstance(result, widgets.Output)
    captured = capsys.readouterr()
    expected_output = get_expected_output_content(sample_tree_data, node_id)
    assert captured.out == expected_output

# Test Case 3: Node not found
# Covers: Edge case where the requested node_id does not exist in tree_data.
def test_display_node_details_node_not_found():
    node_id = "non_existent_node"
    with pytest.raises(ValueError) as excinfo:
        display_node_details(sample_tree_data, node_id)
    assert f"Node with ID '{node_id}' not found." in str(excinfo.value)

# Test Case 4: Node with no children and no raw assessment items (Level 4 example)
# Covers: Intermediate node without children or raw items, ensuring graceful handling.
def test_display_node_details_no_children_or_raw_items(mock_output_widget, capsys):
    node_id = "node_L4_NoChildrenOrRaw"
    result = display_node_details(sample_tree_data, node_id)
    assert isinstance(result, widgets.Output)
    captured = capsys.readouterr()
    expected_output = get_expected_output_content(sample_tree_data, node_id)
    assert captured.out == expected_output

# Test Case 5: Invalid node structure (missing a required key like 'level')
# Covers: Robustness against malformed tree_data, expecting a KeyError.
def test_display_node_details_invalid_node_structure():
    node_id = "invalid_node_missing_level"
    with pytest.raises(KeyError) as excinfo:
        display_node_details(sample_tree_data, node_id)
    assert "Node 'invalid_node_missing_level' is missing required key: 'level'" in str(excinfo.value)
