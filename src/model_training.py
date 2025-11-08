"""
model_training.py
=================
Implements the ``ModelTraining`` class for the Machine Maintenance workflow.

Overview
--------
This module defines a **reproducible model training and evaluation stage** for the
MLOps Machine Maintenance pipeline. It:
1) Loads preprocessed, scaled datasets from ``artifacts/processed/``
2) Trains a **Logistic Regression** model to predict machine efficiency
3) Persists the trained model to ``artifacts/models/``
4) Evaluates model performance using standard classification metrics

Notes
-----
- The Logistic Regression classifier is trained on pre-scaled numerical features.
- Evaluation metrics include accuracy, precision, recall, and F1-score.
- Logged metrics are recorded via the centralised project logger for traceability.
- The module integrates with ``CustomException`` for consistent error handling.

Saved Artefacts
---------------
- ``model.pkl`` — trained Logistic Regression model
- Logs include:
  * Training initialisation and completion
  * Evaluation metrics
  * Error diagnostics (if any)

Examples
--------
>>> mt = ModelTraining("artifacts/processed/", "artifacts/models/")
>>> mt.run()
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard & third-party imports
# -------------------------------------------------------------------
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# -------------------------------------------------------------------
# Internal imports
# -------------------------------------------------------------------
from src.logger import get_logger
from src.custom_exception import CustomException

# -------------------------------------------------------------------
# Logger setup
# -------------------------------------------------------------------
logger = get_logger(__name__)


# -------------------------------------------------------------------
# Class: ModelTraining
# -------------------------------------------------------------------
class ModelTraining:
    """
    Model training and evaluation class for predictive maintenance.

    Parameters
    ----------
    processed_data_path : str
        Path to the directory containing processed training/test artefacts
        (e.g., ``artifacts/processed/``).
    model_output_path : str
        Directory where trained model artefacts will be persisted
        (e.g., ``artifacts/models/``).

    Attributes
    ----------
    processed_path : str
        Directory containing preprocessed data splits.
    model_path : str
        Directory where the trained model is saved.
    clf : LogisticRegression | None
        Trained logistic regression model instance.
    X_train, X_test, y_train, y_test : np.ndarray | pd.Series
        Loaded training and testing data splits.
    """

    def __init__(self, processed_data_path: str, model_output_path: str) -> None:
        self.processed_path = processed_data_path
        self.model_path = model_output_path
        self.clf = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        os.makedirs(self.model_path, exist_ok=True)
        logger.info("Model training initialised.")

    # -------------------------------------------------------------------
    # Step 1: Load preprocessed data
    # -------------------------------------------------------------------
    def load_data(self) -> None:
        """
        Load preprocessed feature and target splits from disk.

        Raises
        ------
        CustomException
            If data files cannot be found or loaded.
        """
        try:
            self.X_train = joblib.load(os.path.join(self.processed_path, "X_train.pkl"))
            self.X_test = joblib.load(os.path.join(self.processed_path, "X_test.pkl"))
            self.y_train = joblib.load(os.path.join(self.processed_path, "y_train.pkl"))
            self.y_test = joblib.load(os.path.join(self.processed_path, "y_test.pkl"))

            logger.info("Processed training and testing datasets loaded successfully.")
            logger.info("Training set shape: %s, Test set shape: %s", self.X_train.shape, self.X_test.shape)
        except Exception as e:
            logger.error("Error while loading processed data: %s", e)
            raise CustomException("Failed to load processed data", e)

    # -------------------------------------------------------------------
    # Step 2: Train model
    # -------------------------------------------------------------------
    def train_model(self) -> None:
        """
        Train a Logistic Regression classifier on the loaded training data.

        Notes
        -----
        - Uses ``random_state=42`` for reproducibility.
        - Increases ``max_iter`` to 1000 to ensure convergence.

        Raises
        ------
        CustomException
            If model training or persistence fails.
        """
        try:
            self.clf = LogisticRegression(random_state=42, max_iter=1000)
            self.clf.fit(self.X_train, self.y_train)

            model_path = os.path.join(self.model_path, "model.pkl")
            joblib.dump(self.clf, model_path)

            logger.info("Model trained and saved successfully: %s", model_path)
        except Exception as e:
            logger.error("Error while training model: %s", e)
            raise CustomException("Failed to train model", e)

    # -------------------------------------------------------------------
    # Step 3: Evaluate model
    # -------------------------------------------------------------------
    def evaluate_model(self) -> None:
        """
        Evaluate the trained model on the test set and log key metrics.

        Metrics
        --------
        - Accuracy
        - Precision (weighted)
        - Recall (weighted)
        - F1-score (weighted)

        Raises
        ------
        CustomException
            If model evaluation fails.
        """
        try:
            if self.clf is None:
                raise ValueError("Model not trained. Call `train_model()` before evaluation.")

            y_pred = self.clf.predict(self.X_test)

            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, average="weighted")
            recall = recall_score(self.y_test, y_pred, average="weighted")
            f1 = f1_score(self.y_test, y_pred, average="weighted")

            logger.info("Model Evaluation Results:")
            logger.info("  • Accuracy  : %.4f", accuracy)
            logger.info("  • Precision : %.4f", precision)
            logger.info("  • Recall    : %.4f", recall)
            logger.info("  • F1 Score  : %.4f", f1)
            logger.info("Model evaluation completed successfully.")
        except Exception as e:
            logger.error("Error while evaluating model: %s", e)
            raise CustomException("Failed to evaluate model", e)

    # -------------------------------------------------------------------
    # Orchestrator
    # -------------------------------------------------------------------
    def run(self) -> None:
        """
        Execute the full model training and evaluation pipeline:
        1) Load processed datasets
        2) Train a Logistic Regression model
        3) Evaluate and log performance metrics
        """
        self.load_data()
        self.train_model()
        self.evaluate_model()
        logger.info("Model training and evaluation pipeline completed.")


# -------------------------------------------------------------------
# Script entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    trainer = ModelTraining("artifacts/processed/", "artifacts/models/")
    trainer.run()
