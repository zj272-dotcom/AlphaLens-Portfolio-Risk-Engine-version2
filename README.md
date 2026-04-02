# Portfolio Risk Engine

This project is a new portfolio risk engine built around a clean, reusable
multi-asset data pipeline. The current version focuses on two foundations:

- defining a stable ETF universe
- producing a clean return matrix and rolling train/test windows for later risk models

## Project Structure

```text
bigdata/
├── bigdata/
│   ├── __init__.py
│   ├── universe.py
│   └── data_pipeline.py
├── tests/
│   ├── conftest.py
│   └── test_data_pipeline.py
├── pyproject.toml
├── conda.yaml
└── README.md
```

## Version 1 Universe

The first-pass universe uses 9 liquid ETF proxies across major asset groups.

Asset list:

- SPY
- QQQ
- IWM
- TLT
- IEF
- GLD
- USO
- UUP
- EEM

Asset class mapping:

- Equities: SPY, QQQ, IWM, EEM
- Fixed Income: TLT, IEF
- Commodities: GLD, USO
- FX Proxy: UUP

Implementation:

- [`bigdata/universe.py`](./bigdata/universe.py) exposes `ASSET_LIST`
- [`bigdata/universe.py`](./bigdata/universe.py) exposes `ASSET_CLASS_MAPPING`
- [`bigdata/universe.py`](./bigdata/universe.py) also exposes `ASSET_UNIVERSE` for row-like structured access

## Data Pipeline

The data pipeline lives in [`bigdata/data_pipeline.py`](./bigdata/data_pipeline.py).
It is designed to produce a stable input matrix for downstream risk models.

### What It Does

1. Downloads daily adjusted close prices from Yahoo Finance.
2. Aligns all assets to a unified business-day calendar.
3. Measures missingness by asset.
4. Drops assets whose missing ratio is above a chosen threshold.
5. Forward fills intermediate missing values.
6. Drops any remaining leading NaNs that cannot be filled.
7. Computes daily simple returns with `pct_change()`.
8. Clips extreme return observations to reduce outlier distortion.
9. Splits the clean return matrix into rolling train/test windows.

### Main Functions

- `download_adjusted_close_prices(...)`
  Downloads adjusted close data and returns a price matrix indexed by date.
- `align_and_clean_prices(...)`
  Reindexes to a common business-day calendar, removes overly sparse assets, forward fills gaps, and drops remaining leading NaNs.
- `compute_clean_return_matrix(...)`
  Converts cleaned prices to daily simple returns and clips extreme values.
- `create_rolling_windows(...)`
  Builds rolling train/test splits, with defaults of 252 trading days for training and 21 for testing.
- `build_data_pipeline(...)`
  Runs the full workflow and returns a `DataPipelineResult` bundle.

### Pipeline Outputs

The pipeline returns a `DataPipelineResult` object containing:

- `clean_return_matrix`
  Fully aligned daily return matrix with no NaNs.
- `training_test_windows`
  Rolling train/test windows for backtesting or model validation.
- `clean_price_matrix`
  Aligned and cleaned adjusted close matrix.
- `missing_ratio_by_asset`
  Per-asset missingness diagnostics before dropping sparse assets.
- `dropped_assets`
  List of assets removed because they exceeded the missing-data threshold.

### Rolling Window Design

The current default setup is:

- training window: 252 trading days
- test window: 21 trading days
- step size: 21 trading days

This is meant to simulate real-world model recalibration without look-ahead bias.

## Unit Tests

The test suite is now organized under [`tests/`](./tests).

Current coverage focus:

- adjusted close download behavior
- business-day alignment
- missing-value cleaning
- return matrix construction
- rolling window generation
- end-to-end pipeline output shape

Main test file:

- [`tests/test_data_pipeline.py`](./tests/test_data_pipeline.py)

Shared fixtures:

- [`tests/conftest.py`](./tests/conftest.py)

## Installation

### Using Pip

```bash
pip install -e ".[test]"
```

### Using Conda

```bash
conda env create -f conda.yaml
conda activate bigdata
```

## Running Tests

```bash
pytest
```

If you want coverage output:

```bash
pytest --cov=bigdata --cov-report=term-missing
```

## Current Scope

At this stage, the project intentionally focuses on the data foundation first.
Risk metrics, factor models, and stress testing can be layered on top of the
same clean return matrix once the pipeline is stable.
