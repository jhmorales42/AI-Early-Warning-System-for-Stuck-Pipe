# AI-Early-Warning-System-for-Stuck-Pipe
AI-driven Early Warning System (EWS) for Stuck Pipe prevention using **Random Forest**.
## Overview
This project implements a Machine Learning solution using the Random Forest algorithm to monitor real-time drilling operations. By analyzing telemetry data (Torque, ROP, MSE, Friction Factors), the system detects the subtle onset of "Stuck Pipe" events (e.g., poor hole cleaning, differential sticking) before they become critical.

## Technical Approach
**Physics-Based Feature Engineering**: The model ingests raw sensor data and computes advanced metrics such as Friction Factor and Torque Trends to isolate mechanical friction from normal drilling resistance.

## Dual-Stage Architecture:

**Training Module**: Learns from historical offset well data (stuckpipe_brain.joblib).

**Production Monitor**: Simulates real-time inference on new wells to validate performance.

**Predictive Analytics**: The system successfully detected the stuck pipe event with a lead time of **37 hours**, allowing sufficient time for remedial actions (e.g., wiper trips, mud conditioning).

**Economic Impact**: Automatically calculates potential NPT (Non-Productive Time) savings based on rig daily rates.

## Key Results
**Lead Time Gained**: 37.1 hours (**1.5 days**) of advance warning in production simulation.

**Precision**: 100% precision on "Risk" alerts (Zero False Alarms), ensuring high operational trust.

## Requirements
To run this project, install the dependencies: pip install -r requirements.txt
