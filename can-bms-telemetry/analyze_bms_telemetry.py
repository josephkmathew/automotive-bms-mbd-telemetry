import cantools
import pandas as pd
import matplotlib.pyplot as plt

db = cantools.database.load_file("bms_telemetry.dbc")
df = pd.read_csv("bms_can_log.csv")

decoded_rows = []
for _, row in df.iterrows():
    arb_id = int(str(row["arb_id"]), 16)
    payload = bytes.fromhex(row["data_hex"])
    msg = db.get_message_by_frame_id(arb_id)
    signals = msg.decode(payload)
    decoded_rows.append({
        "timestamp": row["timestamp"],
        "message": msg.name,
        **signals
    })

telemetry = pd.DataFrame(decoded_rows).sort_values("timestamp").reset_index(drop=True)
for col in ["PackVoltage_V", "PackCurrent_A", "SoC_Pct", "Fault_Code"]:
    if col in telemetry.columns:
        telemetry[col] = telemetry[col].ffill()

# Example pack-level threshold check (e.g., flag if PackVoltage_V < 200 V or Fault_Code != 0)
telemetry["Voltage_OK"] = telemetry["PackVoltage_V"] >= 200.0
telemetry["No_Fault"] = telemetry["Fault_Code"] == 0.0
telemetry["Row_Pass"] = telemetry["Voltage_OK"] & telemetry["No_Fault"]

print("=== Aligned Telemetry & Pass/Fail Checks ===")
print(telemetry[["timestamp", "PackVoltage_V", "PackCurrent_A", "SoC_Pct", "Fault_Code", "Row_Pass"]])

overall_pass = bool(telemetry["Row_Pass"].all())
print(f"\nOverall Telemetry Check: {'PASS' if overall_pass else 'FAIL'}")

# Step 2: Plot Voltage, SoC, and Fault_Code
fig, axes = plt.subplots(3, 1, figsize=(8, 6), sharex=True)

axes[0].plot(telemetry["timestamp"], telemetry["PackVoltage_V"], marker="o", label="PackVoltage_V")
axes[0].axhline(200.0, color="r", linestyle="--", label="Min Threshold (200V)")
axes[0].set_ylabel("Voltage (V)")
axes[0].legend(loc="best")
axes[0].grid(True)

axes[1].plot(telemetry["timestamp"], telemetry["SoC_Pct"], marker="s", color="g", label="SoC_Pct")
axes[1].set_ylabel("SoC (%)")
axes[1].legend(loc="best")
axes[1].grid(True)

axes[2].step(telemetry["timestamp"], telemetry["Fault_Code"], where="post", marker="^", color="orange", label="Fault_Code")
axes[2].set_ylabel("Fault Code")
axes[2].set_xlabel("Time (s)")
axes[2].legend(loc="best")
axes[2].grid(True)

plt.tight_layout()
plt.savefig("bms_telemetry_plot.png", dpi=150)
print("Saved plot to bms_telemetry_plot.png")
