import pandas as pd
import pytest


@pytest.fixture
def sample_prices_with_gaps():
    index = pd.to_datetime(
        [
            "2024-01-01",
            "2024-01-02",
            "2024-01-04",
            "2024-01-05",
        ]
    )
    return pd.DataFrame(
        {
            "SPY": [100.0, 101.0, 103.0, 104.0],
            "QQQ": [200.0, None, 202.0, 203.0],
            "BAD": [None, None, 50.0, 51.0],
        },
        index=index,
    )


@pytest.fixture
def clean_return_matrix():
    index = pd.bdate_range("2024-01-01", periods=12)
    return pd.DataFrame(
        {
            "SPY": [0.01, 0.00, -0.01, 0.02, 0.01, 0.00, 0.01, -0.02, 0.01, 0.00, 0.01, 0.02],
            "QQQ": [0.02, -0.01, 0.00, 0.01, 0.03, -0.01, 0.00, 0.01, 0.02, -0.02, 0.01, 0.00],
        },
        index=index,
    )
