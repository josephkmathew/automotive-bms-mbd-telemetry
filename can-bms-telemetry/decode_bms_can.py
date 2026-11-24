import cantools
import pandas as pd

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

decoded_df = pd.DataFrame(decoded_rows)
print(decoded_df)
