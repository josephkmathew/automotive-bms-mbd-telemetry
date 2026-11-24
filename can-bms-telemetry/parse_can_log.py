import pandas as pd
import cantools

df = pd.read_csv("sample_can_log.csv")
df["arb_id_int"] = df["arb_id"].apply(lambda x: int(str(x), 16))
df["payload_bytes"] = df["data_hex"].apply(bytes.fromhex)

print("Loaded CAN rows:", len(df))
print(df[["timestamp", "arb_id", "arb_id_int", "dlc", "data_hex"]])
