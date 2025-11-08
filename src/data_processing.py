"""
data_processing.py
==================
Implements the ``DataProcessing`` class for the Machine Maintenance workflow.

Overview
--------
This module provides a minimal, reproducible data-preparation stage used in the
project setup. It:
1) Loads a CSV dataset from disk
2) Expands a ``Timestamp`` column into calendar/time features
3) Casts and label-encodes selected categoricals
4) Standardises numeric features with ``StandardScaler``
5) Performs a stratified train/test split
6) Persists splits and the fitted scaler to ``artifacts/processed/`` via Joblib

Target & Features
-----------------
- Target:
  * ``Efficiency_Status`` (label-encoded)
- Features (in order used for scaling):
  * ``Operation_Mode``, ``Temperature_C``, ``Vibration_Hz``,
    ``Power_Consumption_kW``, ``Network_Latency_ms``, ``Packet_Loss_%``,
    ``Quality_Control_Defect_Rate_%``, ``Production_Speed_units_per_hr``,
    ``Predictive_Maintenance_Score``, ``Error_Rate_%``,
    ``Year``, ``Month``, ``Day``, ``Hour``

Saved Artefacts
---------------
- ``X_train.pkl``, ``X_test.pkl`` — scaled feature matrices (NumPy arrays)
- ``y_train.pkl``, ``y_test.pkl`` — target vectors
- ``scaler.pkl`` — fitted ``StandardScaler`` for inference/serving

Notes
-----
- ``LabelEncoder`` instances are **not** persisted here; if you need the exact
  mapping in downstream services, consider saving fitted encoders alongside the
  scaler.
- Any non-parsable timestamps are coerced to ``NaT`` (via ``errors='coerce'``);
  ensure upstream data quality or impute/drop as needed before modelling.

Examples
--------
>>> dp = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")
>>> dp.run()
"""

from __future__ import annotations

# Standard & third-party imports
import os
from typing import List, Optional, Sequence, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Internal imports
from src.logger import get_logger
from src.custom_exception import CustomException

# Logger setup
logger = get_logger(__name__)


class DataProcessing:
    """
    Simple, reproducible data-processing pipeline for Machine Maintenance.

    Parameters
    ----------
    input_path : str
        Path to the input CSV file (e.g., ``artifacts/raw/data.csv``).
    output_path : str
        Directory where processed artefacts are persisted
        (e.g., ``artifacts/processed``).

    Attributes
    ----------
    input_path : str
        Source CSV path.
    output_path : str
        Target directory for persisted artefacts.
    df : pd.DataFrame | None
        In-memory dataframe after loading.
    features : list[str] | None
        Ordered list of feature names used for scaling/splitting.
    """

    def __init__(self, input_path: str, output_path: str) -> None:
        self.input_path: str = input_path
        self.output_path: str = output_path
        self.df: Optional[pd.DataFrame] = None
        self.features: Optional[List[str]] = None

        os.makedirs(self.output_path, exist_ok=True)
        logger.info("Data processing initialised.")

    # ------------------------------------------------------------------
    # Step 1: Load
    # ------------------------------------------------------------------
    def load_data(self) -> None:
        """
        Load the dataset from ``self.input_path`` into ``self.df``.

        Raises
        ------
        CustomException
            If the CSV cannot be read.
        """
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info("Data loaded successfully. Shape: %s", None if self.df is None else self.df.shape)
        except Exception as e:
            logger.error("Error while loading data: %s", e)
            # Preserve call pattern used in the project’s CustomException
            raise CustomException("Failed to load data", e)

    # ------------------------------------------------------------------
    # Step 2: Preprocess
    # ------------------------------------------------------------------
    def preprocess(self) -> None:
        """
        Perform minimal preprocessing:
        - Parse ``Timestamp`` to datetime (coerce on error)
        - Cast selected categoricals
        - Derive calendar/time features: ``Year``, ``Month``, ``Day``, ``Hour``
        - Drop ``Timestamp`` and ``Machine_ID`` (identifier fields)
        - Label-encode ``Efficiency_Status`` and ``Operation_Mode``

        Raises
        ------
        CustomException
            If preprocessing fails or if data has not been loaded.
        """
        try:
            if self.df is None:
                raise ValueError("Dataframe is not loaded. Call `load_data()` first.")

            # Parse timestamp
            self.df["Timestamp"] = pd.to_datetime(self.df["Timestamp"], errors="coerce")

            # Ensure categoricals are treated as such
            categorical_cols: List[str] = ["Operation_Mode", "Efficiency_Status"]
            for col in categorical_cols:
                self.df[col] = self.df[col].astype("category")

            # Calendar/time expansion
            self.df["Year"] = self.df["Timestamp"].dt.year
            self.df["Month"] = self.df["Timestamp"].dt.month
            self.df["Day"] = self.df["Timestamp"].dt.day
            self.df["Hour"] = self.df["Timestamp"].dt.hour

            # Drop identifier & raw timestamp
            self.df.drop(columns=["Timestamp", "Machine_ID"], inplace=True)

            # Label encode selected categoricals
            columns_to_encode: List[str] = ["Efficiency_Status", "Operation_Mode"]
            for col in columns_to_encode:
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col])
                # Optional: log mapping for traceability
                mapping = dict(zip(le.classes_, range(len(le.classes_))))
                logger.info("Label mapping for %s: %s", col, mapping)

            logger.info("Basic data preprocessing completed.")
        except Exception as e:
            logger.error("Error while preprocessing data: %s", e)
            raise CustomException("Failed to preprocess data", e)

    # ------------------------------------------------------------------
    # Step 3: Split, scale, and persist
    # ------------------------------------------------------------------
    def split_and_scale_and_save(self) -> None:
        """
        Select features/target, standardise features, perform stratified split,
        and persist splits + scaler to disk.

        Persists
        --------
        - ``X_train.pkl``, ``X_test.pkl`` : np.ndarray
        - ``y_train.pkl``, ``y_test.pkl`` : pd.Series
        - ``scaler.pkl`` : fitted ``StandardScaler``

        Raises
        ------
        CustomException
            If scaling, splitting, or persistence fails.
        """
        try:
            if self.df is None:
                raise ValueError("Dataframe is not loaded. Call `load_data()` first.")

            self.features = [
                "Operation_Mode",
                "Temperature_C",
                "Vibration_Hz",
                "Power_Consumption_kW",
                "Network_Latency_ms",
                "Packet_Loss_%",
                "Quality_Control_Defect_Rate_%",
                "Production_Speed_units_per_hr",
                "Predictive_Maintenance_Score",
                "Error_Rate_%",
                "Year",
                "Month",
                "Day",
                "Hour",
            ]

            X: pd.DataFrame = self.df[self.features]
            y: pd.Series = self.df["Efficiency_Status"]

            scaler = StandardScaler()
            X_scaled: np.ndarray = scaler.fit_transform(X)

            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled,
                y,
                test_size=0.2,
                random_state=42,
                stratify=y,
            )

            joblib.dump(X_train, os.path.join(self.output_path, "X_train.pkl"))
            joblib.dump(X_test, os.path.join(self.output_path, "X_test.pkl"))
            joblib.dump(y_train, os.path.join(self.output_path, "y_train.pkl"))
            joblib.dump(y_test, os.path.join(self.output_path, "y_test.pkl"))
            joblib.dump(scaler, os.path.join(self.output_path, "scaler.pkl"))

            logger.info("Train/test splits and scaler saved successfully.")
        except Exception as e:
            logger.error("Error while splitting, scaling, and saving data: %s", e)
            raise CustomException("Failed to split, scale, and save data", e)

    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------
    def run(self) -> None:
        """
        Execute the full pipeline in order:
        1) Load data
        2) Preprocess (datetime expansion, categorical encoding)
        3) Split, scale, and persist datasets and scaler
        """
        self.load_data()
        self.preprocess()
        self.split_and_scale_and_save()
        logger.info("Data processing completed.")


# Script entrypoint
if __name__ == "__main__":
    processor = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")
    processor.run()
