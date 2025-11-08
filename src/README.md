# `src/` README — Core Utilities (Custom Exception & Logger)

This folder contains foundational utilities for the **MLOps Machine Maintenance** pipeline.
These modules provide **consistent logging** and **structured error handling** across all workflow stages — including **sensor data ingestion**, **preprocessing**, **feature engineering**, **model training**, **evaluation**, and **deployment for predictive maintenance**.

## 📁 Folder Overview

```text
src/
├─ custom_exception.py   # Unified and detailed exception handling
└─ logger.py             # Centralised logging configuration
```

## ⚠️ `custom_exception.py` — Unified Error Handling

### Purpose

Defines a `CustomException` class that captures detailed debugging context for any error that occurs in the pipeline — whether during **vibration/temperature data ingestion**, **signal processing**, **model fitting**, or **API inference**.

### Key Features

* Captures the **file name** and **line number** where the exception occurred.
* Includes a formatted **traceback** for quick, consistent debugging.
* Works with flexible inputs:

  * the `sys` module,
  * an explicit exception instance, or
  * no arguments (defaults to the current exception via `sys.exc_info()`).

### Example Usage

```python
from src.custom_exception import CustomException
import sys
import pandas as pd

try:
    df = pd.read_csv("data/raw/sensors.csv")
    if df.empty:
        raise ValueError("Sensor dataset is empty.")
except Exception as e:
    raise CustomException("Error during sensor data ingestion", sys) from e
```

### Output Example

```
Error in /mlops-machine-maintenance/src/data_ingestion.py, line 24: Error during sensor data ingestion
Traceback (most recent call last):
  File "/mlops-machine-maintenance/src/data_ingestion.py", line 24, in <module>
    df = pd.read_csv("data/raw/sensors.csv")
ValueError: Sensor dataset is empty.
```

This ensures all exceptions are reported in a **consistent, traceable format** across the Machine Maintenance pipeline — from raw telemetry handling to live model inference.

## 🪵 `logger.py` — Centralised Logging

### Purpose

Provides a **standardised logging setup** for the Machine Maintenance project.
Each log message is timestamped and written to a dated log file inside a `logs/` directory — enabling a clear audit trail across **ETL steps**, **feature calculations** (e.g., RMS vibration, rolling stats), **training runs**, and **serving-time predictions**.

### Log File Format

* Directory: `logs/`
* File name: `log_YYYY-MM-DD.log`
* Example: `logs/log_2025-11-08.log`

### Default Configuration

* Logging level: `INFO`
* Format:

  ```
  %(asctime)s - %(levelname)s - %(message)s
  ```

### Example Usage

```python
from src.logger import get_logger

logger = get_logger(__name__)

logger.info("Starting predictive maintenance pipeline.")
logger.warning("Missing vibration readings detected. Applying forward fill.")
logger.error("Training aborted due to invalid label distribution.")
```

### Output Example

```
2025-11-08 12:04:31,892 - INFO - Starting predictive maintenance pipeline.
2025-11-08 12:04:32,441 - WARNING - Missing vibration readings detected. Applying forward fill.
2025-11-08 12:04:33,009 - ERROR - Training aborted due to invalid label distribution.
```

## 🧩 Integration Guidelines

| Module Type         | Use `CustomException` for…                                  | Use `get_logger` for…                                           |
| ------------------- | ----------------------------------------------------------- | --------------------------------------------------------------- |
| Data Ingestion      | File/stream errors, schema mismatches, empty partitions     | File paths, batch sizes, schema summaries                       |
| Preprocessing       | Casting failures, resampling/windowing issues, NaNs         | Imputation choices, scaling ranges, outlier detection summaries |
| Feature Engineering | FFT/RMS failures, window overlap errors, invalid features   | Feature lists, window params, feature importance snapshots      |
| Model Training      | Invalid targets, convergence issues, shape mismatches       | Training progress, folds/metrics, hyperparameters per run       |
| Evaluation          | Metric computation errors, artifact write failures          | Validation metrics, confusion/ROC summaries                     |
| Inference/Serving   | Invalid payloads, missing model artefacts, timeout handling | Request volumes, latency, predicted RUL/failure probabilities   |
| CI/CD & Scheduling  | Failed job steps, API timeouts, credentials/secrets issues  | Stage boundaries, run durations, cloud job/resource statuses    |

**Tip:** Combine both tools for robust debugging and traceability:

```python
from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def predict_failure(model, X):
    try:
        logger.info(f"Inference started for {len(X)} machine records.")
        y_hat = model.predict(X)
        logger.info("Inference completed successfully.")
        return y_hat
    except Exception as e:
        logger.error("Inference step failed.")
        raise CustomException("Predictive maintenance inference error", sys) from e
```

## ✅ In summary

* `custom_exception.py` provides **clear, contextual error messages** for every exception.
* `logger.py` enables **structured, timestamped logging** across all project modules.

Together they form the **core reliability backbone** of the **MLOps Machine Maintenance** pipeline — supporting reproducibility, faster debugging, and transparent experiment tracking throughout the lifecycle.
