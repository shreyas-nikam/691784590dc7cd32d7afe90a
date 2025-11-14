import pytest
from unittest.mock import Mock, patch

# Keep the definition_5f1acdd837b2421bb000d9d732a93771 block as it is. DO NOT REPLACE or REMOVE the block.
# from definition_5f1acdd837b2421bb000d9d732a93771 import on_node_click, display_node_details 


def _create_mock_plotly_points(customdata_list):
    """Helper to create a list of plotly point mocks with specified customdata."""
    if customdata_list is None:
        return None
    return [Mock(customdata=cd) for cd in customdata_list]

def _create_mock_point_without_customdata_attr():
    """Helper to create a plotly point mock without a 'customdata' attribute."""
    return [Mock(point_index=0)]

@pytest.mark.parametrize(
    "test_name, points_mock, tree_data, expected_call, expected_node_id",
    [
        (
            "successful_node_click",
            _create_mock_plotly_points([['node_id_123', 'Node Name', 5.0]]),
            {'node_id_123': {'name': 'Node 123'}},
            True, # display_node_details should be called
            'node_id_123'
        ),
        (
            "no_points_clicked_empty_list",
            [], # points is an empty list
            {},
            False, # display_node_details should not be called
            None
        ),
        (
            "points_is_none",
            None, # points is None
            {},
            False,
            None
        ),
        (
            "point_without_customdata_attribute",
            _create_mock_point_without_customdata_attr(), # points[0] exists but lacks customdata
            {},
            False,
            None
        ),
        (
            "customdata_without_node_id_at_index_0",
            _create_mock_plotly_points([['just_some_other_data', 'Node Name', 5.0]]), # customdata doesn't start with node ID
            {},
            False, # assuming the function expects node_id at customdata[0]
            None
        ),
        # (
        #     "invalid_tree_data_format", # on_node_click should still attempt to call display_node_details; validation is DND's job
        #     _create_mock_plotly_points([['node_id_123', 'Node Name', 5.0]]),
        #     None, # tree_data is None
        #     True,
        #     'node_id_123'
        # ),
    ]
)
def test_on_node_click_scenarios(test_name, points_mock, tree_data, expected_call, expected_node_id):
    """
    Tests various scenarios for the on_node_click function, including successful
    node clicks and various edge cases for the 'points' argument.
    """
    trace = Mock()
    state = Mock()
    output_widget = Mock()

    # We need to mock display_node_details as it's a dependency called by on_node_click
    # and its implementation is not part of the current stub for on_node_click.
    with patch('definition_5f1acdd837b2421bb000d9d732a93771.display_node_details') as mock_display_node_details:
        # Import on_node_click inside the patch context to ensure it sees the mocked display_node_details
        from definition_5f1acdd837b2421bb000d9d732a93771 import on_node_click 
        on_node_click(trace, points_mock, state, tree_data, output_widget)

        if expected_call:
            mock_display_node_details.assert_called_once_with(tree_data, expected_node_id)
        else:
            mock_display_node_details.assert_not_called()