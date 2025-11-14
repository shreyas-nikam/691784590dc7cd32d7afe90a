import pytest
from unittest.mock import MagicMock, patch

# Keep a placeholder definition_555a9410d22a468a955c8ef15b47eeb4 for the import of the module. Keep the `your_module` block as it is. DO NOT REPLACE or REMOVE the block.
from definition_555a9410d22a468a955c8ef15b47eeb4 import on_selection_change, build_corix_tree_data, create_interactive_corix_tree_plot

# --- Fixtures for setting up the test environment ---

@pytest.fixture
def mock_loaded_df():
    """Mocks the global pandas DataFrame `loaded_df`."""
    df = MagicMock()
    df.columns = ['Level', 'Construct', 'Application A - Pathfinder', 'Application B - TV Spoilers']
    return df

@pytest.fixture
def mock_app_dropdown():
    """Mocks the global ipywidgets.Dropdown instance `app_dropdown`."""
    dropdown = MagicMock()
    dropdown.value = "Application A - Pathfinder" # Default initial value
    return dropdown

@pytest.fixture
def mock_depth_slider():
    """Mocks the global ipywidgets.IntSlider instance `depth_slider`."""
    slider = MagicMock()
    slider.value = 5 # Default depth value
    return slider

@pytest.fixture
def mock_ipython_display(mocker):
    """Mocks IPython.display's `clear_output` and `display` functions."""
    mock_clear_output = mocker.patch('IPython.display.clear_output')
    mock_display = mocker.patch('IPython.display.display')
    yield mock_clear_output, mock_display

@pytest.fixture
def mock_corix_functions(mocker):
    """Mocks `build_corix_tree_data` and `create_interactive_corix_tree_plot` from your_module."""
    mock_build_tree = mocker.patch('definition_555a9410d22a468a955c8ef15b47eeb4.build_corix_tree_data', return_value={"tree": "data_structure"})
    mock_create_plot = mocker.patch('definition_555a9410d22a468a955c8ef15b47eeb4.create_interactive_corix_tree_plot', return_value=MagicMock(name="plotly_figure"))
    return mock_build_tree, mock_create_plot

@pytest.fixture(autouse=True)
def setup_on_selection_change_env(mocker, mock_loaded_df, mock_app_dropdown, mock_depth_slider):
    """
    Patches global variables/objects that `on_selection_change` implicitly uses.
    This fixture runs automatically for all tests in this file.
    """
    mocker.patch('definition_555a9410d22a468a955c8ef15b47eeb4.loaded_df', new=mock_loaded_df)
    mocker.patch('definition_555a9410d22a468a955c8ef15b47eeb4.app_dropdown', new=mock_app_dropdown)
    mocker.patch('definition_555a9410d22a468a955c8ef15b47eeb4.depth_slider', new=mock_depth_slider)

    # Patch the global output widgets themselves if they are directly referenced (e.g., in `with details_output:`).
    # This ensures they behave as context managers, which then call the mocked `IPython.display` functions.
    mocker.patch('definition_555a9410d22a468a955c8ef15b47eeb4.plot_output', new=MagicMock(name="plot_output_widget"))
    mocker.patch('definition_555a9410d22a468a955c8ef15b47eeb4.details_output', new=MagicMock(name="details_output_widget"))


# --- Test Cases for on_selection_change ---

def test_on_selection_change_valid_app_scenario(
    mock_loaded_df, mock_app_dropdown, mock_depth_slider,
    mock_ipython_display, mock_corix_functions
):
    """
    Test that on_selection_change correctly processes a valid application/scenario selection.
    Verifies that the tree data is built, plot is created, and output widgets are updated.
    """
    mock_app_dropdown.value = "Application A - Pathfinder"
    mock_depth_slider.value = 4 # Simulate a specific depth for the slider
    change_event = {'name': 'value', 'old': 'None', 'new': mock_app_dropdown.value}

    on_selection_change(change_event)

    # Assert clear_output is called twice (once for details, once for plot)
    mock_ipython_display[0].assert_any_call(wait=True)
    assert mock_ipython_display[0].call_count == 2

    # Assert build_corix_tree_data is called with correct arguments
    mock_corix_functions[0].assert_called_once_with(mock_loaded_df, "Application A", "Pathfinder")

    # Assert create_interactive_corix_tree_plot is called with tree data and depth
    mock_corix_functions[1].assert_called_once_with({"tree": "data_structure"}, 4)

    # Assert display is called with the figure returned by create_interactive_corix_tree_plot
    mock_ipython_display[1].assert_called_once_with(mock_corix_functions[1].return_value)


def test_on_selection_change_another_valid_app_scenario(
    mock_loaded_df, mock_app_dropdown, mock_depth_slider,
    mock_ipython_display, mock_corix_functions
):
    """
    Test with a different valid application/scenario to ensure dynamic updates
    and proper parsing of selection.
    """
    mock_app_dropdown.value = "Application B - TV Spoilers"
    mock_depth_slider.value = 5 # Default depth
    change_event = {'name': 'value', 'old': 'Application A - Pathfinder', 'new': mock_app_dropdown.value}

    on_selection_change(change_event)

    mock_ipython_display[0].assert_any_call(wait=True)
    assert mock_ipython_display[0].call_count == 2

    mock_corix_functions[0].assert_called_once_with(mock_loaded_df, "Application B", "TV Spoilers")
    mock_corix_functions[1].assert_called_once_with({"tree": "data_structure"}, 5)
    mock_ipython_display[1].assert_called_once_with(mock_corix_functions[1].return_value)


def test_on_selection_change_malformed_dropdown_value(
    mock_loaded_df, mock_app_dropdown, mock_ipython_display, mock_corix_functions, mocker
):
    """
    Test behavior when `app_dropdown.value` is malformed (e.g., lacks the ' - ' separator).
    Expect core functions not to be called, and graceful handling (e.g., printing an error).
    """
    mock_app_dropdown.value = "Just an Application" # Malformed string
    change_event = {'name': 'value', 'old': 'Application A - Pathfinder', 'new': mock_app_dropdown.value}

    mock_print = mocker.patch('builtins.print') # To capture any `print()` calls

    on_selection_change(change_event)

    # `details_output` clearing should still happen at the beginning of the function
    mock_ipython_display[0].assert_called_once_with(wait=True) # Only the first clear_output should be called

    # `build_corix_tree_data` and `create_interactive_corix_tree_plot` should NOT be called
    mock_corix_functions[0].assert_not_called()
    mock_corix_functions[1].assert_not_called()

    # `display` should not be called
    mock_ipython_display[1].assert_not_called()

    # Assert that an error message was printed
    mock_print.assert_called_once_with(f"Invalid dropdown value format: Just an Application")


def test_on_selection_change_empty_dropdown_value(
    mock_loaded_df, mock_app_dropdown, mock_ipython_display, mock_corix_functions, mocker
):
    """
    Test behavior when `app_dropdown.value` is an empty string.
    Expect core functions not to be called, and graceful handling.
    """
    mock_app_dropdown.value = "" # Empty string
    change_event = {'name': 'value', 'old': 'Application A - Pathfinder', 'new': mock_app_dropdown.value}

    mock_print = mocker.patch('builtins.print')

    on_selection_change(change_event)

    mock_ipython_display[0].assert_called_once_with(wait=True)

    mock_corix_functions[0].assert_not_called()
    mock_corix_functions[1].assert_not_called()

    mock_ipython_display[1].assert_not_called()

    mock_print.assert_called_once_with(f"Invalid dropdown value format: ")


def test_on_selection_change_build_corix_tree_data_failure(
    mock_loaded_df, mock_app_dropdown, mock_ipython_display, mock_corix_functions
):
    """
    Test behavior when `build_corix_tree_data` raises an exception.
    The exception should propagate, and subsequent visualization steps should not occur.
    """
    mock_app_dropdown.value = "Application A - Pathfinder"
    mock_corix_functions[0].side_effect = ValueError("Failed to build tree data due to missing column")
    change_event = {'name': 'value', 'old': 'None', 'new': mock_app_dropdown.value}

    with pytest.raises(ValueError, match="Failed to build tree data due to missing column"):
        on_selection_change(change_event)

    # `details_output` clearing should still happen at the beginning
    mock_ipython_display[0].assert_called_once_with(wait=True)

    # `build_corix_tree_data` should still be called (and raise its error)
    mock_corix_functions[0].assert_called_once_with(mock_loaded_df, "Application A", "Pathfinder")

    # `create_interactive_corix_tree_plot` should NOT be called if `build_corix_tree_data` fails
    mock_corix_functions[1].assert_not_called()

    # `display` should not be called
    mock_ipython_display[1].assert_not_called()