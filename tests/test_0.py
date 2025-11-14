import pytest
import pandas as pd
from pathlib import Path
from io import StringIO

# Keep the definition_0c36275485164a078879d0c746ef062d block as it is. DO NOT REPLACE or REMOVE the block.
from definition_0c36275485164a078879d0c746ef062d import load_corix_dataset


# A helper fixture to create temporary CSV files for parameterized tests
@pytest.fixture
def _create_temp_csv(tmp_path):
    """
    Fixture to create a temporary CSV file with given content and return its path.
    """
    def _creator(filename, content):
        filepath = tmp_path / filename
        filepath.write_text(content)
        return str(filepath)
    return _creator

@pytest.mark.parametrize("filepath_arg, file_content, expected", [
    # Test Case 1: Successfully loads a valid CSV file with data.
    ("valid_corix.csv", "Level,Construct,Application A - Pathfinder,Application B - TV Spoilers\n"
                        "2,Validity/Reliability (V/R),2.88,4.29\n"
                        "3,Model Testing (MT),0.72,2.29",
     pd.DataFrame({
         "Level": [2, 3],
         "Construct": ["Validity/Reliability (V/R)", "Model Testing (MT)"],
         "Application A - Pathfinder": [2.88, 0.72],
         "Application B - TV Spoilers": [4.29, 2.29]
     })),

    # Test Case 2: Loads an empty CSV file (only headers), expecting an empty DataFrame with columns.
    ("empty_headers.csv", "Level,Construct,Application A - Pathfinder",
     pd.DataFrame(columns=["Level", "Construct", "Application A - Pathfinder"])),

    # Test Case 3: Handles a malformed CSV file that pandas cannot parse, expecting a ParserError.
    ("malformed.csv", "Level,Construct,Score\n1,\"Item A\",10\n2,\"Item B\"", # Malformed: last row incomplete
     pd.errors.ParserError),

    # Test Case 4: Handles a non-existent file path, expecting FileNotFoundError.
    ("non_existent_corix.csv", None, FileNotFoundError),

    # Test Case 5: Handles an invalid filepath type (e.g., an integer), expecting TypeError.
    (123, None, TypeError),
])
def test_load_corix_dataset(_create_temp_csv, filepath_arg, file_content, expected):
    """
    Comprehensive test for load_corix_dataset covering success, empty/malformed files,
    file not found, and invalid filepath types using a single parameterized test.
    """
    actual_filepath = None

    # Determine the actual filepath to use based on the test case type
    if isinstance(filepath_arg, str) and file_content is not None:
        # For cases requiring a temporary file to be created (valid, empty, malformed CSVs)
        actual_filepath = _create_temp_csv(filepath_arg, file_content)
    elif isinstance(filepath_arg, str) and file_content is None and expected == FileNotFoundError:
        # For FileNotFoundError, we pass a string that does not correspond to an existing file
        actual_filepath = filepath_arg
    else:
        # For cases with invalid `filepath_arg` types (e.g., int, None), pass it directly
        actual_filepath = filepath_arg

    try:
        # Call the function under test
        result = load_corix_dataset(actual_filepath)

        # Assertions for successful DataFrame loading
        assert isinstance(result, pd.DataFrame)
        pd.testing.assert_frame_equal(result, expected)

    except Exception as e:
        # Assertions for expected exceptions
        assert isinstance(e, expected)