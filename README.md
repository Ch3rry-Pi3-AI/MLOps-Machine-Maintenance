# ⚙️ **Data Processing — MLOps Machine Maintenance**

This branch builds upon the **initial setup** by introducing the **`data_processing.py`** module inside `src/`.
It marks the **first executable workflow stage** of the **MLOps Machine Maintenance** pipeline — responsible for loading raw machine sensor data, cleaning and transforming it, encoding categorical features, scaling numerical inputs, and saving train/test splits for model training and predictive maintenance analysis.

## 🧩 **Overview**

The `DataProcessing` class implements a **deterministic preprocessing workflow** with integrated logging and unified exception handling.
It produces reproducible, well-structured datasets ready for downstream models that predict machine efficiency or failure risk.

### 🔍 Core Responsibilities

| Stage | Operation          | Description                                                                                           |
| ----: | ------------------ | ----------------------------------------------------------------------------------------------------- |
|   1️⃣ | **Load Data**      | Reads input CSV from `artifacts/raw/data.csv`.                                                        |
|   2️⃣ | **Preprocess**     | Parses `Timestamp`, derives `Year`, `Month`, `Day`, and `Hour`, and label-encodes categorical fields. |
|   3️⃣ | **Scale Features** | Standardises numeric features with `StandardScaler` to normalise input magnitudes.                    |
|   4️⃣ | **Split Data**     | Performs an 80/20 **stratified** train/test split on `Efficiency_Status`.                             |
|   5️⃣ | **Save Artefacts** | Persists scaled splits and the fitted scaler into `artifacts/processed/`.                             |

## 🗂️ **Updated Project Structure**

```text
mlops_machine_maintenance/
├── .venv/                          # 🧩 Local virtual environment (created by uv)
├── artifacts/
│   ├── raw/
│   │   └── data.csv                # ⚙️ Input sensor dataset
│   └── processed/                  # 💾 Processed output artefacts
│       ├── X_train.pkl
│       ├── X_test.pkl
│       ├── y_train.pkl
│       ├── y_test.pkl
│       └── scaler.pkl
├── mlops_machine_maintenance.egg-info/ # 📦 Package metadata (auto-generated)
├── pipeline/                       # ⚙️ Pipeline orchestration (future stage)
├── src/
│   ├── __init__.py
│   ├── custom_exception.py         # Unified and detailed exception handling
│   ├── logger.py                   # Centralised logging configuration
│   └── data_processing.py          # 🧠 End-to-end sensor data preparation
├── static/                         # 📊 Visual or diagnostic assets
├── templates/                      # 🧩 Placeholder for web/API templates
├── .gitignore                      # 🚫 Git ignore rules
├── .python-version                 # 🐍 Python version pin
├── pyproject.toml                  # ⚙️ Project metadata and uv configuration
├── requirements.txt                # 📦 Python dependencies
├── setup.py                        # 🔧 Editable install support
└── uv.lock                         # 🔒 Locked dependency versions
```

## ⚙️ **How to Run the Data Processing Module**

After activating the virtual environment and ensuring your dataset is located at `artifacts/raw/data.csv`, run:

```bash
python src/data_processing.py
```

### ✅ **Expected Successful Output**

```console
2025-11-08 14:02:11,213 - INFO - Data loaded successfully. Shape: (5000, 15)
2025-11-08 14:02:11,327 - INFO - Label mapping for Efficiency_Status: {'Low': 0, 'Medium': 1, 'High': 2}
2025-11-08 14:02:11,365 - INFO - Label mapping for Operation_Mode: {'Idle': 0, 'Active': 1, 'Maintenance': 2}
2025-11-08 14:02:11,402 - INFO - Basic data preprocessing completed.
2025-11-08 14:02:11,601 - INFO - Train/test splits and scaler saved successfully.
2025-11-08 14:02:11,605 - INFO - Data processing completed.
```

This confirms that:

* The raw sensor dataset was successfully read and parsed.
* `Timestamp` values were converted to calendar/time components.
* Categorical fields were label-encoded and numerical features scaled.
* Clean, standardised train/test splits and a reusable scaler were saved under `artifacts/processed/`.

## 🧠 **Implementation Highlights**

* **Integrated Logging** — powered by `src/logger.py`
  Every step is timestamped and recorded for full experiment traceability.

* **Unified Exception Handling** — via `src/custom_exception.py`
  Any failure during ingestion, transformation, or scaling raises contextual errors for rapid debugging.

* **Scalable, Modular Design**
  The `DataProcessing` class is reusable and importable — easily extended for pipeline orchestration, model training, and deployment workflows.

## 🧩 **Integration Guidelines**

| File                      | Purpose                                                                |
| ------------------------- | ---------------------------------------------------------------------- |
| `src/data_processing.py`  | Executes the sensor data preprocessing workflow end-to-end.            |
| `src/custom_exception.py` | Provides structured, contextual exception handling across all modules. |
| `src/logger.py`           | Delivers consistent, timestamped logs for pipeline reproducibility.    |

✅ **In summary:**
This branch upgrades the repository from a static scaffold into a **fully functional preprocessing stage** of the **MLOps Machine Maintenance** pipeline — producing clean, standardised artefacts, traceable logs, and reproducible results that set the foundation for **predictive maintenance modelling, training, and deployment** in later stages.
