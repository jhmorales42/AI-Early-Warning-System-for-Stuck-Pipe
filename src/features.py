import pandas as pd

def feature_engineering(df, window=30):
    """
    Performs feature engineering on the drilling data.

    Calculates trends using a rolling window for Torque, ROP, and SPP.
    Calculates Friction Factor based on Torque, WOB, and Depth.

    Args:
        df (pd.DataFrame): The input dataframe containing raw sensor data.
        window (int): The window size for rolling average calculation.

    Returns:
        pd.DataFrame: Dataframe with new features added and NaN values dropped.
    """
    # Calculate trends (Moving Average)
    df['Torque_Trend'] = df['Torque_ft_lb'] / df['Torque_ft_lb'].rolling(window=window).mean()
    df['ROP_Trend'] = df['ROP_m_hr'] / df['ROP_m_hr'].rolling(window=window).mean()
    df['SPP_Trend'] = df['SPP_PSI'] / df['SPP_PSI'].rolling(window=window).mean()

    # Friction Factor
    # We add +1 to denominator to avoid division by zero if depth or wob is zero (unlikely but safe)
    df['Friction_Factor'] = df['Torque_ft_lb'] / (df['WOB_klbs'] * df['Depth_m'] + 1)

    return df.dropna().copy()
