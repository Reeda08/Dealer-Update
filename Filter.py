import os
import pandas as pd
from datetime import datetime

# Vista file download location
vista_download_dir = r"C:\Users\dsajekar\Downloads"

# Get latest Vista .xls file
def get_latest_vista_file(folder):
    files = [f for f in os.listdir(folder) if f.startswith("Vista Advanced") and f.endswith(".xls")]
    if not files:
        return None
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    return os.path.join(folder, files[0])

vista_file = get_latest_vista_file(vista_download_dir)

if not vista_file:
    print("❌ No Vista Advanced file found.")
    exit()

print(f"📥 Reading Vista file: {vista_file}")

# Read the .xls file
df = pd.read_excel(vista_file, dtype=str)
df.columns = df.columns.str.strip()

# Check column existence
if "Status Description" not in df.columns:
    print("❌ 'Status Description' column not found.")
    exit()

# Filter rows
filtered_df = df[df["Status Description"].isin(["Order Confirmed", "Holding Pool"])]

if filtered_df.empty:
    print("⚠️ No rows found with 'Order Confirmed' or 'Holding Pool'")
else:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(vista_download_dir, f"Filtered_Vista_Status_{timestamp}.csv")
    filtered_df.to_csv(output_file, index=False)
    print(f"✅ Filtered rows: {len(filtered_df)}")
    print(f"📁 Saved to: {output_file}")