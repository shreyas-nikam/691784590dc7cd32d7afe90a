import pytest
import numpy as np
import math
from definition_02bb8e75d74b497194471d98600ebf3f import aggregate_node_score

@pytest.mark.parametrize("children_scores, level, expected", [
    # Test case 1: Level 2 (Risks) - numpy.max aggregation
    ([1.0, 5.0, 2.0], 2, 5.0),
    # Test case 2: Level 3 (Testing Level) - numpy.mean aggregation
    ([10.0, 20.0, 30.0], 3, 20.0),
    # Test case 3: Level 4 or 5 (Mean aggregation) - single element list
    ([7.5], 4, 7.5),
    # Test case 4: Edge case - empty list for numpy.max (Level 2), should raise ValueError
    ([], 2, ValueError),
    # Test case 5: Edge case - empty list for numpy.mean (Level 3), should result in NaN
    ([], 3, float('nan')),
])
def test_aggregate_node_score(children_scores, level, expected):
    """
    Tests the aggregate_node_score function for various levels,
    children_scores lists, and edge cases.
    """
    try:
        result = aggregate_node_score(children_scores, level)
        # Special handling for NaN comparison
        if math.isnan(expected):
            assert math.isnan(result)
        else:
            # Use pytest.approx for floating point comparisons
            assert result == pytest.approx(expected)
    except Exception as e:
        # Check if the raised exception is of the expected type
        assert isinstance(e, expected)