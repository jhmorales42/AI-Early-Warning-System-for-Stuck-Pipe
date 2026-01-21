import matplotlib.pyplot as plt

def generate_impact_report(df_results, alert_threshold=0.75):
    """
    Generates a value report based on AI predictions and actual stuck pipe events.

    Args:
        df_results (pd.DataFrame): Dataframe containing 'Date', 'Phase_Status' and 'Risk_Probability'.
        alert_threshold (float): Probability threshold to trigger an alert.

    Returns:
        tuple: (ai_alert_date, real_stuck_date) or (None, None) / (None, real_stuck_date)
    """
    stuck_events = df_results[df_results['Phase_Status'] == 'Stuck']
    if len(stuck_events) == 0:
        print(" No Stuck Pipe events detected.")
        return None, None

    real_stuck_date = stuck_events['Date'].iloc[0]

    # Find first AI alert before the event
    ai_alerts = df_results[
        (df_results['Risk_Probability'] >= alert_threshold) &
        (df_results['Date'] < real_stuck_date)
    ]

    print("\n" + "="*60)
    print("        VALUE REPORT: ARTIFICIAL INTELLIGENCE        ")
    print("="*60)

    if len(ai_alerts) > 0:
        ai_alert_date = ai_alerts['Date'].iloc[0]
        time_gained = real_stuck_date - ai_alert_date
        hours_gained = time_gained.total_seconds() / 3600
        days_gained = hours_gained / 24
        estimated_savings = hours_gained * 5000

        print(f" Critical Event Date (Stuck Pipe):  {real_stuck_date}")
        print(f" Early Detection Date (AI):         {ai_alert_date}")
        print("-" * 60)
        print(f" REACTION TIME GAINED:            {hours_gained:.1f} HOURS ({days_gained:.1f} Days)")
        print("-" * 60)
        print(f" POTENTIAL ECONOMIC IMPACT:")
        print(f"   (Base: NPT Cost = $5,000 / hour)")
        print(f"   VALUE PRESERVED:                 ${estimated_savings:,.2f} USD")
        print("="*60)
        return ai_alert_date, real_stuck_date
    else:
        print(" AI did not generate early warning.")
        return None, real_stuck_date

def plot_results(df_model, ai_date, real_date, alert_threshold=0.75):
    """
    Plots the AI Risk Probability and Real Torque, highlighting the time gained.

    Args:
        df_model (pd.DataFrame): Dataframe with 'Date', 'Risk_Probability', and 'Torque_ft_lb'.
        ai_date (datetime): The date when AI detected the risk.
        real_date (datetime): The actual date of the stuck pipe event.
        alert_threshold (float): The threshold used for alerts.
    """
    if not (ai_date and real_date):
        print("Cannot plot results: missing dates.")
        return

    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot 1: AI Risk Probability (Left Axis - Red)
    ax1.plot(df_model['Date'], df_model['Risk_Probability'], color='#e74c3c', label='AI Risk Probability', linewidth=2)
    ax1.set_ylabel('Stuck Pipe Risk (0-100%)', color='#e74c3c', fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='#e74c3c')
    ax1.set_ylim(-0.05, 1.1)

    # Threshold Line
    ax1.axhline(y=alert_threshold, color='#f39c12', linestyle='--', alpha=0.8, label=f'Alert Threshold ({alert_threshold*100:.0f}%)')

    # Plot 2: Physical Torque (Right Axis - Gray)
    ax2 = ax1.twinx()
    ax2.plot(df_model['Date'], df_model['Torque_ft_lb'], color='#7f8c8d', alpha=0.3, label='Real Torque (Sensor)', linewidth=1)
    ax2.set_ylabel('Torque (ft-lb)', color='#7f8c8d', fontsize=12)

    # Highlight: Time Gained Zone (Green Area)
    ax1.axvspan(ai_date, real_date, color='#2ecc71', alpha=0.2, label='Time Gained (Action Window)')

    # Annotations
    ax1.axvline(x=ai_date, color='#27ae60', linestyle='-', linewidth=2)
    ax1.text(ai_date, 1.02, '  AI DETECTION', color='#27ae60', fontweight='bold', ha='left', va='bottom')

    ax1.axvline(x=real_date, color='#c0392b', linestyle='-', linewidth=2)
    ax1.text(real_date, 1.02, 'REAL STUCK PIPE  ', color='#c0392b', fontweight='bold', ha='right', va='bottom')

    # Final Polish
    time_gained_seconds = (real_date - ai_date).total_seconds()
    plt.title(f'AI Early Warning System: {time_gained_seconds/3600:.1f} Hours Gained', fontsize=16)
    plt.grid(True, linestyle=':', alpha=0.6)

    # Combine legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', bbox_to_anchor=(0.02, 0.95))

    plt.tight_layout()
    plt.show()
