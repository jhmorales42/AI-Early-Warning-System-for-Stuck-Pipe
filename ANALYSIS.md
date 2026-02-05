# Code Analysis: AI Early Warning System for Stuck Pipe

## 1. Project Overview
This project aims to detect "Stuck Pipe" events in drilling operations using a Machine Learning approach (Random Forest). It processes sensor data (Torque, ROP, SPP, etc.) to identify pre-cursor patterns (trends) that indicate an impending stuck pipe event. The system consists of a training module and a monitoring module.

## 2. Code Structure
*   **Notebooks:**
    *   `Notebooks/Drilling IA training.ipynb`: Handles data loading, feature engineering, model training, and evaluation. It generates the model (`stuckpipe_brain.joblib`) and configuration (`Conf_IA.joblib`).
    *   `Notebooks/Drilling IA monitor.ipynb`: Simulates a real-time monitoring environment by loading the trained model and predicting risk on a new dataset.
*   **Data:**
    *   `Data/drilling_data_stuckpipe.csv`: Historical data used for training, containing the `Phase_Status` target variable.
    *   `Data/drilling_data.csv`: "New" data used for the monitoring simulation.
*   **Models:**
    *   `stuckpipe_brain.joblib`: The trained Random Forest classifier.
    *   `Conf_IA.joblib`: Configuration dictionary containing feature names and thresholds.

## 3. Methodology Review

### Feature Engineering
The feature engineering logic is sound and aligned with drilling physics.
*   **Rolling Statistics:** The use of rolling averages (window=30) to calculate trends (`Torque_Trend`, `ROP_Trend`, `SPP_Trend`) is a standard and effective technique for detecting anomalies in time-series data relative to recent history.
*   **Friction Factor:** The calculation of `Friction_Factor` adds valuable domain-specific information.
*   **Target Definition:** Mapping `Phase_Status` to a binary target (0 for Normal, 1 for Risk/Stuck) fits the "Early Warning" problem statement well.

### Modeling
*   **Algorithm:** Random Forest is a robust choice for tabular sensor data. It handles non-linear relationships well and provides feature importance.
*   **Parameters:** `n_estimators=100, max_depth=10` are reasonable starting hyperparameters to prevent massive overfitting, though `max_depth` could be tuned.

## 4. Critical Findings & Issues

### 🔴 Critical: Evaluation on Training Data (Overfitting Risk)
The most significant issue is in `Drilling IA training.ipynb`.
*   **The Issue:** The model is trained on the full dataset (`df_model`), and then evaluated on the **exact same dataset**.
*   **Consequence:** The classification report shows perfect scores (Precision: 1.00, Recall: 1.00). **This is misleading.** A model evaluated on the data it memorized will always perform unrealistically well. It does not reflect how the model will perform on unseen future data.
*   **Recommendation:** You **must** split your data into a training set (e.g., first 80% of data) and a testing set (last 20% of data), or use Cross-Validation. Since this is time-series data, random shuffling should be avoided; split by time (e.g., train on earlier dates, test on later dates).

### 🟠 Hardcoded Parameters
*   **Window Size:** `window=30` is hardcoded. Depending on the data sampling rate (looks like 5 minutes), this represents 2.5 hours. If the sampling rate changes, this logic breaks.
*   **Threshold:** `alert_threshold=0.75` is hardcoded. This threshold controls the trade-off between False Alarms and Missed Detections. It should ideally be determined based on a precision-recall curve on the validation set.

### 🟡 Time-Series Considerations
*   **Leakage:** While standard Random Forest assumes independent samples, drilling data is highly correlated over time. Using a standard random split for validation would cause "data leakage" (training on future samples very similar to past test samples).
*   **Recommendation:** Use `TimeSeriesSplit` or a strict temporal cutoff for train/test splitting.

## 5. Recommendations for Improvement

1.  **Implement Train/Test Split:** Modify the training notebook to split `df_model` into `X_train, y_train` and `X_test, y_test` based on a cutoff date or index. Train on the first part, evaluate on the second.
2.  **Robust Evaluation:** Use metrics like ROC-AUC or Precision-Recall curves instead of just accuracy. Focus on Recall (catching the event) while keeping False Positives low.
3.  **Hyperparameter Tuning:** Use `GridSearchCV` or `RandomizedSearchCV` (with time-series aware splitting) to find optimal `max_depth` and `n_estimators`.
4.  **Config Management:** Move parameters like `window_size` and `threshold` into a config block or file so they can be easily adjusted.
5.  **Pipeline:** Consider using `sklearn.pipeline.Pipeline` to bundle the preprocessing (if any scaling/imputation is added later) with the model.

## 6. Conclusion
The codebase provides a solid functional prototype with correct domain logic. However, the **performance metrics reported in the training notebook are invalid due to evaluation on training data.** Addressing this is crucial to assessing the true value of the system.
