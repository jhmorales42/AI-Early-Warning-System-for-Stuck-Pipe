# AI-Early-Warning-System-for-Stuck-Pipe
AI-driven Early Warning System (EWS) for Stuck Pipe prevention using **Random Forest**.

## Overview
This project implements a Machine Learning solution using the **Random Forest** algorithm to monitor drilling operations. By analyzing telemetry data (Torque, ROP, MSE, Friction Factors), the system detects the subtle onset of "Stuck Pipe" events (poor hole cleaning, differential sticking) before they become critical.

## Technical Approach
1.  **Physics-Based Feature Engineering**: The model ingests raw sensor data and computes advanced metrics such as *Friction Factor* and *Torque Trends* to isolate mechanical friction from normal drilling resistance.
2.  **Rigorous Time-Series Validation**: Unlike standard models, this system uses **`TimeSeriesSplit`** and strict chronological Train/Test separation to prevent data leakage, ensuring the model respects the temporal nature of drilling data.
3.  **Automated Hyperparameter Tuning**: Implements **`GridSearchCV`** to mathematically optimize the Random Forest configuration (n_estimators, max_depth) for the best balance between sensitivity and stability.
4.  **Dual-Stage Architecture**:
    * **Training Module:** Learns from historical offset well data using optimized parameters.
    * **Production Monitor:** Simulates inference on new wells to validate performance in a "blind" environment.

## Key Results
* **Lead Time Gained**: **37.1 hours (1.5 days)** of advance warning in production simulation.
* **Precision**: **100%** on "Risk" alerts (Zero False Alarms). The model prioritizes high confidence to prevent alarm fatigue.

## Requirements
To run this project, install the dependencies:
```bash
pip install -r requirements.txt
