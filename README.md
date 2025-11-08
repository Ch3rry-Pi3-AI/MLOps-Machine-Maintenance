# ⚙️ **Model Training — MLOps Machine Maintenance**

This branch advances the **MLOps Machine Maintenance** project by introducing the **`model_training.py`** module inside `src/`.
It represents the **second executable workflow stage** of the pipeline — focusing on **model training**, **evaluation**, and **persistence** using the preprocessed datasets generated in the previous **data processing** stage.

## 🧩 **Overview**

The `ModelTraining` class implements a **reproducible machine learning training and evaluation workflow** built on **Logistic Regression**.
It loads the processed artefacts, trains a predictive model for **machine efficiency classification**, evaluates performance with multiple metrics, and saves the trained model for later inference and deployment.

### 🔍 Core Responsibilities

| Stage | Operation          | Description                                                                                     |
| ----: | ------------------ | ----------------------------------------------------------------------------------------------- |
|   1️⃣ | **Load Data**      | Loads `X_train.pkl`, `X_test.pkl`, `y_train.pkl`, and `y_test.pkl` from `artifacts/processed/`. |
|   2️⃣ | **Train Model**    | Fits a `LogisticRegression` classifier on the training data.                                    |
|   3️⃣ | **Save Model**     | Serialises the trained model as `model.pkl` under `artifacts/models/`.                          |
|   4️⃣ | **Evaluate Model** | Computes accuracy, precision, recall, and F1-score using the test data.                         |

## 🗂️ **Updated Project Structure**

```text
mlops_machine_maintenance/
├── .venv/                           # 🧩 Local virtual environment (created by uv)
├── artifacts/
│   ├── raw/
│   │   └── data.csv                 # ⚙️ Input sensor dataset
│   ├── processed/                   # 💾 Data prepared by preprocessing
│   │   ├── X_train.pkl
│   │   ├── X_test.pkl
│   │   ├── y_train.pkl
│   │   ├── y_test.pkl
│   │   └── scaler.pkl
│   └── models/                      # 🧠 Trained model artefacts
│       └── model.pkl
├── pipeline/                        # ⚙️ Workflow orchestration (future automation)
├── src/
│   ├── __init__.py
│   ├── custom_exception.py          # Unified and detailed exception handling
│   ├── logger.py                    # Centralised logging configuration
│   ├── data_processing.py           # 🧩 Data preprocessing, scaling & splitting
│   └── model_training.py            # ⚙️ Model training, evaluation, and persistence
├── static/                          # 📊 Visual assets or diagnostics
├── templates/                       # 🧩 Placeholder for web/API templates
├── .gitignore                       # 🚫 Git ignore rules
├── .python-version                  # 🐍 Python version pin
├── pyproject.toml                   # ⚙️ Project metadata and uv configuration
├── requirements.txt                 # 📦 Python dependencies
├── setup.py                         # 🔧 Editable install support
└── uv.lock                          # 🔒 Locked dependency versions
```

## ⚙️ **How to Run the Model Training Module**

After completing the data processing stage and ensuring that the preprocessed artefacts exist in `artifacts/processed/`, run:

```bash
python src/model_training.py
```

### ✅ **Expected Successful Output**

```console
2025-11-08 14:10:51,105 - INFO - Model training initialised.
2025-11-08 14:10:51,189 - INFO - Processed training and testing datasets loaded successfully.
2025-11-08 14:10:51,872 - INFO - Model trained and saved successfully: artifacts/models/model.pkl
2025-11-08 14:10:52,034 - INFO - Model Evaluation Results:
2025-11-08 14:10:52,035 - INFO -   • Accuracy  : 0.8523
2025-11-08 14:10:52,035 - INFO -   • Precision : 0.8497
2025-11-08 14:10:52,035 - INFO -   • Recall    : 0.8523
2025-11-08 14:10:52,035 - INFO -   • F1 Score  : 0.8501
2025-11-08 14:10:52,036 - INFO - Model evaluation completed successfully.
2025-11-08 14:10:52,037 - INFO - Model training and evaluation pipeline completed.
```

This confirms that:

* Processed data splits were successfully loaded.
* The Logistic Regression model was trained and persisted as `model.pkl`.
* Evaluation metrics were calculated and logged clearly for traceability.

## 🧠 **Implementation Highlights**

* **Machine Learning Algorithm:**
  Uses **`LogisticRegression`** from **scikit-learn**, a lightweight, interpretable, and fast classifier ideal for baseline predictive maintenance models.

* **Integrated Logging** via `src/logger.py`
  Logs every step of the training lifecycle — including data loading, model fitting, and evaluation — with precise timestamps.

* **Unified Exception Handling** via `src/custom_exception.py`
  Ensures that all runtime or I/O errors are captured and raised with detailed, contextualised information.

* **Persisted Artefacts:**
  Trained models are saved to `artifacts/models/` for reuse in **inference**, **evaluation**, or **deployment** stages.

## 🧩 **Integration Guidelines**

| File                      | Purpose                                                            |
| ------------------------- | ------------------------------------------------------------------ |
| `src/model_training.py`   | Trains, evaluates, and saves the Logistic Regression model.        |
| `src/data_processing.py`  | Supplies preprocessed, scaled, and split datasets for training.    |
| `src/custom_exception.py` | Provides structured, traceable exception handling across modules.  |
| `src/logger.py`           | Records logs for transparency, debugging, and experiment tracking. |

✅ **In summary:**
This branch evolves the project into a **fully operational model-training stage** — integrating clean datasets from preprocessing, training a Logistic Regression model, and generating core performance metrics.
It sets the stage for upcoming **deployment**, **monitoring**, and **CI/CD automation** phases within the **MLOps Machine Maintenance** pipeline.
