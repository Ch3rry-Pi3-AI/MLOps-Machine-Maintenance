# `src/` README — Core Utilities & Data Processing

This folder contains foundational modules for the **MLOps Machine Maintenance** pipeline.
They provide **consistent logging**, **structured error handling**, and a **reproducible data-preparation stage** used across **sensor data ingestion**, **preprocessing**, **feature engineering**, **model training**, **evaluation**, and **deployment for predictive maintenance**.

## 📁 Folder Overview

```text
src/
├─ custom_exception.py     # Unified and detailed exception handling
├─ logger.py               # Centralised logging configuration
└─ data_processing.py      # Deterministic preprocessing, scaling & train/test persistence
```

## ⚠️ `custom_exception.py` — Unified Error Handling

### Purpose

Defines a `CustomException` that captures rich debugging context for any error — whether during **vibration/temperature ingestion**, **signal processing**, **model fitting**, or **API inference**.

### Key Features

* Captures the **file name** and **line number** where the exception occurred
* Includes a formatted **traceback** for quick, consistent debugging
* Works with flexible inputs: `sys`, an explicit exception, or defaults to `sys.exc_info()`

### Example

```python
from src.custom_exception import CustomException
import sys, pandas as pd

try:
    df = pd.read_csv("data/raw/sensors.csv")
    if df.empty:
        raise ValueError("Sensor dataset is empty.")
except Exception as e:
    raise CustomException("Error during sensor data ingestion", sys) from e
```

**Output example**

```
Error in /mlops-machine-maintenance/src/data_ingestion.py, line 24: Error during sensor data ingestion
Traceback (most recent call last):
  File "/mlops-machine-maintenance/src/data_ingestion.py", line 24, in <module>
    df = pd.read_csv("data/raw/sensors.csv")
ValueError: Sensor dataset is empty.
```

## 🪵 `logger.py` — Centralised Logging

### Purpose

Provides a **standardised logging setup**. Each message is timestamped and written to a dated file in `logs/`, giving a clear audit trail across **ETL**, **feature calculations** (e.g., RMS, rolling stats), **training runs**, and **serving-time predictions**.

### Defaults

* Directory: `logs/`
* File name: `log_YYYY-MM-DD.log` (e.g., `logs/log_2025-11-08.log`)
* Level: `INFO`
* Format: `%(asctime)s - %(levelname)s - %(message)s`

### Example

```python
from src.logger import get_logger
logger = get_logger(__name__)

logger.info("Starting predictive maintenance pipeline.")
logger.warning("Missing vibration readings detected. Applying forward fill.")
logger.error("Training aborted due to invalid label distribution.")
```

**Output example**

```
2025-11-08 12:04:31,892 - INFO - Starting predictive maintenance pipeline.
2025-11-08 12:04:32,441 - WARNING - Missing vibration readings detected. Applying forward fill.
2025-11-08 12:04:33,009 - ERROR - Training aborted due to invalid label distribution.
```

## 🧪 `data_processing.py` — Deterministic Preprocessing & Splits

### What it does

Implements a minimal, reproducible preparation stage that:

1. Loads a CSV from disk
2. Parses `Timestamp` and derives `Year`, `Month`, `Day`, `Hour`
3. Casts and **label-encodes** `Efficiency_Status` and `Operation_Mode`
4. **Standardises** numeric features using `StandardScaler`
5. Performs a **stratified** train/test split
6. Persists **scaled** splits and the **fitted scaler** to `artifacts/processed/`

### Target & Features

* **Target:** `Efficiency_Status` (label-encoded)
* **Feature order (used for scaling):**

  * `Operation_Mode`, `Temperature_C`, `Vibration_Hz`,
    `Power_Consumption_kW`, `Network_Latency_ms`, `Packet_Loss_%`,
    `Quality_Control_Defect_Rate_%`, `Production_Speed_units_per_hr`,
    `Predictive_Maintenance_Score`, `Error_Rate_%`,
    `Year`, `Month`, `Day`, `Hour`

### Saved artefacts

* `X_train.pkl`, `X_test.pkl` — **scaled** feature matrices (NumPy arrays)
* `y_train.pkl`, `y_test.pkl` — target vectors
* `scaler.pkl` — fitted `StandardScaler` (use for downstream inference)

> Note: `LabelEncoder` instances are not persisted. If you need exact label mappings in serving, consider saving the encoders alongside the scaler.

### Quick start

```python
from src.data_processing import DataProcessing

dp = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")
dp.run()
```

### CLI-style one-liner

```bash
python -m src.data_processing
```

## 🧩 Integration Guidelines

| Module Type         | Use `CustomException` for…                                  | Use `get_logger` for…                                           |
| ------------------- | ----------------------------------------------------------- | --------------------------------------------------------------- |
| Data Ingestion      | File/stream errors, schema mismatches, empty partitions     | File paths, batch sizes, schema summaries                       |
| Preprocessing       | Casting failures, resampling/windowing issues, NaNs         | Imputation choices, scaling ranges, outlier detection summaries |
| Feature Engineering | FFT/RMS failures, window overlap errors, invalid features   | Feature lists, window params, feature importance snapshots      |
| Model Training      | Invalid targets, convergence issues, shape mismatches       | Training progress, folds/metrics, hyperparameters per run       |
| Evaluation          | Metric computation errors, artefact write failures          | Validation metrics, confusion/ROC summaries                     |
| Inference/Serving   | Invalid payloads, missing model artefacts, timeout handling | Request volumes, latency, predicted RUL/failure probabilities   |
| CI/CD & Scheduling  | Failed job steps, API timeouts, credentials/secrets issues  | Stage boundaries, run durations, cloud job/resource statuses    |

**Tip:** Combine all three for robust traceability:

```python
from src.logger import get_logger
from src.custom_exception import CustomException
from src.data_processing import DataProcessing
import sys

logger = get_logger(__name__)

def build_dataset():
    try:
        dp = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")
        dp.run()
        logger.info("Dataset prepared successfully.")
    except Exception as e:
        logger.error("Dataset preparation failed.")
        raise CustomException("Data preparation error", sys) from e
```

## ✅ In summary

* `custom_exception.py` delivers **clear, contextual error messages**
* `logger.py` provides **structured, timestamped logging**
* `data_processing.py` ensures **deterministic preprocessing, scaling, and splits**

Together they form the **core reliability backbone** of the **MLOps Machine Maintenance** pipeline, enabling reproducibility, faster debugging, and smooth hand-offs from data prep to modelling and deployment.
